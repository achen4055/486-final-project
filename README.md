# Project Setup Guide

This guide provides detailed instructions on how to set up and use the various components of our project. Follow these steps to ensure correct installation and operation.

## Initial Setup

### Retrieving Initial Data
- **Description**: Begin by retrieving the initial categories and text summaries which will serve as the foundation for model analysis and classification.
- **Steps**:
  1. Access the initial data source specified in the project documentation.
  2. Download or extract the data sets needed for the initial categories and summaries.

## Using Crawlers

### Running Crawlers
- **Prerequisites**:
  - Ensure that you have the necessary APIs installed to run the crawlers. For example, to install the MediaWiki API, use the following command:
    ```bash
    pip install mediawikiapi
    ```
- **Instructions**:
  1. Prepare a CSV file formatted according to the specifications in our source folder.
  2. To execute the review or summary crawlers, use the command line with appropriate argument(input file path) like:
    ```bash
     python3 reviews_crawler.py source/2009-2019_amazon_books.csv
    ```
  3. To execute the twitter crawlers, directly use the command line:
      ```bash
      python3 crawler_twitter.py
      ```

## Data Conversion

### Converting Text to JSON
- **Purpose**: Convert the TXT output from the crawlers into JSON format for later data processing.
- **Procedure**:
  1. Use the `txt_to_json.py` script to convert TXT files to JSON. Provide [input file path] and [type(summary or review)] in your command. For instance,
      ```bash
      python3 txt_to_json.py data_from_crawler/2020-2022summaries_Good_Read.txt summary
      ```

## Label Extraction

### Extracting Labels
- **Location**: Navigate to the `label extraction` folder within the project directory.
- **Usage**:
  1. Identify the appropriate script for your data source (e.g., `goodreads.py`, `google.py`, `twitter.py`).
  2. Prepare your data in the format required by the selected script and substitute the file name in the code.
  3. Run the script to extract labels. For example, to run the Goodreads label extraction script:
      ```bash
      python goodreads.py
      ```
- **Support**: Additional helper classes are available in the same folder to assist with the extraction process.

By following these instructions, you can effectively set up and use the project's tools for your data analysis and processing needs. If you encounter any problems, refer back to this guide and check the troubleshooting section in our documentation.
