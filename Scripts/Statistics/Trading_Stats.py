import pandas as pd
import numpy as np

monthly_stats = []
long_only = 1
for year in [2010,2011,2012,2013,2014,2015,2016,2017]:
    if year==2010:
        months = [7,8,9,10,11,12]
    elif year == 2017:
        months = [1,2]
    else:
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
    for month in months:
        print("Year: {} Month: {}".format(year,month))
        tempDF = pd.read_csv("C:\\Honors_Thesis\\Case1\\Agg4Rm\\Agg5RmTradeLog_" + str(year) + "_" + str(month) + ".csv")
        tempDF = tempDF.loc[tempDF['AmountTraded']>0]


        if long_only == 1:
            tempDF['Duration'] = tempDF['SellDate'] - tempDF['BuyDate']
            print(tempDF)
            tempDF = tempDF.loc[tempDF['Duration'] >= 0]

        sells = sum(tempDF['SellPrice']*tempDF['AmountTraded'])
        buys = sum(tempDF['BuyPrice']*tempDF['AmountTraded'])

        if buys>0 and sells>0:
            record = []
            if (pd.isnull(buys)):
                print("BUYS")
            if (pd.isnull(sells)):
                print("SELLS")
            record.append(str(year)+'-'+str(month)+'-01')
            record.append((sells-buys)/(sells))
            record.append(buys)
            record.append(sells)
            record.append(sells+buys)
            record.append(sum(tempDF['AmountTraded']))
            record.append(sells-buys)
            record.append(len(tempDF))
            print("Length Buys: {}".format(len(tempDF['BuyDate'])))
            print("Length Sells: {}".format(len(tempDF['SellDate'])))
            test = tempDF['BuyDate'].append(tempDF['SellDate'])
            print("Sum: {}".format(len(test)))
            print("Dropped: {}".format(len(test.drop_duplicates())))
            record.append(len(test.drop_duplicates()))
            if month in [4,5,9,11]:
                record.append(30)
            elif month in [1,3,6,7,8,10,12]:
                record.append(31)
            elif month in [2]:
                if year%4==0:
                    record.append(29)
                else:
                    record.append(28)
            monthly_stats.append(record)


columns = ['Date','WeightedAverageSpread','DollarVolumeBought','DollarVolumeSold','TotalDollarVolume','BTCVolume','Proceeds','Trades','TradePeriods','Days']
month_stats_df = pd.DataFrame(monthly_stats,columns=columns)
month_stats_df['DollarVolumeBought'] = month_stats_df['DollarVolumeBought']/1000
month_stats_df['WeightedAverageSpread'] = month_stats_df['WeightedAverageSpread']*100
month_stats_df['DollarVolumeSold'] = month_stats_df['DollarVolumeSold']/1000
month_stats_df['TotalDollarVolume'] = month_stats_df['TotalDollarVolume']/1000
month_stats_df['BTCVolume'] = month_stats_df['BTCVolume']/1000
month_stats_df['Proceeds'] = month_stats_df['Proceeds']/1000
print(month_stats_df.head(20))
print(month_stats_df.tail())

month_stats_df.to_csv("Case1_Monthly_Trade_StatsBT.csv",index=False)
'''
month_stats_df['DollarVolumeBought'] = month_stats_df['DollarVolumeBought'].apply(lambda x: '$'+str(round(x,2)))
month_stats_df['DollarVolumeSold'] = month_stats_df['DollarVolumeSold'].apply(lambda x: '$'+str(round(x,2)))
month_stats_df['TotalDollarVolume'] = month_stats_df['TotalDollarVolume'].apply(lambda x: '$'+str(round(x,2)))
month_stats_df['Proceeds'] = month_stats_df['Proceeds'].apply(lambda x: '$'+str(round(x,2)))
month_stats_df['WeightedAverageSpread'] = month_stats_df['WeightedAverageSpread'].apply(lambda x: str(round(x,2))+'%')
month_stats_df['BTCVolume'] = month_stats_df['BTCVolume'].apply(lambda x: str(round(x,2)))
month_stats_df.set_index(keys=['Date'],inplace=True,drop=True)
print(month_stats_df.to_latex(longtable=True))'''