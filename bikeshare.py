import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
global raw_start
global raw_stop

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
  
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please input the city, you would like to analyze data for.\n You can choose between "Chicago", "New York City" and "Washington"')
    while not city.title() in ('Chicago', 'New York City', 'Washington'):
        city = input('You must enter either "Chicago", "New York City" or "Washington"')

    # TO DO: get user input for month (all, january, february, ... , june)
    global month
    month = input('Great, now please input the month you wish to analyze: (You can choose jan, feb, mar, apr, may, jun or all)\n')
    while not month.title() in ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'All'):
        month = input('You must enter either jan, feb, mar, apr, may, jun or all.\n')
                      
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    global day
    day = input('And one last thing: What day of the week, would you like to pull data from? You can enter "Monday", "Tuesday", "Wedensday", "Thursday", "Friday", "Saturday", "Sunday" or "all".\n')
    
    while not day.title() in ("Monday", "Tuesday", "Wedensday", "Thursday", "Friday", "Saturday", "Sunday", "All"):
        day = input('You must enter either "Monday", "Tuesday", "Wedensday", "Thursday", "Friday", "Saturday", "Sunday" or "all":\n')
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
    
    df = pd.read_csv(city.replace(' ', '_').lower()+'.csv')
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Filter by day or select all
    if day != 'all':
        df['filter_day'] = df['Start Time'].dt.weekday_name
        # filter by day of week to create the new dataframe
        df = df[df['filter_day'] == day.title()]
    # filter by month or select all months
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        month = months.index(month.title()) + 1
        df['filter_month'] = df['Start Time'].dt.month
        df = df[df['filter_month'] == month]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #Only find most popular month, if no month filter was applied
    if month == 'all':
        #Get the month number from the start time
        df['month'] = df['Start Time'].dt.month
        # TO DO: display the most common month
        print('Most common month:', df['month'].mode()[0])
    else:
        print('You chose to only view this month: ', month)

    #Only find most popular day, if no day filter was applied
    if day == 'all':
        # TO DO: display the most common day of week
        df['day'] = df['Start Time'].dt.dayofweek
        print('Most common day of week:', df['day'].mode()[0]+1)
    else:
        print('You chose to only view this day of the week: ', day)

    # TO DO: display the most common start hour
    df['start'] = df['Start Time'].dt.hour
    print('The most popular hour to begin a bike ride was: ', df['start'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('The most popular starting station was: ', pop_start_station)

    # TO DO: display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('The most popular stopping station was: ', pop_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['station_combo'] = df['Start Station']+' --> '+df['End Station']
    pop_station_combo = df['station_combo'].mode()[0]
    print('The most popular start-and-stop station combination was: ',pop_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()/60
    print('The total traveltime in minutes based on your filters was: ', total_travel_time)
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('The mean traveltime in minutes based on your filters was: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('There were the following usertypes in the data returned based on your filters:\n', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        user_genders = df['Gender'].fillna('unknown').value_counts()
        print('User genders were registered in the following numbers in the data returned based on your filters:\n', user_genders)
    else:
        print('Data based on your filters does not contain information about gender')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:

        print('The oldest user (earliest registered birth year) is from: ', int(df['Birth Year'].min()))
        print('The youngest user (latest registered birth year) is from: ', int(df['Birth Year'].max()))
        print('The most commonly registered birth year is: ', int(df['Birth Year'].mode()[0]))
    else:
        print('Data based on your filters does not contain information about birth year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #Ask if the user wishes to view the raw data. User must give valid yes/no input.
    raw = input('Would you like to see the raw data that this analysis is based on? Please answer "yes" or "no".')
    while raw.title() != 'Yes' and raw.title() != 'No':
        raw = input('Please answer "yes" or "no".')
    if raw.title() == 'Yes':

        raw_data(df)
    print('Done.')

def raw_data(df):
    """Displays five lines of raw data on user's request. When user answers no, the function will break"""
    raw_start = 0
    raw_stop = 5
    print(df[raw_start:raw_stop])
    five_more = 'yes'
    while five_more.title() != 'No':
        five_more = input('Would you like to view five more lines?')
        if five_more.title() != 'Yes' and five_more.title() != 'No':
            five_more = input('Please answer "yes" or "no"')
        elif five_more.title() == 'Yes':
            raw_start = raw_start + 5
            raw_stop = raw_stop + 5
            print(df[raw_start:raw_stop])
        elif five_more.title() == 'no':
            break
                          
def main():
    while True:
        city, month, day = get_filters()
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
