import click
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


def getBooks(query):
    # Function to get the books from the API
    info = {}
    URL = "https://www.googleapis.com/books/v1/volumes?q="
    #with f-string we concatenates the URL with the query argument
    urlQuery = f'{URL}' + query
    result = requests.get(urlQuery)

    #assigns totalItems and items from the API call to a info object
    info['totalItems'] = result.json().get('totalItems')
    info['items'] = result.json().get('items')

    return info
    
def parseInfo(info):
    #returns specific book information

    book = {}
    attrs = ['title','authors','description','categories']

    for attr in attrs: 
        book[attr] = info.get(attr)
    return book
    
#Creates the command 
@click.command()
@click.argument('name')
def main(name):
    start  = time.time()
   
    # Displays all the information related with the query 
    info = getBooks(name) # Gets the books
    totalBooks = info.get("totalItems")
    books = info.get("items")
    # displays books that contains the query 
    click.echo(f'TOTAL OF BOOKS FOUND: {totalBooks}')
    click.echo("BOOKS FOUND: ")
    
    book_list = [book.get('volumeInfo') for book in books] # Para cada libro deveulve
    executor = ThreadPoolExecutor(100)
    result = list(executor.map(parseInfo,book_list))

    for book in result:
         click.echo(book)
         click.echo("****************************************")
         
    #Displays the first 10 books found
    # for count,book in enumerate(books, start=1):
    #     info = book.get('volumeInfo')
    #     click.echo(f'{count}-{parseInfo(info)}')
if __name__== "__main__":
    main()
