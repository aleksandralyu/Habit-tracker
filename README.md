# Habit Tracking App

A Python-based habit tracking application that allows users to define, track, and analyze their habits through a command-line interface (CLI). This project implements core functionality such as creating habits (daily, weekly, or special), recording check-ins, calculating streaks, and performing analytics—all while persisting data in a JSON file.

## Features

- **User & Habit Management:**
  - Create a user profile and add multiple habits.
  - Each habit is defined with a name, periodicity, and a unique ID.
  - Check in to record the completion of a habit.

- **Streak Tracking & Analytics:**
  - Automatically calculates current and longest streaks for each habit.
  - Provides analytics functions to list habits, filter by periodicity, and view streak information.

- **Data Persistence:**
  - Habit data is stored in a JSON file (`data.json`) to persist between sessions.

- **Command-Line Interface (CLI):**
  - Built using [Click](https://click.palletsprojects.com/), the CLI supports commands such as:
    - `create-user` to create a new user.
    - `add-habit` to add a habit.
    - `list-habits` to display current habits.
    - `check-in` to record a habit completion.
    - `edit-habit` to modify or delete a habit.
    - `analytics` to view habit statistics.
    - `delete-user` to remove user data.
    
- **Testing & Test Data:**
  - Includes a unit test suite (`test_app.py`) using Python's `unittest` framework.
  - A separate script (`user_data.py`) generates 4 weeks of sample data for testing purposes.

## Installation

1. **Clone the Repository:**

       git clone <your-github-repository-url>
       cd Habit-Tracker

2. **Set Up a Virtual Environment:**

       python3 -m venv .venv
       source .venv/bin/activate

3. **Install Dependencies:**

       python3 -m pip install --upgrade pip
       python3 -m pip install click

## Usage

The project is operated via the command line. Below are some example commands:

- **Create a User:**

       python3 final.py create-user

- **Add a Habit:**

       python3 final.py add-habit

- **List Habits:**

       python3 final.py list-habits

- **Record a Check-In:**

       python3 final.py check-in

- **Edit a Habit:**

       python3 final.py edit-habit

- **View Analytics:**

       python3 final.py analytics

- **Delete User Data:**

       python3 final.py delete-user

## Generating Test Data

To generate sample data covering 4 weeks with predefined habits, run:

       python3 user_data.py

This script creates a test user with 5 habits (including daily, weekly, and special habits) and populates the data with simulated check-ins for 28 days.

## Running Unit Tests

To ensure all functionality works as expected, run the unit tests with:

       python3 test_app.py

## Project Structure

- **final.py:** Main application file containing the CLI, core classes, and functionality.
- **user_data.py:** Script to generate sample/test data (4 weeks backlog).
- **test_app.py:** Unit test suite for the application.
- **data.json:** JSON file used for persisting user and habit data.
- **README.md:** This file.
- **.venv:** Virtual environment folder (if created locally).

## Documentation

- All functions and classes are documented using Python docstrings.
- The code is structured for readability and maintainability.


Developed by Aleksandra Lyubarskaja.


