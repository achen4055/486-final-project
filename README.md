# What’s in People’s Mind?

## Project Description

This project tackles the complex challenges Amazon booksellers face in leveraging market trends, driven by a vast array of ratings and reviews across multiple platforms. The core objective is to develop a dynamic recommendation system designed to help sellers effectively stock books that are likely to be in demand, thereby maximizing profitability.

### Overview
The solution harnesses data from various sources, including book summaries from Goodreads and Google Books, as well as trending words from social media. This data is aggregated and analyzed to identify emerging trends via specific keywords.

### System Design
The project involves creating a sophisticated classification system that categorizes books based on current trends. This is achieved by:
- **Data Collection:** Utilizing web-crawled data from social media and book summaries.
- **Text Preprocessing:** Removing common and stop words to clean the data.
- **Text Classification:** Employing the BART model for initial text classification to refine and determine the top ten relevant categories.

### Predictive Modeling
The identified categories are then used as input for the RoBERTa model to predict future book trends. This predictive mechanism is designed to continuously adapt to changing consumer preferences, ensuring that the recommendations remain relevant and timely.

### Objective
By implementing this system, Amazon booksellers can dynamically adjust their inventory to align with predicted bestsellers and consumer demand, optimizing stock levels and potentially increasing sales and profits through more accurate and data-driven decision-making.

### Challenge and future plan
We also plan to incorporate Goodreads reviews into our data processing framework. However, due to the substantial volume of review data, we encountered challenges with processing capacity, as standard GPUs were inadequate. This has prompted further considerations for optimizing data handling and processing to include these extensive datasets effectively.

This approach promises to transform the way books are sold on Amazon by integrating advanced machine learning techniques to forecast market dynamics effectively.

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

## Data Processing And Trend Prediction
- **Purpose**: Follow the algorithm in paper to find most popular ten words for every two year and predict trend categories.
- **Usage**: If you are using Colab, you can directly run the `data_processing.ipynb` in Colab. If you run the code on your local device, you may need to `pip install torch, transformers`. In both case, please make sure you have cuda deceive, otherwise, change the pipeline with `device = torch.device('cpu')` in processing part.
- **Output**: The output of data processing is stored in `final_label.txt`

## Recommendations && Data Display
- **Purpose**: Get recommmendations and display them in an user-friendly way.
- **Usage**: Given the top trend labels, you will need to save them in a "txt" file after running the Colab. Proceeding to the frontend folder, you put the txt file inside the folder. Then, run
      ```
      python3 recom_books.py
      ```
  It will default to recommend the most relative top 10 books for each trending label. After that, you just run python3 -m http.server 8000. If you specify the port 8000, you will need to go to the link  ``` "http://localhost:8000/show.html"  ``` and see the front-end page. The description about the book could be seen after clicking the description button.

  
  <img width="705" alt="image" src="https://github.com/achen4055/486-final-project/assets/87424645/78d139cb-6e5f-424a-8bd9-a86dd468a692">

