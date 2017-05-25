import pandas as pd
import os


raw = pd.read_csv("GEM-Raw.csv")
raw = raw.drop_duplicates().reset_index(drop=True)
raw["Volume"] = raw["amount"]
raw["Price"] = raw["price"]
raw["Exchange"] = "geminiUSD"

print("Handling TradeDates...")
raw["TradeDate"] = pd.to_datetime(raw["timestamp"],unit="s")

curr_df = raw[['TradeDate','Price','Volume','Exchange']]


print("Handling Month/Year Columns...")
curr_df['Year'] = curr_df['TradeDate'].apply(lambda x: x.year)
curr_df['Month'] = curr_df['TradeDate'].apply(lambda x: x.month)

for year in range(min(curr_df['Year']),max(curr_df['Year'])+1):
    tempDF = curr_df.loc[curr_df['Year']==year]
    for month in range(min(curr_df['Month']),max(curr_df['Month'])+1):
        print("Sorting out: {}-{}".format(month,year))
        tempDF2 = tempDF.loc[tempDF['Month'] == month]

        file_path = os.path.join("C:\\","Honors_Thesis","Cleaned_Files",str(year),str(month))

        name = "geminiUSD_"+str(year)+"_"+str(month)+".csv"
        file_name = os.path.join(file_path,name)
        print(file_name)
        tempDF2 = tempDF2[["TradeDate","Price","Volume","Exchange"]]
        tempDF2.to_csv(file_name,index=False)

raw.to_csv("geminiUSD.csv")
