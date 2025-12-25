# Quickstart: Project Scaffolding

This guide provides the steps to get the backend and frontend servers running for the Local Voice Assistant project.

## Prerequisites

- Python 3.11+
- Node.js 20+
- `uv` (Python package installer)
- `npm` or `yarn` (Node.js package manager)

## Installation

1.  **Clone the repository**:
    ```bash
    git clone git@github.com:0h-n0/local-voice-assistant-gemini.git
    cd local-voice-assistant-gemini
    ```

2.  **Install Backend Dependencies**:
    Navigate to the backend directory and use `uv` to install the packages.
    ```bash
    cd backend
    uv pip install -r requirements.in
    ```

3.  **Install Frontend Dependencies**:
    Navigate to the frontend directory and use `npm` or `yarn`.
    ```bash
    cd ../frontend
    npm install
    # or yarn install
    ```

## Running the Application

1.  **Start the Backend Server**:
    From the `backend` directory:
    ```bash
    uvicorn src.main:app --reload
    ```
    The server will be running at `http://127.0.0.1:8000`. You can check the health status by visiting `http://127.0.0.1:8000/health`.

2.  **Start the Frontend Server**:
    From the `frontend` directory:
    ```bash
    npm run dev
    # or yarn dev
    ```
    The frontend development server will be running at `http://localhost:3000`.

You should now see the placeholder "Local Voice Assistant" page in your browser.
