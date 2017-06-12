import os
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
import itertools

MEN_DATA_DIR     = os.path.abspath(os.path.join(__file__, '..','..', '..','data','combined'))+'/'
WOMEN_DATA_DIR   = os.path.abspath(os.path.join(__file__, '..','..', '..','data','combined'))+'/'
EXTENSION    = '.csv'
CURRENT_YEAR = 2017 # Change once a year!

def read_by_date(earliest_year=None, latest_year=None):
    range_of_years = [year for year in range(latest_year, earliest_year -1, -1)]
    atp_frames     = map(lambda x: pd.read_csv(x,skipinitialspace=True), 
                         [MEN_DATA_DIR + str(year) + EXTENSION for year in range_of_years])
    wta_frames     = map(lambda x: pd.read_csv(x,skipinitialspace=True), 
                         [WOMEN_DATA_DIR + str(year) + 'w'+ EXTENSION for year in range_of_years])
   
    atp_all_frames = pd.concat(atp_frames, keys=range_of_years)
    wta_all_frames = pd.concat(wta_frames, keys=range_of_years)
    return atp_all_frames, wta_all_frames


def change_date_atp_to_betting(df):
    df['tourney_date'] = df['tourney_date'].apply(lambda x: str(x)[:4]+'-'+str(x)[4:6]+'-'+str(x)[6:])
    df['tourney_date'] = pd.to_datetime(df['tourney_date'])
    return df

def change_date_betting_to_atp(df):
    df["Date"] = df["Date"].apply(lambda x: str(x).replace('-',''))
    return df

def change_name_atp_to_betting(df):
    format_change = lambda x: x.split(' ', 1)[1] + ' ' + x.split(' ', 1)[0][0] + '.'
    df['winner_name']  = df['winner_name'].apply(format_change)
    df['loser_name']   = df['loser_name'].apply(format_change)
    return df

def join_atp_and_bet_tables(atp=None, bet=None):
    range_in_days = 3
    atp, bet = fix_dates_discrepancies(atp, bet, 3)
    res = pd.merge(bet, atp, how='inner',
                   left_on=['Date','Winner','Loser'],
                   right_on=['tourney_date','winner_name','loser_name'])
   
    # Many columns appear in both tables, Here we drop the repeated columns from bet
    # We will then stick to atp_dao from now on
#    columns_to_drop = ['Winner','Loser','Date','Tournament','Court','Surface','ATP','Location','Date']
 #   res = res.drop(columns_to_drop, axis=1)
    return res


'''
 Dates do not match in atp and betting databases. This could be due to different timezones.
 This function checks if dates are within a small range, and renders them equal in that case,
 substituting one with the other. Function assumes that The names used in the player fields are
 use the same format -> Surname FirstLetterOfFirstName.

 Warning: function is slow. O(n**2) where n is the length of the shortest data frame
'''
def fix_dates_discrepancies(atp_df, bet_df, range_in_days=1):
    # TODO: Copy initial dfs? Or change input parameters?
    a_counter = 0
    for i_atp, r_atp in atp_df.iterrows():
        print('atp len ' + str(len(atp_df)))
        print('CACA ' + str(a_counter))
        a_counter += 1

        date = r_atp['tourney_date']

        for i_bet, r_bet in bet_df.iterrows():
            matching_winner_and_loser = (r_atp['winner_name'] == r_bet['Winner']) and (r_atp['loser_name'] == r_bet['Loser'])   

            similar_dates = dates_within_range(range_in_days, r_atp['tourney_date'], r_bet['Date'])
            if matching_winner_and_loser and similar_dates:
                atp_df.set_value(i_atp, 'tourney_date', bet_df.loc[i_bet]['Date'])
                break
    return atp_df, bet_df

def dates_within_range(range_in_days, d1, d2):
    # TODO: remove string hack
    d1t = type(d1)
    d1 = str(d1).split(' ')[0]
    d2 = str(d2).split(' ')[0]
    date_1 = datetime.strptime(d1,'%Y-%m-%d')
    date_2 = datetime.strptime(d2,'%Y-%m-%d')
    r = relativedelta(date_1,date_2)
    return (abs(r.days) <= range_in_days) and abs(r.months == 0) and abs(r.years == 0)

# With this I will get the index around which I have to fix dependencies.
def binarySearch(alist, item):
    first = 0
    last = len(alist)-1
    found = False

    while first<=last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    return found
