from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
from textblob import TextBlob
import re



spark = SparkSession.builder\
    .master("local[*]")\
    .appName("NLP") \
    .master("local[*]")\
    .config("spark.executor.memory", "8g")\
    .config("spark.driver.memory", "6g")\
    .config("spark.memory.offHeap.enabled", "true")\
    .config("spark.memory.offHeap.size", "6g")\
    .config("spark.sql.shuffle.partitions", "800") \
    .getOrCreate()


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

def splt(text):
    if(len(text)>1):
        return text[0]
    else:
        pass

def splt1(text):
    if(len(text)>1):
        return text[1]
    else:
        pass


udf_split = udf(splt)
udf_split1 = udf(splt1)

df = spark.read\
    .json("file:///home/pratik/Desktop/BigData/project/coordjson.json")
df1 = df
    # .select(split("value","\[\('").alias("strings"))\
    # .select(udf_split("strings").alias("other"),udf_split1("strings").alias("review")).dropna()


review_udf = udf(review_clean,StringType())

# result = df1\
#     .select("other",explode(split("review","\)")).alias("review"))\
#     .withColumn("review_clean",review_udf("review"))\
#     .drop("review")\
#     .withColumn("polarity",polarity_detection("review_clean"))\
#     .where("polarity !=0.0")\
#     .selectExpr("other","review_clean","CAST(polarity as DOUBLE)")\
#     .groupby("other")\
#     .avg("polarity")


# result.coalesce(1).write.options(delimiter='^').csv("file:///home/pratik/Desktop/BigData/project/output")

df1.show(n=10, truncate=False)
spark.stop()

