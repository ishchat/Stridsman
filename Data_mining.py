# from yahoo_finance import Share
# yahoo = Share('YHOO')
# print(yahoo.get_open())
# print(yahoo.get_historical('2014-04-25', '2014-04-29'))

import pandas as pd
import datetime as dt

data_df = pd.read_csv('C:/Users/Ishan/Desktop/Trade/table.csv')
# print(data_df)

class DataMining:

    def __init__(self, df):
        self.df = df

    def weekly(self):
        self.df['Datetype'] = self.df['Date'].apply(lambda x: dt.datetime.strptime(x, "%m/%d/%Y"))
        self.df['Year'] = self.df['Datetype'].apply(lambda x: x.year)
        self.df["DayOfWeek"] = self.df['Datetype'].dt.dayofweek #weekday 0 means Monday
        self.df["WeekdayName"] = self.df['Datetype'].dt.weekday_name
        self.df["WeekOfYear"] = self.df['Datetype'].dt.week #This function will have week value 1 starting from 1st Monday of the year. This week will end on subsequent Sunday. Then from next Monday week 2 will start and so on. Days before first Monday of the year will have week 53. Days after last Sunday of the year will also be week 53.
        # http://stackoverflow.com/questions/32459325/python-pandas-dataframe-select-row-by-max-value-in-group
        self.df_weekly1 = self.df.loc[self.df.reset_index().groupby(['Year','WeekOfYear'])['DayOfWeek'].idxmin()]
        self.df_weekly1 = self.df_weekly1.drop_duplicates(['Year','WeekOfYear','DayOfWeek'])  # Just to make sure no 3 rows with same values in these 3 columns exist
        self.df_weekly1['Date'] = self.df_weekly1['Datetype']
        self.df_weekly1 = self.df_weekly1.set_index(['Datetype'])
        self.df_weekly1 = self.df_weekly1.sort_index(ascending=True)
        self.df_weekly2 = self.df.loc[self.df.reset_index().groupby(['Year','WeekOfYear'])['DayOfWeek'].idxmax()]
        self.df_weekly2 = self.df_weekly2.drop_duplicates(['Year','WeekOfYear','DayOfWeek'])  # Just to make sure no 3 rows with same values in these 3 columns exist
        self.df_weekly2['Date'] = self.df_weekly2['Datetype']
        self.df_weekly2 = self.df_weekly2.set_index(['Datetype'])
        self.df_weekly2 = self.df_weekly2.sort_index(ascending=True)
        #Doing inner join (as opposed to vertically appending) as it will take care of many things on its own. There might be only 1 trading day in some weeks(ex-first week of year), there may be some other issue. Inner join ensures we match the 2 days representing min and max trading days for a given week ina  given year.
        #http://stackoverflow.com/questions/28228781/python-pandas-inner-join
        self.df_weekly_joined = pd.merge(self.df_weekly1, self.df_weekly2, on=['Year', 'WeekOfYear'])

        print("nothing")


    def monthly(self):
        self.df['month'] = self.df['Datetype'].apply(lambda x: x.month)

DM = DataMining(data_df)

DM.weekly()
DM.monthly()

# print(DM.df)
print(DM.df_weekly)

DM.df_weekly.to_csv('C:/Users/Ishan/Desktop/Trade/table1.csv')
