# FastAPI Songs API

This project is a FastAPI-based REST API for managing songs, with endpoints to upload song data, retrieve songs, search for songs by title, and rate songs. The backend is powered by SQLAlchemy and MySQL, with Alembic for database migrations. The project also includes automated testing using pytest.

## Features

- **Upload JSON data**: Upload a JSON file containing song data.
- **Retrieve all songs**: Retrieve a paginated list of all songs.
- **Search for a song**: Search for a song by its title.
- **Rate a song**: Rate a song by its ID.
- **Database migrations**: Manage schema changes using Alembic.
- **Automated testing**: pytest-based tests for all endpoints and database operations.

## Project Structure

```plaintext

.
├── alembic
│   ├── versions
│   └── env.py
├── app
│   ├── api
│   │   └── v1
│   │       └── endpoints.py
│   ├── core
│   │   └── config.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── crud.py
│   └── schemas.py
├── tests
│   ├── test_endpoints.py
├── static
│   ├── css
│   │   └── styles.css
│   ├── js
│   │   ├── scripts.js
│   │   └── search.js
│   └── templates
│       ├── upload.html
│       ├── songs.html
│       ├── landing_page.html
│       └── search_song.html
├── .env
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

* Python 3.9+
* MySQL 5.7+

### Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/patel-dhaval/vivpro.git
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Create a .env file in the root directory:

```bash
touch .env
```

Add the following to the .env file:

```bash
DATABASE_URL=mysql+pymysql://your_user:your_password@localhost/your_database
```

5. **Setup the database:**

- **Create the database:**

```sql
CREATE DATABASE your_database;
```
- **CRun database migrations:**

```bash
alembic upgrade head
```

### Running the Application

To start the FastAPI application, run:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.


### API Endpoints

- **Upload JSON data: POST /api/v1/upload-json/**
- **Retrieve all songs: GET /api/v1/songs/**
- **Search for a song by title: GET /api/v1/songs/{title}**
- **Rate a song by ID: PUT /api/v1/songs/{song_id}/rate**


### Running Tests


To run the tests using pytest, refer above for step 5, create a new database, update the connection url in both .env and alembic.ini file, run migrations and execute the below:

```bash
pytest
```

### Troubleshooting

- **MySQL Connection Issues:**
    - Ensure your .env file is correctly configured and that MySQL is running.

- **Migrations Not Working:**
  - Make sure Alembic is correctly set up and the database URL is correct.

- **Tests Failing Due to Database State:**
  - Ensure that the test database is correctly set up and that tables are being created and dropped correctly between tests.


### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

- FastAPI
- SQLAlchemy
- Alembic
- pytest