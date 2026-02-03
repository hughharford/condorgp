REF:
****
all very well, but creating the hive table didn't work, so here is my adjusted "ignore hive" version

https://www.dremio.com/subsurface/migrating-a-hive-table-to-an-iceberg-table-hands-on-tutorial/


START DOCKER:
*************
docker run -it --name iceberg-env alexmerced/iceberg-starter 


COMMAND TO RUN SPARK FIRST:
***************************
don't bother with hive tables, just run on iceburg from the off


spark-shell --packages org.apache.iceberg:iceberg-spark3-runtime:0.13.0\
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
    --conf spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkSessionCatalog \
    --conf spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog
    
RUN A SET OF SAMPLE DATABASE COMMANDS:
**************************************
using parquet filetype as good for big storage

spark.sql("CREATE TABLE people (first_name string, last_name string) USING parquet");
