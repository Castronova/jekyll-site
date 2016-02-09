---
title: Speeding up DateTime Conversions
layout: post
---
{::options parse_block_html="true" /}

I have run into an issue recently when attempting to convert Python datetime objects into a specific string format.  While this is a simple task, it becomes computationally expensive to perform a string formatting operation on large datasets. Unfortunately, there is no way to side-step these conversions since I want to insert these data into a SQLite file database ([see doc](https://www.sqlite.org/lang_datefunc.html)). This is the naive code:

    def strftime_iter_looping(dt_list):
        # iterate through a large list of datetime objects using the built-in list iterator
        # use the datetime string formatting function to convert into SQLite format
        conv = []
        for dt in dt_list:
            conv.append(dt.strftime('%Y-%m-%d %H:%M:%S.%f'))
        return conv

<!--break-->


For a list of 100000 elements, this function takes 1.75 seconds (average of 5 runs).  This will become prohibitively slow as the size of the input data increases.  The following function offers a slight speedup:

    def strftime_comprehension(dt_list):
        conv = [d.strftime('%Y-%m-%d %H:%M:%S.%f') for d in dt_list]
        return conv

List comprehension provides a small amount of speedup (1.70 sec), however this is still not acceptable.  The lack of speedup between these two cases implies that the `datetime.strftime()` function is the culprit, rather than the looping technique.  We can replace this function call with a simple string conversion (which just happens to produce the desired string formatting)

    def strftime_str(dt_list):
        conv = [str(d) for d in dt_list]
        return conv

For a list of 100000 elements, this function takes 0.48632 seconds, which is a speedup of approximately 3.5x!

