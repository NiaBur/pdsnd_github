import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    usa_city = ''
    while usa_city.lower() not in CITY_DATA:
        usa_city = input('Please enter name of usa city: ')
        if usa_city.lower() in CITY_DATA:
            city = CITY_DATA[usa_city.lower()]
        else:
            print('City must be either new york, chicago, or washington')

    # get user input for month (all, january, february, ... , june)
    month_of_year = ''
    while month_of_year.lower() not in MONTH_DATA:
        month_of_year = input('Please enter month of year: ')
        if month_of_year.lower() in MONTH_DATA:
            month = month_of_year.lower()
        else:
            print('Not applicable - please choose different month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    the_day = ''
    while the_day.lower() not in DAY_DATA:
        the_day = input('Please enter day of week: ')
        if the_day.lower() in DAY_DATA:
            day = the_day.lower()
        else:
            print('Selection must be a day of the week')

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
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = MONTH_DATA.index(month)
        df = df.loc[df['month'] == month]

    if day != 'all':
        df = df.loc[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is ', MONTH_DATA[most_common_month].title())

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day is ', most_common_day)

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is ', str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is ', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is ', most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combo = (df['Start Station'] + '||' + df['End Station']).mode()[0]
    print('The most frequent combo is ', str(most_frequent_combo.split('||')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('The counts of user types is ', counts_of_user_types)

    # Display counts of gender
    if 'Gender' in df:
        counts_of_gender_types = df['Gender'].value_counts()
        print('The counts of gender types is ', counts_of_gender_types)
    else:
        print('Not appplicable for this location')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year_of_birth = df['Birth Year'].min()
        print('The earliest year of birth is ', earliest_year_of_birth)

        latest_year_of_birth = df['Birth Year'].max()
        print('The latest year of birth is ', latest_year_of_birth)

        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('The most common year of birth is ', most_common_year_of_birth)

    else:
        print('Not applicable for this location')

def display_data(df):
    raw_data = 0
    while True:
        answer = input("Do you want to see the raw data? Yes or No").lower()
        if answer not in ['yes', 'no']:
            answer = input("You wrote the wrong word. Please type Yes or No.").lower()
        elif answer == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
            again = input("Do you want to see more? Yes or No").lower()
            if again == 'no':
                break
        elif answer == 'no':
            return

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
