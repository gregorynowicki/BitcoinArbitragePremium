import requests
import pandas as pd
import time
# 7/20/14
end_time_unix = 1488326400 # First second of 3/1/17
gem_url = "https://api.gemini.com/v1/trades/btcusd?limit_trades=500&since="

r = requests.get(gem_url+str(1))

rd = r.json()
rdf = pd.DataFrame(rd)
rdf.timestamp = rdf.timestamp.apply(lambda x: int(x))

last_trade_time = max(rdf.timestamp)-1
print(rdf.head())
print(last_trade_time)
repeat_bool = True
while (repeat_bool==True):
    try:
        curr_url = gem_url+str(last_trade_time)
        r = requests.get(curr_url)
        rd = r.json()
        trd = pd.DataFrame(rd)
        added = len(trd)
        trd.timestamp = trd.timestamp.apply(lambda x: int(x))
        rdf = rdf.append(trd)
        if(last_trade_time>end_time_unix):
            repeat_bool = False
        last_trade_time = max(trd.timestamp)-1
        # print("Length: {}".format(len(rdf)))
        # print("TID: {}".format(last_trade_id))
        # print("Added: {}".format(added))
        # print("RD: {}".format(rd))
        # print("URL: {}".format(curr_url))
        print("TID: {}".format(max(trd.tid)))
        time.sleep(1)
    except (JSONDecodeError):
        rdf.to_csv("GEM-EXCEPTION-THROWN.csv",index=False)

print("{} Transactions".format(len(rdf)))
# print("Max Timestamp {}".format(max(rdf.timestamp)))
# print("Min Timestamp {}".format(min(rdf.timestamp)))
rdf.to_csv("GEM-Raw.csv",index=False)