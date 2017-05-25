import pandas as pd



file = 'C:\\Honors_Thesis\\Case2\\Agg5RmTradeLog_'
total_months=0
for year in [2010,2011,2012,2013,2014,2015,2016,2017]:
    if year==2010:
        months = [7,8,9,10,11,12]
    elif year == 2017:
        months = [1,2]
    else:
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
    for month in months:
        file_name = file+str(year)+'_'+str(month)+'.csv'
        print("Year: {} - Month: {}".format(year, month))
        if year==2010 and month==7:
            raw = pd.read_csv(file_name)
        tempDF = pd.read_csv(file_name)
        raw = raw.append(tempDF)
        total_months+=1

raw = raw.loc[raw['AmountTraded']>0]
raw.to_csv('Case2_Full_Trade_Log.csv',index=False)

print("Length: {}".format(len(raw)))
print("Months: {}".format(total_months))