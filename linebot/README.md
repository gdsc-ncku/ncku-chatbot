# NCKU Chatbot Linebot

## Usage

Make sure you have sqlite3 and redis installed on your system.

1. Copy `.env.example` to `.env` and replace the values with your own
    ```cli
    cp .env.example .env
    ```
2. Use poetry to create and manage your virtual environment.
    ```bash
    poetry env use 3.12
    poetry install
    ```
3. Run the service
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
