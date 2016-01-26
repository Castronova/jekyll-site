---
title: Rasterizing GIS Layers
layout: post
---
{::options parse_block_html="true" /}

ArcMap has a tool for converting vector layers to raster datasets `FeatureToRaster` that generally works pretty well.  Unfortunately, if you need your rasterized layer to align with existing rasters, i.e. same cellsize and same extent, this tool becomes a headache. ArcMap provides a tool for aligning rasters, but it doesn't work!  There are a bunch of posts regarding this topic: [ex1](http://gis.stackexchange.com/questions/34085/how-can-i-align-two-non-coincident-equi-resolution-raster-grids), [ex2](https://geonet.esri.com/thread/98483), [ex3](http://gis.stackexchange.com/questions/43437/how-to-align-two-rasters-of-exact-same-cell-size-extent-in-arcgis-desktop).  After wasting too much time searching for a working solution in ArcMap, I decided to use gdal instead.

**Problem**

How can I convert a vector layer into a raster and exactly align the cells with an existing raster?  If we try to do this using a naive approach (using ArcMap) by (1) converting the vector layer to a raster and (2) clipping it to the extent of our existing raster layer, we end up with something like this:

<p align="center">
![unaligned_rasters]({{site.baseurl}}/img/unaligned_rasters.png){:height="300" width="300"}
</p>

Where the converted vector file is shown is yellow/green and the existing raster is shown in blue.  As you can see, the cells do not align perfectly which may cause errors in data processing, especially if performing element-wise calculations.

---

**Solution 1**

The first way to fix this problem is to directly leverage gdal from the terminal.  To check if you have gdal installed (or osgeo), open your terminal and type `gdalwarp`.  You should see output similar to this: 


<p align="center">
![check_gdal_using_terminal]({{site.baseurl}}/img/check_gdal_terminal.png)
</p>

First, extract attributes of the target raster dataset using `gdalinfo`. This command will display lots of metadata about the dataset that is provided as input.  In our case we are interested in the extent and cell size of the target raster (i.e. the raster that we want to align the vector dataset on)

    $ gdalinfo my_raster_dataset


<p align="center">
![execute_gdal_info]({{site.baseurl}}/img/gdalinfo.png)
</p>


Now that we know our target cell size we can convert our vector layer into a raster grid using `gdal_rasterize`, where `tr` designates the target x and y cellsize, `my_attribute_name` is the name of the attribute that will be represented in the output raster, `my_shape_file` is the input vector layer, and `rasterized.tif` is the output rasterized layer.

    gdal_rasterize -tr 35.02423028 35.02423028 -of GTiff -a my_attribute_name my_shapefile.shp rasterized.tif


Finally, we need to take our `rasterized.tif` and align it with our target raster.  Note that target extent `-te` and target resolution `-tr` are taken from the `gdalinfo` command above.

    gdalwarp -te 490323.808772045 1178632.03998184 493090.722964553 1181714.17224691 -tr 35.02423028 35.02423028 rasterized.tif aligned.tif

The result of these steps should be perfectly aligned rasters.


---

**Solution 2**

While the solution above works well, this process can be further automated using Python and the `osgeo` library.  The following code was built and executed within an anaconda environment on OSX.  [download][1]

[1]:{{ site.url }}/files/align.py


    import os, sys
    import time
    import argparse
    from os.path import *
    from osgeo import ogr, gdal
    from multiprocessing import Process

    # set the GDA:_DATA environment variable assuming that it is relative to the anaconda executable
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
