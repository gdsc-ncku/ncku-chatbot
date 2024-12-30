# NCKU Chatbot Linebot

## Usage

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