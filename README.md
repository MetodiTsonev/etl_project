# ETL Project

This project is an ETL pipeline built using Scrapy and FastAPI. The pipeline scrapes articles from two sources and stores them in an SQLite database. The FastAPI application provides an API to interact with the scraped data.


## Setup Instructions

### Prerequisites

- Python 3.10 or later
- SQLite3

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd etl_project

2. Create a virtual env:
   ```bash
   python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

4. Create the database:
   ```bash
   python utils/create_database.py

5. Navigate to the spiders and run them:
   ```bash
   cd etl_project/etl_project
   scrapy crawl restofworld_spider
   scrapy crawl capitalbrief_spider

6. Navigate back to the root directory:
   ```bash
   cd ../..

7. Start the FastAPI:
   ```bash
   uvicorn utils.main:app --reload

## API Endpoints

### GET /articles/?page={n}
Get all crawled articles and their properties paginated by size 5.

### GET /articles/?date={date}
Get a list of articles from the specified date.

### GET /articles/?author={author}
Get a list of articles with the same author.

### GET /article/{article_UID}
Get a single article by its UID.

### POST /article/{article_UID}
Create an article by providing the details in the message body.

### DELETE /article/{article_UID}
Delete a single article by its UID.

### PUT /article/{article_UID}
Update a single article by providing the details in the message body.

## Examples

### Using Postman

#### POST /article/{article_UID}
- URL: `http://127.0.0.1:8000/article/100`
- Method: `POST`
- Body:
    ```json
    {
        "author": "New Author",
        "title": "New Title",
        "publication_date": "2024-05-21",
        "url": "http://new-url.com",
        "images": ["http://image1.com", "http://image2.com"],
        "body": ["Paragraph 1", "Paragraph 2"]
    }
    ```

#### PUT /article/{article_UID}
- URL: `http://127.0.0.1:8000/article/100`
- Method: `PUT`
- Body:
    ```json
    {
        "author": "Updated Author",
        "title": "Updated Title",
        "publication_date": "2024-05-21",
        "url": "http://updated-url.com",
        "images": ["http://image1.com", "http://image2.com"],
        "body": ["Updated paragraph 1", "Updated paragraph 2"]
    }
    ```
