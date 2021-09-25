from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
from textblob import TextBlob
import re



spark = SparkSession.builder\
    .master("local[*]")\
    .appName("NLP")\
    .getOrCreate()

schemaList= "sr string, id string, address string, name string, online_order string, book_table string, rate string, votes string, location string, rest_type string, cuisines string, cost_for_two string,  reviews_list string, restaurant_type string, latitude string, longitude string"

df = spark.read \
    .option("delimiter","^")\
    .option("header","true")\
    .schema(schemaList)\
    .csv("file:///home/pratik/Desktop/BigData/project/coord_caret")


def polarity_score(text):
    return TextBlob(text).sentiment.polarity

polarity_detection = udf(polarity_score,StringType())

def review_clean(text):
    r = re.sub("[^a-zA-Z .']", " ", text)
    r = r.replace("'Rated  . '  'RATED   ", "")
    r = r.replace("'Rated  . '   RATED   ", "")
    r = r.replace("Rated  . '  RATED   ", "")

    r = str(r)
    return r

review_udf = udf(review_clean,StringType())



result = df\
    .select("sr","name",explode(split("reviews_list","\)")).alias("review"))\
    .withColumn("review_clean",review_udf("review"))\
    .drop("review")\
    .withColumn("polarity",polarity_detection("review_clean"))\
    .selectExpr("sr","name","CAST(polarity as DOUBLE)")\
    .groupBy("sr","name")\
    .avg("polarity")


# df.show(n=10,truncate=False)


result.coalesce(1).write.option("sep","^").csv("file:///home/pratik/Desktop/BigData/project/output4")


spark.stop()


