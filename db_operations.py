import pymongo
from dotenv import dotenv_values

config = dotenv_values("pymongo.env")
myclient = pymongo.MongoClient(config["ATLAS_URI"])
print("hello")
print(myclient)
mydb = myclient[config["DB_NAME"]]


def insert_one_news(one_news):
    mycol = mydb["news"]
    x = mycol.insert_one(one_news)
    return x.inserted_id


def insert_multiple_news(news):
    for elem in news:
        insert_one_news(elem)