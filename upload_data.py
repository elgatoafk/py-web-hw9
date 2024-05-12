from constants import *
from mongoengine import connect
from models import Authors, Quotes
import json

connect(host=f"""mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{DOMAIN}/
        {DB_NAME}?retryWrites=true&w=majority""", ssl=True)


def load_authors():
    with open("authors.json", "r", encoding="utf-8") as f:
        authors = json.load(f)

    for author in authors:
        Authors(name=author["fullname"], born_date=author["born_date"], 
                born_location=author["born_location"], 
                description=author["description"] ).save()


def load_quotes():
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes = json.load(f)
        
    author_name = quotes["author"]
    author = Authors.objects(name=author_name).first()
    if not author:
        author = Authors(name=author_name, born_date="", born_location="", description="")
        author.save()
    Quotes(tags=quotes["tags"], author=author, quote=quotes["quote"]).save()


if __name__ == "__main__":
    load_authors()
    load_quotes()
    print("All done")