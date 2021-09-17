import time
import pandas as pd
import numpy as np
import json as js

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ["January", "February", "March", "April","May", "June"]

days = {1:"Sunday", 2:"Monday", 3:"Tuesday", 4:"Wednesday", 5:"Thursday", 6:"Friday", 7:"Saturday"}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    month = ""
    day = ""

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Would you like to see data for Chicago, New York City, Washington? \n"))

    while city.lower() not in ["chicago", "new york city", "washington"]:

        print("Incorrect city entered.")
        city = str(input("\nWould you like to see data for Chicago, New York City, Washington? \n"))

    city = city.lower()
    
    time_filter = str(input("\nWould you like to filter the data by month, day or not at all? Type 'none' for no time filter. \n"))

    if time_filter.lower() == 'none':        
        month = None 
        day = None

    while time_filter.lower() not in ["month","day", "none"]:
        print("Incorrect choice. Enter 'month', 'day' or 'none'")
        time_filter = str(input("\nWould you like to filter the data by month, day or not at all? Type 'none' for no time filter. \n"))

    # get user input for month (all, january, february, ... , june)  
    
    if time_filter.lower() == "month":
        month = str(input("\nWhich month? January, February, March, April, May or June? \n"))
        
        while month.lower().title() not in months:
            print("Incorrect month.")
            month = str(input("\nWhich month? January, February, March, April, May or June? \n")).title()
        month = month.title()

    # get user input for day of week (all, monday, tuesday, ... sunday)   
    if time_filter.lower() == "day":

        try:
            
            day_index = int(input("\nWhich day? Please type your response as an integer (eg. 1= Sunday) \n"))
            
            while day_index not in [1,2,3,4,5,6,7]:
                print("Incorrect day.")
                day_index = int(input("\nWhich day? Please type your response as an integer (eg. 1= Sunday) \n"))
            day = days[day_index]

        except:

            print("Enter a valid integer. e.g 1")
            day_index = int(input("\nWhich day? Please type your response as an integer (eg. 1= Sunday) \n"))
            
            while day_index not in [1,2,3,4,5,6,7]:
                print("Incorrect day.")
                day_index = int(input("\nWhich day? Please type your response as an integer (eg. 1= Sunday) \n"))

            day = days[day_index]

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
    df = pd.read_csv(CITY_DATA[city])   

    df['Start Time'] =  pd.to_datetime(df['Start Time'])

    if month != '':
        current_month = months.index(month)+1
        df= df[(df['Start Time'].dt.month == current_month)]
    
    if day:
        df= df[(df['Start Time'].dt.day_name() == day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    df['Month'] = df['Start Time'].dt.month
    common_month = df['Month'].mode()[0]
    month_count = df[(df['Month'] == common_month)].count(axis=0)['Month']
    print('The most common month: {} Count: {} '.format(months[common_month-1], month_count))

    # display the most common day of week

    df['Day of Week'] = df['Start Time'].dt.day_name()
    common_day = df['Day of Week'].mode()[0]
    day_count = df[(df['Day of Week'] == common_day)].count(axis=0)['Day of Week']
    print('The most common Day of Week: {} Count: {} '.format(common_day, day_count))

    # display the most common start hour

    df['Start Hour'] = df['Start Time'].dt.hour
    common_hour = df['Start Hour'].mode()[0]
    hour_count = df[(df['Start Hour'] == common_hour)].count(axis=0)['Start Hour']
    print('The most common Start Hour: {} Count: {} '.format(common_hour, hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].mode()[0]
    start_station_count = df[(df['Start Station'] == common_start_station)].count(axis=0)['Start Station']
    print('The most commonly used Start station: {} Count: {} '.format(common_start_station, start_station_count))

    # display most commonly used end station

    common_end_station = df['End Station'].mode()[0]
    end_station_count = df[(df['End Station'] == common_end_station)].count(axis=0)['End Station']
    print('The most commonly used end station: {} Count: {} '.format(common_end_station, end_station_count))

    # display most frequent combination of start station and end station trip

    df['Start-End Stations'] = df['Start Station'] + ' to ' + df['End Station']
    f_combined_stations = df['Start-End Stations'].mode()[0]

    join_len = len(' to ')
    end_index = f_combined_stations.index(' to')
    start_s = f_combined_stations[:end_index]
    end_s = f_combined_stations[len(start_s)+join_len:]
    from_to_stations_count = df[(df['Start-End Stations'] == f_combined_stations)].count(0)['Start-End Stations']
    print('The most frequent combination of start and end station trip: {} to {} Count: {} combinations '.format(start_s, end_s, from_to_stations_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() /3600
    print("Total travel time in hours {} hours.".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df[df['User Type'].notnull()]
    users_count = pd.Series(users['User Type'].value_counts())

    for type_user in users['User Type'].unique():
        print("{} {}s" .format(users_count[type_user], type_user))

    # Display counts of gender

    columns = list(df.columns)
    is_gender_present = 'Gender' in columns

    if is_gender_present:
        genders = df[df['Gender'].notnull()]
        gender_count = pd.Series(genders['Gender'].value_counts())

        for gender in genders['Gender'].unique():       
            print("{} {}s" .format(gender_count[gender], gender))   
    else:
        print("\nThe selected city has no 'Gender' information")

    # Display earliest, most recent, and most common year of birth
    birthday_col = 'Birth Year' in columns

    if birthday_col:

        birth_year = df['Birth Year']
        print('\nMost earliest year of birth: {}'.format(birth_year.min()))
        print('\nMost recent year of birth: {}'.format(birth_year.max()))
        print('\nMost common year of birth: {}'.format(birth_year.mode()[0]))

    else:
        print("\nThe selected city has no 'Birth Day' information")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_five_records(raw_json_data):
    """
    Helper function to convert DataFrame into JSON data and print
    """
    for row_data in raw_json_data:
            parsed_data = js.loads(row_data)
            json_data = js.dumps(parsed_data, indent=4) 
            print(json_data)

def display_raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs `yes`. Iterate until user response with a `no`

    """

    data = 0

    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        if answer.lower() == 'yes':
            print(df[data : data+5])
            data += 5

        else:
            break    

def main():
    while True:
        city, month, day = get_filters()

        if month == None and day == None:
            print('No time filter chosen.')
            break

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
