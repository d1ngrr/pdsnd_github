import time
import pandas as pd
import numpy as np
import os

# define dictionary to store data file filenames
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

 # define lists with months and days to be used for filtering options           
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

# set option to display all columns
pd.set_option('display.max_columns',200)
              
def display_choices(choices):
    """
    Displays numbered list of choices for user to select from
    
    Args:
        (list) choices - list of choices (e.g. cities, months, days)
    """
    for choice in choices:
        print(' '*5 + str(choices.index(choice)+1) +  '. ' + choice.title())

def get_filters():
    """
    Asks user to specify a city, month, and day to analyse.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington).
    prompt = "Which city would you like to look at?\n"
    prompt+= "(Enter the number that corresponds with your choice)\n"
    display_choices(list(CITY_DATA.keys()))
    
    while True:
        try:
            city = input(prompt).strip().lower()            
            if city in ['1','chicago']:
                city = 'Chicago'
                break
            elif city in ['2','new york city','new york']:
                city = 'New York City'
                break
            elif city in ['3','washington']:
                city = 'Washington'
                break
            else:
                print('Please make a valid choice - 1, 2 or 3.')
        except Exception as e:           
            print("Exception occurred: {}".format(e))
            print('Please make a valid choice - 1, 2 or 3.')    
    
    # get user input for month (all, january, february, ... , june)    
    prompt = "Which month would you like to look at?\n"
    prompt+= "(Enter the number that corresponds with your choice)\n"
    print(prompt)
    display_choices(months)
    # BreakFlag variable needed to escape from while loop due to nested loops
    BreakFlag = 0

    while True:
        try:
            month = input().strip().lower() 
            for m in months:
                if month in [m, str(months.index(m)+1)]:
                    month = m.title()
                    BreakFlag = True
                    break
            if BreakFlag:
                break
            else:
                 print('Please make a valid choice - 1 to 7.')  
        except Exception as e:           
           print("Exception occurred: {}".format(e))
           print('Please make a valid choice - 1 to 7')
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt = "Which day of the week would you like to look at?\n"
    prompt+= "(Enter the number that corresponds with your choice)\n"
    print(prompt)
    display_choices(days)
    # reset BreakFlag
    BreakFlag = 0

    while True:
        try:
            day = input().strip().lower()        
            for d in days:
                if day in [d, str(days.index(d)+1)]:
                    day = d.title()
                    BreakFlag = True
                    break
            if BreakFlag:
                break
            else:
                print('Please make a valid choice - 1 to 7.')
        except Exception as e:           
           print("Exception occurred: {}".format(e))
           print('Please make a valid choice - 1 to 7')     

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
    # load data file into a dataframe    
    script_dir = os.path.abspath( os.path.dirname( __file__ ) )
    filepath = script_dir + "//data//" + CITY_DATA[city.lower()]
    df = pd.read_csv(filepath)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All': 
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]    

    return df
    

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        df - Pandas DataFrame    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')    
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]    
    print('Most Frequent Start Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]    
    print('Most Frequent Start Day of the Week:', popular_day_of_week)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]    
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        df - Pandas DataFrame
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]  
    print('Most Frequent Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end_station)    

    # display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + " to " + df['End Station']
    popular_start_end = df['start_end'].mode()[0]
    print('Most Frequent Combination of Start Station and End Station:', popular_start_end) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Args:
        df - Pandas DataFrame    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert the Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # display total travel time
    df['travel_time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['travel_time'].sum()
    print("Total Travel Time: {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['travel_time'].mean()
    print("Mean Trip Duration: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Args:
        df - Pandas DataFrame    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Number of Users by User-Type:")
    print(user_types)
    print() 

    # Display counts of gender
    print("Number of Users by Gender:")
    # Use try/except to handle absence of Gender column in Washington.csv
    try: 
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
        print()
    except KeyError:
        print("No gender data available")
        print()

    # Display earliest, most recent, and most common year of birth
    print("User Birth Year Stats:")
    # Use try/except to handle absence of Birth Year column in Washington.csv
    try:
        earliest_birthyear = df['Birth Year'].min()
        latest_birthyear = df['Birth Year'].max()
        popular_birthyear = df['Birth Year'].mode()[0]
        print("Earliest year of birth: {} ".format(int(earliest_birthyear)))
        print("Most recent year of birth: {} ".format(int(latest_birthyear)))
        print("Most common year of birth: {}".format(int(popular_birthyear)))
    except KeyError:
        print("No birth year data available")
        print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 
    
def show_raw_data(df):
    """
    Display 5 lines of raw data.
    Prompt user if they would like to see another 5 lines of data.
    Continue displaying 5 more lines of data until user declines or end of data reached.
    Args:
        df - Pandas DataFrame    
    """
    print(df.head())
    i = 5
    last_row_index = df.tail(1).index.item()
    while i <= last_row_index:
        show_more = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
        if show_more.lower() in  ['yes','y']:
            if i + 4 <= last_row_index:
                print(df.iloc[i:i+5])
                i+=5
            elif i <= last_row_index:
                print(df.iloc[i:last_row_index + 1])
                print('---no more data to load---')
                break
        else:
            break
    else:
        print('---no more data to load---')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # populate null Gender and User Type data as 'Unknown'
        # Use try/except to continue where columns do not exist
        try: 
            df[['Gender', 'User Type']] = df[['Gender', 'User Type']].fillna('Unknown')
        except KeyError:
            pass
            
        # call functions to display stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # ask user if they would like to view raw data
        # call function to show raw data if requested
        show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if show_data.lower() in ['yes','y']:
            show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
