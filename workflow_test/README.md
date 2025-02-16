# Workflow (Agent) Test

This repo is for testing the Dify Workflow.

## Usage

1. Go to [Google Developer Console](https://console.cloud.google.com/), create a project, and enable the Google Drive API.
2. Download the credentials for the Drive API and save it as `credentials.json`.
3. Use poetry to create and manage your virtual environment.
    ```bash
    poetry env use 3.12
    poetry install
    ```
4. Run the service
    ```bash
    poetry run python main.py
    ```
5. Go to browser and go to `http://localhost:8000/docs`
6. Enter Your Google Drive Folder ID