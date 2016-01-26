
import os, sys
import time
import argparse
from os.path import *
from osgeo import ogr, gdal
from multiprocessing import Process

os.environ['GDAL_DATA'] = abspath(join(sys.executable, '../../share/gdal'))


def new_raster_from_base(base, output, format, nodata, datatype):
    """
    creates and empty raster object using a base raster as a template 
    http://gis.stackexchange.com/questions/31568/gdal-rasterizelayer-doesnt-burn-all-polygons-to-raster
    :param base: base raster layer to use as a template 
    :param output: output raster object 
    :param format: format of the raster object
    :param nodata: nodata value 
    :param datatype: value datatype 
    :return: empty raster object
    """
   
    projection = base.GetProjection()
    geotransform = base.GetGeoTransform()
    bands = base.RasterCount

    driver = gdal.GetDriverByName(format)

    new_raster = driver.Create(str(output), cols, rows, bands, datatype)
    new_raster.SetProjection(projection)
    new_raster.SetGeoTransform(geotransform)

    for i in range(bands):
        new_raster.GetRasterBand(i + 1).SetNoDataValue(nodata)
        new_raster.GetRasterBand(i + 1).Fill(nodata)

    return new_raster


def rasterize_and_align(input_layer, input_raster, output_raster):
    """
    converts shapefile layer into a GTiff and aligns the cells with an existing raster
    :param input_layer: shapefile layer that will be rasterized
    :param input_raster: existing raster is used to align the rasterized layer
    :param output_raster: output rasterized and aligned GTiff
    :return: None
    """

    # open the input layer
    shape_datasource = ogr.Open(input_layer)
    shape_layer = shape_datasource.GetLayer()

    # open the output raster
    out_raster = gdal.Open(output_raster)
    rast = gdal.Open(input_raster, gdal.GA_ReadOnly)

    # create a new dataset using the base raster as a template
    print 'Creating an empty output dataset by cloning %s' % rast
    raster_dataset = new_raster_from_base(rast, output_raster, 'GTiff', -1, gdal.GDT_Int32)


    # multiprocess this since it could take a while.
    print 'Rasterizing: %s' % output_raster
    # convert shapefile into raster
    proc = Process(target=gdal.RasterizeLayer, args=(raster_dataset, [1], shape_layer, None, None, [1], ['ATTRIBUTE=MUKEY']))
    proc.start()
    while proc.is_alive():
        time.sleep(0.5)
        sys.stdout.write('.')
        sys.stdout.flush()
    proc.join()

    # gdal.RasterizeLayer(raster_dataset, [1], shape_layer, None, None, [1], ['ATTRIBUTE=MUKEY'] )

    print 'Rasterization complete'
    print 'Conversion Info:'
    # print some stats
    geo = rast.GetGeoTransform()
    print 20 * '- '
    print 'Input raster info: %s' % basename(input_raster)
    print ' rows : %d'       % (rast.RasterXSize)
    print ' cols : %d'       % (rast.RasterYSize)
    print ' proj : %s'       % (rast.GetProjection())
    print ' xcell: %3.5f'   % (geo[1])
    print ' ycell: %3.5f'   % (geo[5])
    print ' ulx  : %3.5f'   % (geo[0])
    print ' uly  : %3.5f'   % (geo[3])

    geo = raster_dataset.GetGeoTransform()
    print 20 * '- '
    print 'Output raster info: %s' % basename(output_raster)
    print ' rows : %d'       % (raster_dataset.RasterXSize)
    print ' cols : %d'       % (raster_dataset.RasterYSize)
    print ' proj : %s'       % (raster_dataset.GetProjection())
    print ' xcell: %3.5f'   % (geo[1])
    print ' ycell: %3.5f'   % (geo[5])
    print ' ulx  : %3.5f'   % (geo[0])
    print ' uly  : %3.5f'   % (geo[3])
    print 20 * '- '



if __name__ == '__main__':

    # define and parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='the input shapefile that will be rasterized')
    parser.add_argument('-r', '--raster', required=True, help='base raster that will be used to align the rasterized vector file.')
    parser.add_argument('-o', '--output', required=True, help='the detination of the rasterized output (GTIFF).')
    args = parser.parse_args()

    if exists(args.output):
        response = raw_input('Output file already exists.  Do you want to delete it? [Y/n] ')
        if response != 'n':
            os.remove(args.output)


    rasterize_and_align(args.input, args.raster, args.output)

    print 'Rasterization and alignment completed successfully'
