---
title: ArcMap Data Import Troubles
layout: post
---
{::options parse_block_html="true" /}

I've recently come across an annoying ArcMap issue when working with a student to join some data (stored as *.txt) to a vector shapefile.  When the data is loaded, ArcMap parses the values and tries to assign correct data types to each of the columns.  This is usually not an issue, except when encoding numeric ids as strings.  For instance, numbers with leading zeros such as`01234` are truncated to `1234` when converted into a numeric datatype. This causes much pain and suffering...fortuntaly there is a simple fix.


<!--break-->

1. Create a text file with your data in it (e.g. `data.txt`)

    
        id,value1,value2  
        1,1000,2000  
        2,2000,3000  
        3,3000,4000

2. Create an empty text file called `schema.ini` in the same directory as your *.txt data file.  In this file we can assign specific data types for out columns.
The format is:

    **Row1:** `[filename.txt]`

    **Row2:** `Col`+*column_number*`=`*column_name* *data_type* 

    For example:

        [data.txt]
        Col1=id Text

3. Load the data.txt file into ArcMap, open the attribute table and verify that the column data types are correct.


![arcmap_datatype_inspection]({{site.baseurl}}/img/arcmap_datatable.png)

<hr>
