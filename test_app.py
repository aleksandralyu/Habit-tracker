#!/usr/bin/env python3
"""
Unit Tests for Habit Tracker
----------------------------
This test suite validates core functionality including habit creation,
check-ins, streak updates, serialization/deserialization, analytics functions,
and data storage/retrieval.
"""

import unittest
from datetime import datetime, timedelta
import os

# Importing the classes and functions from final.py
from final import User, Habit, save_data, load_data, analytics_all_current_habits, analytics_longest_streak_for_habit, analytics_longest_streak_all

class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        # Create a test user with an initial habit for each test
        self.user = User("Unit Test User")
        self.habit = Habit("Test Habit", (1, 1))
        self.user.add_habit(self.habit)
    
    def tearDown(self):
        # Remove the data file after each test to avoid side effects
        if os.path.exists("data.json"):
            os.remove("data.json")
    
    def test_add_habit(self):
        self.assertEqual(len(self.user.habits), 1)
        new_habit = Habit("Another Habit", (1, 7))
        self.user.add_habit(new_habit)
        self.assertEqual(len(self.user.habits), 2)
    
    def test_check_in(self):
        # Initially, the history should be empty
        self.assertEqual(len(self.habit.history), 0)
        now = datetime.now()
        self.habit.check_in(now)
        self.assertEqual(len(self.habit.history), 1)
        self.assertEqual(self.habit.history[0], now)
    
    def test_update_streak_daily(self):
        # For a daily habit, simulate 3 consecutive check-ins
        start = datetime(2025, 1, 1)
        self.habit.history = []  # Clear history
        for i in range(3):
            self.habit.check_in(start + timedelta(days=i))
        self.habit.update_streak(start + timedelta(days=3))
        self.assertEqual(self.habit.streak, 3)
        self.assertEqual(self.habit.longest_streak, 3)
    
    def test_update_streak_weekly(self):
        # Test a weekly habit with 3 check-ins (once per week)
        weekly_habit = Habit("Weekly Habit", (1, 7))
        start = datetime(2025, 1, 1)
        for i in range(3):
            weekly_habit.check_in(start + timedelta(days=i*7 + 1))
        weekly_habit.update_streak(start + timedelta(days=22))
        self.assertEqual(weekly_habit.streak, 3)
        self.assertEqual(weekly_habit.longest_streak, 3)
    
    def test_serialization(self):
        # Check that serializing and deserializing a habit retains its data
        test_time = datetime(2025, 1, 1, 12, 0)
        self.habit.check_in(test_time)
        self.habit.update_streak()
        habit_dict = self.habit.to_dict()
        habit_copy = Habit.from_dict(habit_dict)
        self.assertEqual(habit_copy.name, self.habit.name)
        self.assertEqual(habit_copy.periodicity, self.habit.periodicity)
        self.assertEqual(len(habit_copy.history), len(self.habit.history))
    
    def test_save_and_load_data(self):
        # Save the current user data and then load it back
        save_data(self.user)
        loaded_user = load_data()
        self.assertIsNotNone(loaded_user)
        self.assertEqual(loaded_user.name, self.user.name)
        self.assertEqual(len(loaded_user.habits), len(self.user.habits))
    
    def test_analytics_functions(self):
        # Add two more habits (a daily and a weekly one) for analytics testing
        daily_habit = Habit("Daily Habit", (1, 1))
        weekly_habit = Habit("Weekly Habit", (1, 7))
        self.user.add_habit(daily_habit)
        self.user.add_habit(weekly_habit)
        now = datetime(2025, 1, 1)
        daily_habit.check_in(now)
        weekly_habit.check_in(now)
        daily_habit.update_streak(now + timedelta(days=1))
        weekly_habit.update_streak(now + timedelta(days=8))
        
        all_habits = analytics_all_current_habits(self.user)
        self.assertIn(daily_habit, all_habits)
        
        longest_all = analytics_longest_streak_all(self.user)
        longest_for_daily = analytics_longest_streak_for_habit(self.user, daily_habit.habit_id)
        self.assertEqual(longest_for_daily, daily_habit.longest_streak)
        self.assertEqual(longest_all, max(habit.longest_streak for habit in self.user.habits))

if __name__ == "__main__":
    unittest.main()
