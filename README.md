# Mkulima Connect

Mkulima Connect is a web application designed to connect farmers and buyers efficiently. Farmers can list their produce, and buyers can search and contact farmers directly. An admin panel allows for moderation by approving produce listings before they become public.

## Features

- User authentication for farmers, buyers, and admins
- Farmer dashboard to add and manage produce listings
- Buyer interface to search produce by category and county
- Buyer can send messages to farmers about produce listings
- Admin panel to approve produce listings before public availability
- Current market prices displayed on homepage with fallback to static data
- Responsive UI built with Bootstrap 5 and inline styles
- Secure password hashing and session management
- Input validation and error handling throughout the app
- Database migrations for schema management
- Dockerized for easy deployment
- Automated tests covering all main features

## Technology Stack

- Python 3.10
- Flask web framework
- SQLAlchemy ORM with SQLite database
- Flask-Migrate for database migrations
- Flask-Login for authentication management
- WTForms for form handling and validation
- Requests for external API calls
- Bootstrap 5 for frontend styling
- Pytest for testing

## Prerequisites

- Python 3.10 or higher installed locally
- Git (optional, for cloning the repo)
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository (or download the source code):

    `git clone https://github.com/yourusername/mkulima-connect.git`

2. Navigate to the project directory:

    `cd mkulima-connect`

3. Create a Python virtual environment and activate it:

    - On Unix/macOS:

        `python3 -m venv venv`
        `source venv/bin/activate`

    - On Windows (PowerShell):

        `python -m venv venv`
        `venv\Scripts\Activate.ps1`

4. Install dependencies:

    `pip install -r requirements.txt`

5. Set environment variables:

    Create a `.env` file in the project root, or set environment variables directly.

    Use `.env.example` as a template:

        SECRET_KEY=your_secret_key_here
        DATABASE_URL=sqlite:///mkulima_connect.db
        DEBUG=True

6. Initialize and upgrade the database:

    