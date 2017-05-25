import pandas as pd
import os

raw = pd.read_csv("GDAX_Total.csv")
print("Handling TradeDates...")
raw['TradeDate'] = raw.time.apply(lambda x: pd.to_datetime(x).strftime("%m/%d/%Y %H:%M:%S"))#raw['time'].apply(lambda x: pd.to_datetime((pd.to_datetime(x)).strftime("%m/%d/%Y %H:%M:%S %p")))

print("Handling TradeDates...still...")
raw['TradeDate'] = pd.to_datetime(raw.TradeDate)
raw['Exchange'] = "gdaxUSD"
raw['Price'] = raw['price']
raw['Volume'] = raw['size']
curr_df = raw[['TradeDate','Price','Volume','Exchange']]
raw = []

print("Handling Month/Year Columns...")
curr_df['Year'] = curr_df['TradeDate'].apply(lambda x: x.year)
curr_df['Month'] = curr_df['TradeDate'].apply(lambda x: x.month)
print(curr_df.head())

for year in range(min(curr_df['Year']),max(curr_df['Year'])+1):
    tempDF = curr_df.loc[curr_df['Year']==year]
    for month in range(min(tempDF['Month']),max(tempDF['Month'])+1):
        print("Sorting out: {}-{}".format(month,year))
        tempDF2 = tempDF.loc[tempDF['Month'] == month]

        file_path = os.path.join("C:\\","Honors_Thesis","Cleaned_Files",str(year),str(month))

        name = "gdaxUSD_"+str(year)+"_"+str(month)+".csv"
        file_name = os.path.join(file_path,name)
        print(file_name)
        tempDF2 = tempDF2[["TradeDate","Price","Volume","Exchange"]]
        tempDF2.to_csv(file_name,index=False)

raw.to_csv("gdaxUSD.csv")