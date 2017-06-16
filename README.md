## Data Analyst Nanodegree Open Street Map Project

Download and clean an OpenStreetMap XML file and generate csv files for upload
into a database.  Once loaded into the database, explore and create a report of
the findings.

[Project Rubric](https://review.udacity.com/#!/rubrics/25/view)

### prep_for_database.py

This file was provided from the course lessons and uses Python 2.7.  It was modified by completing
the `shape_element` function.  Additional helper functions where added to
support `shape_element`.

The following csv files are generated as result of running the `prep_for_database.py` script.

1. nodes.csv
2. nodes_tags.csv
3. ways.csv
4. ways_nodes.csv
5. ways_tags.csv

These files are imported into a MySQL database containing tables with the same
names as the csv files.  See the **open_map_project_schema.sql** file in this
repository for details on the tables.

See the **open_street_map_project.pdf** for a description of what tasks were
performed.
