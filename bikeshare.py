"""
Simply program to show bike-sharing statistics.
Internally, the program uses title-case strings which is a bit unconventional,
but matches names returned by calendar.
It makes hard-coded assumptions about available months and cities.
"""

import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'}

# first month is empty as months are 1-indexed
CITIES = ['Chicago', 'New York City', 'Washington']
MONTHS = ['All'] + list(calendar.month_name)[1:7]
DAYS = ['All'] + list(calendar.day_name)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or leave empty to apply no month filter
        (str) day - name of the day of week to filter by leave empty to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = None
    while city is None:
        user_input = input(f'Enter first letters of city to show data for ({", ".join(CITIES)}): ').title()
        match = [city for city in CITIES if city.startswith(user_input)]
        if len(match):
            city = match[0]
            print(f'> Will show data for city: {city}')
        else:
            print('> I did not recognise the city name, please check spelling and try again...')

    month = None
    while month is None:
        user_input = input('Enter first letters of month (Janurary to June) or type "all" to select all months: ').title()
        match = [month for month in MONTHS if month.startswith(user_input)]
        if len(match) == 1:
            month = match[0]
            print(f'> Will show data for month(s): {month}')
            # convert to number

        elif len(match) > 1:
            print('> The month name is ambiguous, please type more letters and try again...')
        else:
            print('> I did not recognise the month name, please check spelling and try again...')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while day is None:
        user_input = input('Enter first letters of day or type "all" to select all days: ').title()
        match = [day for day in DAYS if day.startswith(user_input)]
        if len(match) == 1:
            day = match[0]
            print(f'> Will show data for week day(s): {day}')
            # convert to number
        elif len(match) > 1:
            print('> The day name is ambiguous, please type more letters and try again...')
        else:
            print('> I did not recognise the day name, please check spelling and try again...')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    month_i = MONTHS.index(month)  # type: ignore
    day_i = DAYS.index(day) - 1  # type: ignore
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['year'] = df['Start Time'].dt.year
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    if 'Birth Year' in df.columns:
        df['age'] = df.year - df['Birth Year']
    if month != 'All':
        df = df.query('month == @month_i')
    if day != 'All':
        df = df.query('day == @day_i')

    print(df.columns)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df.month.mode()
    print('Most common month:', common_month)

    # display the most common day of week
    common_day = df.day.mode()
    print('Most common day of week:', common_day)

    # display the most common start hour
    common_hour = df.hour.mode()
    print('Most common hour of day:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_gender_distribution(df):
    genders = df['Gender'].fillna('Unknown')
    gender_counts = genders.value_counts().sort_index()
    n = len(genders)
    for gender, count in gender_counts.items():
        yield (gender, count / n)

def get_birth_decade_distribution(df, granularity=10):
    birth_years = df.dropna(subset=['Birth Year'])['Birth Year'].astype(int)
    decade_counts = (granularity * (birth_years // granularity)).value_counts().sort_index()
    n = len(birth_years)
    for decade, count in decade_counts.items():
        percentage = count/n
        yield decade, percentage

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    # df_station = df[df['Start Station'] == common_start_station]
    print(f'Most common start station: "{common_start_station}"')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'Most common end station: "{common_end_station}"')

    # display most frequent combination of start station and end station trip
    common_a, common_b = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'Most common journey: "{common_a}" -> "{common_b}"')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_days = round(df['Trip Duration'].sum() / (60*60*24), 1)
    print(f'Total time traveled: {total_travel_days} days')

    # display mean travel time
    mean_travel_mins = round(df['Trip Duration'].mean() / 60.0, 1)
    print(f'Average trip duration: {mean_travel_mins} minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('Count of user by type')
        for user_type, count in df.groupby('User Type').size().items():
            print(f'- {user_type}: {count}')

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Count of users by gender')
        for gender, percentage in get_gender_distribution(df):
            perc_str = f'{round(100*percentage, 2)}%'
            print(f'- {gender}: {perc_str}')

    if 'Birth Year' in df.columns:
        print('Birth year distribution:')
        for decade, percentage in get_birth_decade_distribution(df):
            perc_str = f'{round(100 * percentage, 2)}%'
            print(f"- {decade}s: {perc_str}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
