import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' }
MONTHS = [
    'january', 'february', 'march', 'april',
    'may', 'june']
    # months limited to the first six months of they year as stated in the dataset description.
    # Data set for the whole year:
    #['january', 'february', 'march', 'april',
    #'may', 'june', 'july', 'august',
    #'september', 'october', 'november', 'december']
DAYS = [
    'monday', 'tuesday', 'wednesday', 'thursday',
    'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = None
    while (city is None):
        city = input('\nWould you like to see data for Chicago, New York City, or Washington\n').lower()
        if (city not in CITY_DATA):
            print ("Unknown city, please choose from:", str.join(", ", CITY_DATA))
            city = None

    filter_types = {'month', 'day', 'none'}
    filter_type = None
    while (filter_type is None):
        filter_type = input('\nWould you like to filter the data by month, day, or not at all (type none for no time filter)?\n').lower()
        if (filter_type not in filter_types):
            print ("Unknown filter, please choose from:", str.join(", ", filter_types))
            filter_type = None

    if (filter_type == 'none'):
        print('-'*40)
        return city, "all", "all"

    if (filter_type == 'month'):
        month = None
        while (month is None):
            month = input('\nWhich month - January, February, March, etc?\n').lower()
            if (month not in MONTHS):
                print ("Unknown month, please choose from:", str.join(", ", MONTHS))
                month = None
        print('-'*40)
        return city, month, "all"

    if (filter_type == 'day'):
        day = None
        while (day is None):
            day = input('\nWhich day - Monday, Tuesday, Wednesday, etc?\n').lower()
            if (day not in DAYS):
                print ("Unknown day, please choose from:", str.join(", ", DAYS))
                day = None
        print('-'*40)
        return city.lower(), 'all', day.lower()


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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = MONTHS.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        day_index = DAYS.index(day)
        df = df[df['day_of_week'] == day_index]

    df.reset_index(drop=True, inplace=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]
    popular_hour = df['hour'].mode()[0]

    print("Most popular month: ", MONTHS[popular_month - 1].title())
    print("Most popular day: ", DAYS[popular_day].title())
    print("Most popular hour: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Trip'] = df['Start Station'] + ' -TO- ' + df['End Station']
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    popular_trip = df['Trip'].mode()[0]

    print("Most popular start station: ", popular_start_station)
    print("Most popular end station: ", popular_end_station)
    print("Most popular trip: ", popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print("Total travel time: ", total_travel_time, " seconds")
    print("Mean travel time: ", mean_travel_time, " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    # TO DO: Display counts of gender
    if ('Gender' in df.columns):
        gender_types = df['Gender'].value_counts()
        print(gender_types,'\n')
    else:
        print("User gender statistics not available")

    # TO DO: Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df.columns):
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]

        print("Earliest year of birth: ", earliest_year)
        print("Most recent year of birth: ", recent_year)
        print("Most common year of birth: ", common_year)
    else:
        print("User year of birth statistics not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df, start_line, row_count):
    """Displays raw data for the selected city and time filters."""

    row = start_line
    if start_line + row_count < len(df.index):
        end_row = start_line + row_count
    else:
        end_row = len(df.index)
    extra_columns = {'month', 'day_of_week', 'hour', 'Trip'}
    while row < end_row:
    # for loop provides more efficient and neat code but additional columns
    # added during df loading must be filtered out as they are not part of raw data
        for column in df.columns:
            if (column not in extra_columns):
                print(column, ": ",df.loc[row,column])
        row += 1
        print('\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print(df)

        see_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        start_row = 0
        while (see_raw_data.lower() == 'yes'):
            display_raw_data(df, start_row, 5)
            start_row += 5
            see_raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
