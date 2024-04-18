from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import csv
import sys


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

def get_book_summary(book_title):

    max_attempts = 5
    attempt = 0
    found = False
    book_summary = "Retrieval fails"
    while attempt < max_attempts:
        try:
            # Set up the Selenium WebDriver
            options = webdriver.ChromeOptions()
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
            description = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@data-testid, "description")]'))
            )
            book_summary = description.text  # Get the text of the description
            # redundant text
            index = book_summary.find("Show more")
            if index != -1:
                book_summary = book_summary[:index]

            print(book_summary)
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
    return book_summary

def main():

    input_file_path = sys.argv[1]

    year_book_dict = {}
    count = 0
    # Open the CSV file
    with open(input_file_path, newline='', encoding='utf-8') as csvfile:
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


    with open('summary_output.txt', 'w') as f:
        for year, books in year_book_dict.items():
            # Print the year
            print(f"Year: {year}")
            print("Year: " + year, file=f)
            # Iterate over the list of books for the current year
            for book in books:
                # Print each book name
                summary = get_book_summary(book)
                print("book name: " + book, file=f)
                print("book summary: " + summary, file=f)
                print("-" * 40, file=f)  # Separator for readability
                print(count)
                count += 1

            # Add a newline for better readability
            print()
            


if __name__ == "__main__":
    main()