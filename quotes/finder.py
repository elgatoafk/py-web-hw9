from constants import *
from models import Authors, Quotes, Tag

def search_quotes(command):
    parts = command.split(":")
    if len(parts) != 2:
        return "Invalid command format"
    
    field, value = parts[0].strip(), parts[1].strip()

    if field.lower() == "name":
        author = Authors.objects(name=value).first()
        if author:
            quotes = Quotes.objects(author=author)
            return [quote.quote for quote in quotes]
        else:
            return "Author not found"
    elif field.lower() == "tag":
        quotes = Quotes.objects(tags__name=value)
        return [quote.quote for quote in quotes]
    elif field.lower() == "tags":
        tag_names = value.split(",")
        quotes = Quotes.objects(tags__name__in=tag_names)
        return [quote.quote for quote in quotes]
    else:
        return "Invalid command"


    
def main():
    while True:
        command = input("Enter command: ")
        if command.lower() == "exit":
            print("Exiting the program.")
            break
        
        result = search_quotes(command)
        if isinstance(result, list):
            print("Quotes found:")
            for quote in result:
                print("-", quote)
        else:
            print("Error:", result)

if __name__ == "__main__":
    main()
    
