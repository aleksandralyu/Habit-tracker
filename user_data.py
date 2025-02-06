#!/usr/bin/env python3
"""
Generate Test Data for Habit Tracker
-------------------------------------
This script creates a user with five predefined habits and simulates 4 weeks (28 days)
of check-in data for each habit. The habits include at least one daily and one weekly habit,
as well as two "special" habits. The resulting data is saved via the existing data storage
functions (using JSON) so that it can be used as a test fixture.
"""

from datetime import datetime, timedelta
from final import User, Habit, save_data  # Assumes final.py has your main code

def generate_test_data():
    # Create a new user for testing
    user = User("Test User")
    
    # Define a starting date 28 days ago from today
    start_date = datetime.today() - timedelta(days=28)
    
    # Habit 1: Daily habit "Brush Teeth" (1,1) with daily check-ins
    habit1 = Habit("Brush Teeth", (1, 1))
    for i in range(28):
        checkin_date = start_date + timedelta(days=i)
        habit1.check_in(checkin_date)
    
    # Habit 2: Daily habit "Exercise" (1,1) that misses one day every week
    habit2 = Habit("Exercise", (1, 1))
    for i in range(28):
        if i % 7 != 0:  # Skip every 7th day
            checkin_date = start_date + timedelta(days=i)
            habit2.check_in(checkin_date)
    
    # Habit 3: Weekly habit "Call Parents" (1,7) with one check-in per week
    habit3 = Habit("Call Parents", (1, 7))
    for i in range(0, 28, 7):
        # Offset a little to avoid hitting the exact period boundary
        checkin_date = start_date + timedelta(days=i + 1)
        habit3.check_in(checkin_date)
    
    # Habit 4: Special habit "Read Book" (3,7) requiring 3 check-ins per week
    habit4 = Habit("Read Book", (3, 7))
    for week in range(4):
        for j in range(3):  # 3 check-ins per week
            checkin_date = start_date + timedelta(days=week*7 + j)
            habit4.check_in(checkin_date)
    
    # Habit 5: Special habit "Meditate" (5,7) requiring 5 check-ins per week
    habit5 = Habit("Meditate", (5, 7))
    for week in range(4):
        # For each week, simulate check-ins on 5 days
        for j in range(5):
            checkin_date = start_date + timedelta(days=week*7 + j)
            habit5.check_in(checkin_date)
    
    # Add all habits to the user
    user.add_habit(habit1)
    user.add_habit(habit2)
    user.add_habit(habit3)
    user.add_habit(habit4)
    user.add_habit(habit5)
    
    # Update streaks for each habit (so analytics show the correct streaks)
    for habit in user.habits:
        habit.update_streak()
    
    # Save the test data to the JSON file (usually "data.json")
    save_data(user)
    print("Test data generated and saved to data.json")

if __name__ == "__main__":
    generate_test_data()
