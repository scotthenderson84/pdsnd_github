import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input("Please enter the city you would you like to explore? (Chicago, New York City or Washington): ")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Invalid entry. Please enter a valid city to explore the data")
    # get user input for month (all, january, february, ... , june)
    while True:    
        month = input("Please enter the month to review (Specific Month e.g. January, February etc or 'all' for full data set): ")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Invalid entry. Please enter a valid month for analysis")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the day of the week to review (Monday, Tuesday or 'all' for full week): ")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid entry. Please enter a valid day for analysis")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the Specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # import City_Data file into dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Select month and day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        df = df[df['month'] == month]

    # filter by day
    if day != 'all':
                
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month for travel is", df['month'].mode()[0], "\n")

    # display the most common day of week
    print("The most common day of week for travel is", df['day_of_week'].mode()[0], "\n")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hours for travel are", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is", df['Start Station'].mode()[0], "\n")

    # display most commonly used end station
    print("The most commonly used end station is", df['End Station'].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip is: ", df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is", df['Trip Duration'].sum(), "\n")

    # display mean travel time
    print("The mean travel time is", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    
    #Data only available for Chicago & New York City
    if city != 'washington': 
       
        # Display counts of gender
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender, "\n")
        
        # Display earliest, most recent, and most common year of birth
        recentyob = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        earliestyob = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        commonyob = df['Birth Year'].mode()[0]
        print("The earliest year of birth is", earliestyob, "\n")
        print("The most recent year of birth is", recentyob, "\n")
        print("The most common year of birth is", commonyob, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    #Show raw data
    x = 1
    while True:
        raw = input('\nDo you want to review raw data? (yes or no): ')
        if raw.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break
   

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? (yes or no): ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()