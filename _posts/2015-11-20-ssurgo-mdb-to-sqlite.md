---
title: Extending the SSURGO SQLite database
layout: post
---
{::options parse_block_html="true" /}


In my previous post I demonstrated how the SSURGO soil dataset can be converted from a Microsoft Access (*.mdb) file into a platform indepedent SQLite format. This post extends the previous example to build a SQLite soil database from a directory of SSURGO *.mdb files.

The following bash script loops over the all *.mdb files in the current directory and performs the following:

<!--break-->

1. Use the database schema of the first *.mdb file to build the SQLite database tables.

2. For each *.mdb file, dump their data into a single SQLite database.

3. Send any error messages to a stderr.log file

To use this following script, place all SSURGO *.mdb files in a single directory along with the script below (make sure the script has execute privileges).  Execute the script using the following command:



    ./convert2sqlite.sh my-empty-sqlite-file.sqlite


`convert2sqlite.sh` :

    #!/usr/bin/env bash


    COUNTER=1

    for f in *.mdb; do
        echo "Processing file $f..."

        if [ $COUNTER -eq 1 ]; then
            echo "Extracting the database schema";
            mdb-schema $f postgres \
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
            sqlite3 $1<create.sql 2>>stderr.log
        fi
    
        # dump the mdb tables and load into database
        echo "BEGIN;">import-data.sql
    
        # Export each table and replace nan and inf with NULL
        for table in `mdb-tables $f`
        do 
            mdb-export -I sqlite $f $table 2>>stderr.log 1>>import-data.sql
        done
    
        echo "COMMIT;">>import-data.sql
    
        # Import data to sqlite3
        sqlite3 $1<import-data.sql 2>>stderr.log

        # increment the file counter
        COUNTER=$((COUNTER+1))
    done

<hr>
