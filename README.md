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

API Endpoints
GET /: Returns a simple greeting.
GET /articles/: Returns a paginated list of articles.
GET /articles/by_date/: Returns articles published on a specific date.
GET /articles/by_author/: Returns articles written by a specific author.
GET /article/{article_UID}: Returns a single article by its ID.
POST /article/{article_UID}: Creates a new article with the specified ID.
DELETE /article/{article_id}: Deletes an article by its ID.
PUT /article/{article_id}: Updates an article by its ID.

Examples
Using Postman
POST /article/{article_UID}
URL: http://127.0.0.1:8000/article/100
Method: POST
Body:
{
    "author": "New Author",
    "title": "New Title",
    "publication_date": "2024-05-21",
    "url": "http://new-url.com",
    "images": ["http://image1.com", "http://image2.com"],
    "body": ["Paragraph 1", "Paragraph 2"]
}
PUT /article/{article_UID}
URL: http://127.0.0.1:8000/article/100
Method: PUT
Body:
{
    "author": "Updated Author",
    "title": "Updated Title",
    "publication_date": "2024-05-21",
    "url": "http://updated-url.com",
    "images": ["http://image1.com", "http://image2.com"],
    "body": ["Updated paragraph 1", "Updated paragraph 2"]
}
Notes
Ensure that the database is correctly set up and running before starting the API.
If you encounter any issues, check the logs and verify the database connection settings.
The provided examples assume the use of SQLite. For other databases, ensure the necessary drivers and configurations are set.
