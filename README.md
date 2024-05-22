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
