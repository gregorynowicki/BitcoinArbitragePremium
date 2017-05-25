import pandas as pd
import os

month_stats = []

base = "C:\\Honors_Thesis\\Cleaned_Files\\"
for year in [2010,2011,2012,2013,2014,2015,2016,2017]:
    if year==2010:
        months = [7,8,9,10,11,12]
    elif year == 2017:
        months = [1,2]
    else:
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
    for month in months:
        print("Year: {} Month: {}".format(year,month))
        path = base+os.path.join(str(year),str(month),"AggAgg5Rm_"+str(year)+"_"+str(month)+".csv")
        tempDF = pd.read_csv(path)
        tempDF = tempDF.loc[pd.notnull(tempDF['Price'])]
        tempDF = tempDF.loc[pd.notnull(tempDF['Volume'])]
        record = []
        record.append(str(year)+'-'+str(month)+'-01')
        record.append(sum(tempDF['Price']*tempDF['Volume']))
        record.append(len(tempDF))
        record.append(len(tempDF.Exchange.drop_duplicates()))
        record.append(sum(tempDF['Price']*tempDF['Volume'])/sum(tempDF['Volume']))
        month_stats.append(record)

columns = ['Date','DollarVolume','Transactions','Exchanges','WeightAveragePrice']
monthly_stats = pd.DataFrame(month_stats,columns=columns)
monthly_stats.to_csv("Monthly_Exchange_Statistics.csv",index=False)