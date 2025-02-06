#!/usr/bin/env python3
"""
Habit Tracking App
==================

This application implements a basic habit tracking backend using object-oriented
and functional programming in Python. It provides the ability to add habits, record
check-ins, update streaks, and perform analytics on the tracked habits. The app
uses JSON for data persistence and Click for the command-line interface.
"""

import click
import json
import os
from datetime import datetime, timedelta

# =================================
# Helper Functions for Date Handling
# =================================

def datetime_to_str(dt):
    """Convert a datetime object to an ISO-formatted string."""
    return dt.isoformat()

def datetime_from_str(s):
    """Convert an ISO-formatted string back to a datetime object."""
    return datetime.fromisoformat(s)

# =================================
# User and Habit Classes
# =================================

class User:
    """
    Represents a user with a list of habits.
    """
    def __init__(self, name, user_id=0, habits=None):
        self.user_id = user_id
        self.name = name
        self.habits = habits if habits is not None else []

    def add_habit(self, habit):
        """Add a habit to the user."""
        self.habits.append(habit)

    def delete_habit(self, habit_id):
        """Delete a habit from the user's list by habit_id."""
        self.habits = [habit for habit in self.habits if habit.habit_id != habit_id]

    def to_dict(self):
        """Serialize the user and its habits to a dictionary."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'habits': [habit.to_dict() for habit in self.habits]
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a dictionary into a User object."""
        habits = [Habit.from_dict(h) for h in data.get('habits', [])]
        return cls(data['name'], data.get('user_id', 0), habits)

class Habit:
    """
    Represents a habit with a name, periodicity, check-in history, and streak tracking.
    
    Periodicity is a tuple (frequency, period_in_days), e.g.:
      - Daily habit: (1, 1)
      - Weekly habit: (1, 7)
      - Special habit: (x, y) meaning x times every y days.
    """
    _id_counter = 0

    def __init__(self, name, periodicity, creation=None, habit_id=None):
        if habit_id is None:
            self.habit_id = Habit._id_counter
            Habit._id_counter += 1
        else:
            self.habit_id = habit_id
            if habit_id >= Habit._id_counter:
                Habit._id_counter = habit_id + 1

        self.name = name
        self.periodicity = periodicity  # (frequency, period)
        self.frequency = periodicity[0]
        self.period = periodicity[1]
        self.history = []  # List of datetime objects for check-ins
        self.streak = 0
        self.longest_streak = 0
        self.creation = creation if creation is not None else datetime.today()

    def check_in(self, checkin_datetime=None):
        """Record a check-in for the habit."""
        if checkin_datetime is None:
            checkin_datetime = datetime.today()
        self.history.append(checkin_datetime)
        self.history.sort()

    def update_streak(self, update_time=None):
        """
        Update the current and longest streak based on the habit's check-in history.
        Uses the latest check-in as the reference point.
        
        Args:
            update_time (datetime, optional): A reference time. If provided and it is
                earlier than the latest check-in, that value is used; otherwise, the
                latest check-in time is used.
        """
        if not self.history:
            self.streak = 0
            return

        # Use the latest check-in as reference
        last_checkin = max(self.history)
        reference = update_time if (update_time is not None and update_time < last_checkin) else last_checkin
        
        period_length = timedelta(days=self.period)
        count = 0
        end_period = reference
        start_period = end_period - period_length

        while True:
            checkins = [dt for dt in self.history if start_period <= dt <= end_period]
            if len(checkins) >= self.frequency:
                count += 1
                end_period = start_period
                start_period = end_period - period_length
            else:
                break

        self.streak = count
        if self.streak > self.longest_streak:
            self.longest_streak = self.streak

    def to_dict(self):
        """Serialize the habit to a dictionary."""
        return {
            'habit_id': self.habit_id,
            'name': self.name,
            'periodicity': list(self.periodicity),  # Convert tuple to list for JSON compatibility
            'history': [datetime_to_str(dt) for dt in self.history],
            'streak': self.streak,
            'longest_streak': self.longest_streak,
            'creation': datetime_to_str(self.creation)
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a dictionary into a Habit object."""
        habit = cls(
            name=data['name'],
            periodicity=tuple(data['periodicity']),
            creation=datetime_from_str(data['creation']),
            habit_id=data['habit_id']
        )
        habit.history = [datetime_from_str(s) for s in data.get('history', [])]
        habit.streak = data.get('streak', 0)
        habit.longest_streak = data.get('longest_streak', 0)
        return habit

    def __str__(self):
        return (f"[{self.habit_id}] {self.name} "
                f"(Periodicity: {self.periodicity[0]} time(s) every {self.periodicity[1]} day(s))")

# =================================
# Data Persistence Functions
# =================================

DATA_FILE = "data.json"

def save_data(user, filename=DATA_FILE):
    """Save the user data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(user.to_dict(), f, indent=4)

def load_data(filename=DATA_FILE):
    """Load the user data from a JSON file."""
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        data = json.load(f)
        return User.from_dict(data)

# =================================
# Analytics Functions
# =================================

def analytics_all_current_habits(user):
    """Return all currently tracked habits for the user."""
    return user.habits

def analytics_habits_by_periodicity(user, periodicity):
    """Return habits that match the given periodicity."""
    return [habit for habit in user.habits if habit.periodicity == periodicity]

def analytics_longest_streak_all(user):
    """Return the longest streak among all the user's habits."""
    longest = 0
    for habit in user.habits:
        habit.update_streak()
        if habit.longest_streak > longest:
            longest = habit.longest_streak
    return longest

def analytics_longest_streak_for_habit(user, habit_id):
    """Return the longest streak for a specific habit."""
    for habit in user.habits:
        if habit.habit_id == habit_id:
            habit.update_streak()
            return habit.longest_streak
    return None

# =================================
# Command Line Interface (CLI) using Click
# =================================

@click.group()
def cli():
    """Habit Tracking App CLI."""
    pass

@cli.command()
def create_user():
    """Create a new user by prompting for a name."""
    name = click.prompt("Enter your name", type=str)
    user = User(name)
    save_data(user)
    click.echo(f"User '{name}' created.")

@cli.command()
def add_habit():
    """Add a new habit to the current user."""
    user = load_data()
    if not user:
        click.echo("No user found. Please create a user first.")
        return
    name = click.prompt("Enter the name of the new habit", type=str)
    click.echo("Select periodicity type:")
    click.echo("1: Daily (1 time every 1 day)")
    click.echo("2: Weekly (1 time every 7 days)")
    click.echo("3: Special (x times every y days)")
    option = click.prompt("Enter option (1/2/3)", type=int)
    if option == 1:
        periodicity = (1, 1)
    elif option == 2:
        periodicity = (1, 7)
    elif option == 3:
        frequency = click.prompt("Enter frequency (number of times)", type=int)
        period = click.prompt("Enter period in days", type=int)
        periodicity = (frequency, period)
    else:
        click.echo("Invalid option.")
        return
    habit = Habit(name, periodicity)
    user.add_habit(habit)
    save_data(user)
    click.echo(f"Habit '{name}' added with ID {habit.habit_id}.")

@cli.command()
def list_habits():
    """List all habits for the current user."""
    user = load_data()
    if not user:
        click.echo("No user found.")
        return
    if not user.habits:
        click.echo("No habits found.")
        return
    for habit in user.habits:
        habit.update_streak()
        click.echo(str(habit))

@cli.command()
def check_in():
    """Record a check-in for a habit."""
    user = load_data()
    if not user:
        click.echo("No user found.")
        return
    if not user.habits:
        click.echo("No habits to check in.")
        return
    habit_id = click.prompt("Enter habit ID to check in", type=int)
    found = False
    for habit in user.habits:
        if habit.habit_id == habit_id:
            habit.check_in()
            habit.update_streak()
            save_data(user)
            click.echo(f"Checked in for habit '{habit.name}'.")
            found = True
            break
    if not found:
        click.echo("Habit not found.")

@cli.command()
def edit_habit():
    """Edit a habit: check in, change periodicity, or delete it."""
    user = load_data()
    if not user:
        click.echo("No user found.")
        return
    if not user.habits:
        click.echo("No habits to edit.")
        return
    habit_id = click.prompt("Enter habit ID to edit", type=int)
    habit = next((h for h in user.habits if h.habit_id == habit_id), None)
    if not habit:
        click.echo("Habit not found.")
        return
    click.echo(f"Editing habit: {habit}")
    click.echo("1: Check in")
    click.echo("2: Change periodicity")
    click.echo("3: Delete habit")
    option = click.prompt("Select an option", type=int)
    if option == 1:
        habit.check_in()
        habit.update_streak()
        click.echo(f"Checked in for habit '{habit.name}'.")
    elif option == 2:
        click.echo("Select new periodicity type:")
        click.echo("1: Daily (1 time every 1 day)")
        click.echo("2: Weekly (1 time every 7 days)")
        click.echo("3: Special (x times every y days)")
        option2 = click.prompt("Enter option (1/2/3)", type=int)
        if option2 == 1:
            habit.periodicity = (1, 1)
        elif option2 == 2:
            habit.periodicity = (1, 7)
        elif option2 == 3:
            frequency = click.prompt("Enter frequency (number of times)", type=int)
            period = click.prompt("Enter period in days", type=int)
            habit.periodicity = (frequency, period)
        else:
            click.echo("Invalid option.")
            return
        habit.frequency = habit.periodicity[0]
        habit.period = habit.periodicity[1]
        click.echo(f"Periodicity updated for habit '{habit.name}'.")
    elif option == 3:
        user.delete_habit(habit_id)
        click.echo(f"Habit '{habit.name}' deleted.")
    else:
        click.echo("Invalid option.")
        return
    save_data(user)

@cli.command()
def analytics():
    """Open the analytics module to view various habit statistics."""
    user = load_data()
    if not user:
        click.echo("No user found.")
        return
    click.echo("Analytics Options:")
    click.echo("1: List all tracked habits")
    click.echo("2: List habits by periodicity")
    click.echo("3: Longest streak among all habits")
    click.echo("4: Longest streak for a given habit")
    option = click.prompt("Select an option", type=int)
    if option == 1:
        for habit in analytics_all_current_habits(user):
            habit.update_streak()
            click.echo(str(habit))
    elif option == 2:
        click.echo("Select periodicity type:")
        click.echo("1: Daily (1,1)")
        click.echo("2: Weekly (1,7)")
        click.echo("3: Special (x,y)")
        option2 = click.prompt("Enter option", type=int)
        if option2 == 1:
            periodicity = (1, 1)
        elif option2 == 2:
            periodicity = (1, 7)
        elif option2 == 3:
            frequency = click.prompt("Enter frequency (number of times)", type=int)
            period = click.prompt("Enter period in days", type=int)
            periodicity = (frequency, period)
        else:
            click.echo("Invalid option.")
            return
        for habit in analytics_habits_by_periodicity(user, periodicity):
            habit.update_streak()
            click.echo(str(habit))
    elif option == 3:
        longest = analytics_longest_streak_all(user)
        click.echo(f"Longest streak among all habits: {longest}")
    elif option == 4:
        habit_id = click.prompt("Enter habit ID", type=int)
        longest = analytics_longest_streak_for_habit(user, habit_id)
        if longest is not None:
            click.echo(f"Longest streak for habit ID {habit_id}: {longest}")
        else:
            click.echo("Habit not found.")
    else:
        click.echo("Invalid option.")

@cli.command()
def delete_user():
    """Delete the current user's data (removes the data file)."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        click.echo("User data deleted.")
    else:
        click.echo("No user data to delete.")

if __name__ == "__main__":
    cli()
