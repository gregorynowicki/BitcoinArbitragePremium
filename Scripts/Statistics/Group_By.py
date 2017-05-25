import pandas as pd
import os
import numpy as np

###########################################################
#        Add Exchange Name and Amount Able to Sell        #
###########################################################
#    Also Check to make sure the transactions are right   #
###########################################################
def if_sixty(x):
    if x==60:
        return 0
    else:
        return x

def to_dates(row):
    if month < 10:
        mts = '0'+str(month)
    else:
        mts = str(month)
    day = row['TradeDay']
    if day < 10:
        dts = '0'+str(day)
    else:
        dts = str(day)
    hr = row['TradeHour']
    if hr < 10:
        hts = '0'+str(hr)
    else:
        hts = str(hr)
    min = row['TradeMin']
    if min < 10:
        mints = '0'+str(min)
    else:
        mints = str(min)
    ts = hts+":"+mints+":00"
    full = str(year)+'-'+mts+'-'+dts+" "+ts
    return(full)


for year in [2010,2011,2012,2013,2014,2015,2016]:
    for month in [4,5,6,7,8,9,10,11,12]:

        CASE = 1                # Case 1 # Case 2 # Case 3 # Case 4 # Case 5 # Case 6
        MINS_PRIOR = 5          #   5    #   15   #   20   #   15   #   15   #  15
        MINS_AFTER = MINS_PRIOR #        #        #        #        #        #
        MINS_DELAY = 0          #   0    #   0    #   5    #   1    #   3    #  5
        short_exposure=1

        # Transaction time constraints
        use_mean = 1


        TradeLog = pd.DataFrame()

        base_dir = os.path.join("C:\\","Honors_Thesis","Cleaned_Files")
        month_dir = os.path.join(base_dir,str(year),str(month))
        file_dir = os.path.join(month_dir,"Agg_"+str(year)+"_"+str(month)+".csv")

        print("Year: {} Month: {}.  Reading Data.".format(year, month))
        month_data = pd.read_csv(file_dir)
        #print(month_data.head())
        print("Original Length: {}".format(len(month_data)))
        print("Year: {} Month: {}.  Converting to DT.".format(year, month))
        month_data['TradeDate'] = pd.to_datetime(month_data['TradeDate'])
        print("Year: {} Month: {}.  Converting Day".format(year, month))
        month_data['TradeDay'] = month_data['TradeDate'].apply(lambda x: x.day)
        print("Year: {} Month: {}.  Converting Hour".format(year, month))
        month_data['TradeHour'] = month_data['TradeDate'].apply(lambda x: x.hour)
        print("Year: {} Month: {}.  Converting Min".format(year, month))
        month_data['TradeMin'] = month_data['TradeDate'].apply(lambda x: x.minute)
        month_data['NewTradeMin'] = month_data['TradeMin'].apply(lambda x: np.ceil(x/10,)*10)
        month_data['NewTradeMin'] = month_data['NewTradeMin'].apply(lambda x: if_sixty(x))
        month_data['TradeMin'] = month_data['NewTradeMin']
        #print(month_data.loc[month_data['TradeMin']>=55].head())
        month_data['DollarVolume'] = month_data['Price']*month_data['Volume']
        #print(month_data.head())
        test = (month_data.groupby(by=['TradeDay','TradeHour','TradeMin','Exchange']).sum())
        test = test.reset_index()
        #print(test.head())
        print("New Length: {}".format(len(test)))
        #print(type(test))
        test['TradeDate'] = test.apply(to_dates,axis=1)
        test['TradeDate'] = pd.to_datetime(test['TradeDate'])
        test['Price'] = test['DollarVolume']/test['Volume']
        #print(test.head())
        test = test[['TradeDate','Price','Volume','Exchange']]
        #print(test.head())
        #print(test.tail())
        #print(test.head())
        fl_dir = os.path.join(month_dir,"AggAgg5Rm_"+str(year)+"_"+str(month)+".csv")
        test.to_csv(fl_dir,index=False)