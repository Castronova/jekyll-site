---
title: A more useful database for SSURGO
layout: post
---
{::options parse_block_html="true" /}

The SSURGO database contains detailed soil information for the contiguous US.  This database links soil components and their properties with map units using foreign key relationships.  Unfortunately, the choice to implement this data management system in Microsoft Access is an annoyance to everybody that chooses not to use Windows as their primary platform.  This post outlines an approach for extracting the SSURGO data into a platform independed RDBMS for analysis outside of Windows.  Unfortunately, this still requires some use of Windows to prepare the data, so if you are like me, you'll need to spin up a Windows virtual machine for a few minutes.

First we need to download the data and build the SSURGO Access database which means first navigating to the [GeoSpatial Data Gateway](https://gdg.sc.egov.usda.gov/GDGOrder.aspx) to download some data.  Navigate through the prompts to select a state, county, and data set (Soils -> Soil Survey Spatial and Tabular Data).  Once this data is downloaded and unzipped you will see a folder hierarchy like this.

![ssurgo folder structure]({{site.baseurl}}/img/ssurgo_unzipped.png) 

Next, we need to start up our Windows virtual machine and open the *.mdb file with Microsoft Access.  You will be prompted to provide the path the the SSURGO tabular data, and a macro will take over to construct and populate the database.  This is normally where we would add these data into ArcMap and start joining to other datasets, but we want to work outside of Windows today. Copy this *mdb file back onto your local machine (I'm using OSX, El Capitan).

Open your favorite terminal app and lets start hacking away.  First navigate to the folder containing your *.mdb file.

    cd ~/dev/mdb2sqlite

We need to install a library that will help use manipulate *mdb files outside of windows.

    brew install mdbtools

Next, lets create a simple script that will dump the schema and contents of our *.mdb file and load them into a SQLite database.  Create a file named `mdb2sqlite.sh` and paste the code below into it. Note: this process was adapted from [here](https://pnenp.wordpress.com/2011/02/10/converting-ms-access-mdb-files-to-sqlite-mdb2sqlite) .


    #!/bin/bash

    # Use temporary files for sql statements to ease debugging if something goes wrong

    # Export schema from mdb:
    mdb-schema $1 sqlite \
    | sed "s/Int8/INTEGER(8)/" \
    | sed "s/Int4/INTEGER(4)/" \
    | sed "s/Float8/FLOAT(8)/" \
    | sed "s/Float4/FLOAT(4)/" \
    | sed "s/Bool/BOOLEAN/" \
    | sed "s/Char /VARCHAR/" \
    | sed "s/DROP TABLE/DROP TABLE IF EXISTS/" \
    | grep -v "^--" \
    > create.sql

    # Import schema to sqlite3
    sqlite3 $2<create.sql

    # Delete old import data (adding to exising file later)
    # Vast speed improvement with BEGIN..COMMIT
    echo "BEGIN;">import-data.sql

    # Export each table and replace nan and inf with NULL
    for table in `mdb-tables $1`
    do
      mdb-export -I sqlite $1 $table >>import-data.sql
    done

    echo "COMMIT;">>import-data.sql

    # Import data to sqlite3
    sqlite3 $2<import-data.sql

Change the file execution permissions

    chmod +x mdb2sqlite.sh

We can run this script like this:

    ./mdb2sqlite.sh soildb_UT_2003.mdb soildb_UT_2003.sqlite

<hr>
More information about the SSURGO dataset can be found at [here](http://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/geo/?cid=nrcs142p2_053627http://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/geo/?cid=nrcs142p2_053627)
