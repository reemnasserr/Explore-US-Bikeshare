import time
import pandas as pd
import sys
import calendar
import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_list = ['january','february','march','april','may','june','all']
days_list =['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']


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
        city = input('Choose one of the cities to explore chicago, new york city, washington.\n').lower()
        if city =='chicago' or city =='new york city' or city=='washington':
            print('You chose {}.\n'.format(city))
            break
        else:
            print('Please check that you entered the correct city name.\n')
            

    while True:
        filter_choice = input('Would you like to filter the data by month, day, both or none?\n').lower()
        if filter_choice =='month' or filter_choice =='day' or filter_choice=='none'or filter_choice=='both':
            print('You chose {} for filtering.\n'.format(filter_choice))
            break
        else:
            print('Please check that you entered the correct filtering name.\n')
            
      
    # get user input for month (all, january, february, ... , june)
    while True:
        if filter_choice == 'month' or filter_choice=='both' :
            month = input('which month? january,february,march,april,may,june or all\n(please type full month name)\n').lower()            
            if month in months_list:
                print('you chose {}.\n'.format(month))
                break
            else:
                print('Please check that you entered the correct month name.\n')
                continue 
        else:
            month = 'all'
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        if filter_choice == 'day' or filter_choice=='both':
            day = input('which day? Sunday,monday,tuesday,wednesday,thursday,friday,saturday or all\n(please type full day name)\n').lower()            
            if day in days_list:
                print('you chose {}.\n'.format(day))
                break
            else:
                print('Please check that you entered the correct day name.\n')
                continue
        else:
            day = 'all'
            break

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df = df.rename(columns={'Unnamed: 0':'ID'})
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
  
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()



    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months_list.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month_count = df['month'].value_counts().max()
    print('The most common month:{} with total counts: {}'.format(calendar.month_name[common_month],common_month_count))
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    common_day_count = df['day_of_week'].value_counts().max()
    print('The most common day of week:{} with total counts: {}'.format(common_day,common_day_count))

    # display the most common start hour
    common_start_hour =df['Start Time'].dt.hour.mode()[0]
    common_start_hour_count =df['Start Time'].dt.hour.value_counts().max()
    print('The most common start hour: {} with total counts: {}\n'.format(common_start_hour,common_start_hour_count))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_StartStation = df['Start Station'].mode()[0]
    common_StartStation_count = df['Start Station'].value_counts().max()
    print('The most commonly used start station:{} with total counts:{}.'.format(common_StartStation,common_StartStation_count))
    # display most commonly used end station
    common_endStation = df['End Station'].mode()[0]
    common_endStation_count = df['End Station'].value_counts().max()
    print('The most commonly used end station:{} with total counts:{}.'.format(common_endStation,common_endStation_count))

    # display most frequent combination of start station and end station trip
    freq_combination=df.groupby(['Start Station','End Station']).size().idxmax()
    freq_combination_count=df.groupby(['Start Station','End Station']).count().max()[1]
    print('The most frequent combination of start station and end station trip:{} with total counts:{}.'.format(freq_combination,freq_combination_count))
    # print('The most frequent combination of start station and end station trip:{}'.format(freq_combination_2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    duration_time = df['Trip Duration'].sum()
    print('Total trip duration:{}.'.format(duration_time))
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Average travel time:{}.'.format(mean_time))
    duration_time_count = df['Trip Duration'].count()
    print('Total counts:{}'.format(duration_time_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types:\n{}'.format(user_types.to_string()))
    
    # Not available for washington
    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nGenders:\n{}'.format(gender.to_string()))
    else:
        print('\nGender data is only available for NYC and Chicago.')

    # Display earliest, most recent, and most common year of birth
    # Display some statistics about the diversity of ages in the data
    if 'Birth Year' in df.columns:
        most_common = df['Birth Year'].mode()[0]
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        young = (df[df['Birth Year']>=1990.0]).count().max()
        old = (df[df['Birth Year']<1990.0]).count().max()      
        print('\nEarliest year of birth:{}'.format(int(earliest)))
        print('Most recent year of birth:{}'.format(int(most_recent)))
        print('Most common year of birth:{}'.format(int(most_common)))
        print('Number of users born since 1990 till now: {} from {}'.format(young,df.shape[0]))
        print('Number of users born before 1990 till now: {} from {}'.format(old,df.shape[0]))
        print('Number of users didn\'t mention their birth year: {} from {}'.format(df['Birth Year'].isna().sum(),df.shape[0]))
    else:
        print('\nBirth Year data is only available for NYC and Chicago.') 
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def show_data(df):
    
    """
    Show 5 rows individually on user request.
    
    """
    start = 0
    count_row = df.shape[0] #len of dataframe
    df['month']=df['month'].apply(lambda x: calendar.month_name[x]) #to get the full month name instead of int for user
    df['Start Time'] = df['Start Time'].apply(str)

    while True:
        display_user = input('\nWould you like to see 5 lines of raw data enter "yes" or "no" to exit.\n')  
        if display_user.lower()=="yes" and (count_row - (start+5))  > 0 :
            
            print('Showing data from: {} to {} from total rows: {} '.format(start,start+5,count_row))
            rows = (df.iloc[start:start+5].to_dict(orient='records'))  #.to_string()
            for row in rows:
                pprint.pprint(row,sort_dicts=False)
            start+=5

        elif display_user.lower()=="yes" and start > count_row:
            print('\nNo more data to display.')
            break
            
        elif display_user.lower()=="yes" and (count_row -( start+5)) <= 5 :
            
            print('Showing data from: {} to {} from total rows: {} '.format(start,start+5,count_row))
            rows = (df.iloc[start:count_row].to_dict(orient='records'))
            for row in rows:
                pprint.pprint(row,sort_dicts=False)
            print('\nNo more data to display.')                
            break

    
        elif display_user=="no":
            break
        else:
            print('\nInvalid input')
    
       
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                break   
            elif  restart.lower()=="no":
                sys.exit()
            else:
                print('Please check that you entered one of the options.')
                


if __name__ == "__main__":
	main()
