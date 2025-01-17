# Bonphyre API

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description

This project is a Python-based API for a simple crowdfunding platform that provides endpoints where users can create, view, and contribute to
projects.

## Running the server (Native)

1. Clone the repository:
   ```sh
   git clone https://github.com/FrankE01/Bonphyre_Backend.git
   cd Bonphyre_Backend
   ```
2. Create and activate a virtual environment using [Poetry](https://python-poetry.org/):
   ```sh
   poetry shell
   ```
3. Install the dependencies:
   ```sh
   poetry install
   ```
4. Set up the environment variables:

   ```sh
   cp sample.env .env
   # Edit .env file with appropriate values
   ```

5. Start the API server:
   ```sh
   cd app
   python main.py
   ```
6. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Running the server (Docker)

1. Clone the repository:

   ```sh
   git clone https://github.com/FrankE01/Bonphyre_Backend.git
   cd Bonphyre_Backend
   ```

2. Set up the environment variables:

   ```sh
   cp sample.env .env
   # Edit .env file with appropriate values
   ```

3. Start the docker services:
   ```sh
   docker-compose up
   ```
4. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Running the tests

1. Run the test
   ```sh
   pytest
   ```
