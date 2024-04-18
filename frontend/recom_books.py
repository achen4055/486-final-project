

# Get most relevant + popular books, each with n results

# given the txt version of labels
# run python3 recom_books.py
# generate the books_json, which will be displayed in the front end.



import requests
import json

api_key = "GOOGLE_API_KEY"



# Given 10 possible categories
def read_10_categories(file_name):
    categories = []
    with open(file_name, 'r') as file:
        data = file.read()
        categories = data.split("\n")
    return categories




# volume_info = item['volumeInfo']
# sale_info = item['saleInfo']
# title = volume_info['title']
# authors = volume_info.get('authors', [])
# published_date = volume_info['publishedDate']
# categories = volume_info.get('categories', [])
# isbn_13 = next((identifier['identifier'] for identifier in volume_info['industryIdentifiers'] if identifier['type'] == 'ISBN_13'), None)
# isbn_10 = next((identifier['identifier'] for identifier in volume_info['industryIdentifiers'] if identifier['type'] == 'ISBN_10'), None)



def construct_books_diction(results,num_books):

    # results['items'][:20]
    items = results['items'][:num_books]
    # print("the item is ",items)
    book_dict = {}
    for item in items:
        # print(item)
        # print("------")
        # break
        volume_info = item['volumeInfo']
        sale_info = item['saleInfo']
        title = volume_info['title']
        
        book_dict[title] = {}
        book_dict[title]['image'] = volume_info['imageLinks']
        book_dict[title]['authors'] = volume_info.get('authors', None)
        categories = volume_info.get('categories', [])
        # print(categories)
        book_dict[title]['categories'] = volume_info.get('categories', None)
        book_dict[title]['published_date'] = volume_info.get('publishedDate', None)
        price = sale_info.get('retailPrice', None)
        book_dict[title]['sale_price'] = price.get('amount', None) if price else None
        book_dict[title]['description'] = volume_info.get('description',None)
        
        # break
    return book_dict


def get_most_relevant_books(categories,api_key,num_books):
    all_category_books = {}
    for category in categories:

        
        # endpoint_url = "https://www.googleapis.com/books/v1/volumes?q=flowers&orderBy=newest&key="+api_key
        endpoint_url = "https://www.googleapis.com/books/v1/volumes?q=" + category + "&orderBy=newest&key="+api_key
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            results = response.json()
            if results:
                all_category_books[category] = construct_books_diction(results,num_books)
            else:
                return "No book found."
        else:
            print(response.status_code)
            print("Error:", response.status_code, response.text)
    return all_category_books
        

# all_category_books = get_most_relevant_books(categories,api_key)

categories = read_10_categories("result_cate.txt")
num_books = 10
# categories = ["flowers"]
all_category_books = get_most_relevant_books(categories,api_key,num_books)
# print(all_category_books)
for key, value in all_category_books.items():
    with open('./books_recommend.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(all_category_books, jsonfile, indent=4, ensure_ascii=False)
