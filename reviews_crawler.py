from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import csv


def close_popup_if_exists(driver):
    try:
        # Wait for the close button to be clickable
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))
        )
        # Click the button if it is found and clickable
        close_button.click()
    except TimeoutException:
        # If the close button is not found within 10 seconds, ignore the exception
        print("No close button found or it was not clickable within the timeout period.")

def get_book_reviews(book_title, f):
    # Set up the Selenium WebDriver
    # options = webdriver.ChromeOptions()
    # options.add_argument('--incognito')  # Use incognito mode to avoid cookies/pop-ups from past sessions
    # options.add_argument("--no-sandbox")  # Bypass OS security model
    # options.add_argument("--headless")  # Run in headless mode, useful if you don't need a GUI.
    # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    max_attempts = 5
    attempt = 0
    found = False
    book_review = "Retrieval fails"
    while attempt < max_attempts:
        try:
            # Set up the Selenium WebDriver
            options = webdriver.ChromeOptions()
            # options.add_argument('--incognito')  # Use incognito mode to avoid cookies/pop-ups from past sessions
            # options.add_argument("--no-sandbox")  # Bypass OS security model
            # options.add_argument("--headless")  # Run in headless mode, useful if you don't need a GUI.
            # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
            driver = webdriver.Chrome(options=options)

            # Open the search page on Goodreads
            driver.get(f'https://www.goodreads.com/search?q={book_title.replace(" ", "+")}')
        
            wait = WebDriverWait(driver, 10)
            book_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.bookTitle')))
            book_link = book_links[0].get_attribute('href')  # Get the href attribute of the first book title link
            driver.get(book_link)

            # Wait for the close button to be clickable and then click it
            close_popup_if_exists(driver)

            # Wait until the book description is loaded
            # Wait for the book description to load
            reviews = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "ReviewText__content")]'))

                # EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ReviewText")]'))
            )
            for i in range(0, len(reviews)):
                review_element = reviews[i]
                book_review = review_element.text
                index = book_review.find("Show more")  # redundant text
                if index != -1:
                    book_review = book_review[:index]
                print(i)
                print(i, file=f)
                print("book reviews: " + book_review, file=f)
                print(book_review)

            # print(book_review)
            found = True
            break

        except TimeoutException:
            attempt += 1
            print("The elements did not load in time.")

        except WebDriverException as e:
            attempt += 1
            print(f"An error occurred: {e}")

        except Exception as e:
            attempt += 1
            print(f"An error occurred: {e}")

    driver.quit()
    print(found)
    # return book_review

def main():

    # Check if at least one argument is provided
    # if len(sys.argv) < 2:
    #     print("Usage: python main.py folder_path")
    #     sys.exit(1)

    # folder_path = sys.argv[1]
    # python main.py cranfieldDocs/

    # Rest of your script goes here
    # print(f"Folder Path: {folder_path}")

    # (book name + summary) should also be a text
    year_book_dict = {}
    count = 0
    # Open the CSV file
    with open('2020-2022.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Extract the book name from the 'Name' column
            book_name = row['Name']
            book_year = row['Year']
            # Check if the year is already a key in the dictionary
            if book_year in year_book_dict:
                # If yes, append the book name to the existing list of books for that year
                year_book_dict[book_year].append(book_name)
            else:
                # If not, create a new key-value pair with the year and a list containing the book name
                year_book_dict[book_year] = [book_name]
            # print(year_book_dict)

    # Iterate over the dictionary
    # Open a file in write mode

    # years_to_remove = ['2016', '2011', '2018', '2017', '2019', '2014', '2010', '2009', '2015', '2013']

    # for year in years_to_remove:
    #     if year in year_book_dict:
    #         del year_book_dict[year]
    #     else:
    #         print(f"Year {year} not found in dictionary.")


    # count = 0
    with open('reviews2020.txt', 'w') as f:
        for year, books in year_book_dict.items():
            # Print the year
            print(f"Year: {year}")
            print("Year: " + year, file=f)
            # Iterate over the list of books for the current year
            for book in books:
                # Print each book name
                
                print("book name: " + book, file=f)
                get_book_reviews(book, f)
                # print("book reviews: " + review, file=f)
                print("-" * 40, file=f)  # Separator for readability
                # print(f" - {book}")
                # print(count)
                # count += 1

            # Add a newline for better readability
            print()
            # count += 1
            # if count == 3:
            #     break
            
            

    # Use the function with the desired book title
    # summary = get_book_summary('Harry Potter and the Chamber of Secrets: The Illustrated Edition (Harry Potter, Book 2)')
    # summary = get_book_summary('The Great Gatsby')
    # print(summary)



    # for filename in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, filename)

    #     # Read the file with ISO-8859-1 encoding
    #     with open(file_path, 'r', encoding='ISO-8859-1') as file:
    #         content = file.read()
    #         print(f"File: {filename}")
    #         # print("Tokens:", tokens)
    #         # print("-" * 30)

if __name__ == "__main__":
    main()