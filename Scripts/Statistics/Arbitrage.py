import pandas as pd
import os
import numpy as np
import time


###########################################################
#        Add Exchange Name and Amount Able to Sell        #
###########################################################
#    Also Check to make sure the transactions are right   #
###########################################################
for year in [2014,2015]:#,2016,2017]:
    if year == 2010:
        months = [7,8,9,10,11,12]
    elif year == 2017:
        months = [1,2]
    else:
        months = [1,2,3,4,5,6,7,8,9,10,11,12]

    for month in months:

        CASE = 2                # Case 1 # Case 2 # Case 3 # Case 4 # Case 5 # Case 6
        MINS_PRIOR = 15          #   5    #   15   #   20   #   15   #   15   #  15
        MINS_AFTER = MINS_PRIOR #        #        #        #        #        #
        MINS_DELAY = 10          #   0    #   0    #   5    #   1    #   3    #  5
        short_exposure=1

        # Transaction time constraints
        use_mean = 1


        TradeLog = pd.DataFrame()

        base_dir = os.path.join("C:\\","Honors_Thesis","Cleaned_Files")
        month_dir = os.path.join(base_dir,str(year),str(month))
        file_dir = os.path.join(month_dir,"AggAgg5Rm_"+str(year)+"_"+str(month)+".csv")

        month_data = pd.read_csv(file_dir)

        # Convert TradeDate Datatype
        month_data['TradeDate'] = pd.to_datetime(month_data['TradeDate']).astype(np.int64)/(1e9)
        month_data['TradeDate'] = month_data['TradeDate'].astype(int)
        # Make a Transaction ID
        month_data["TID"] = range(0,len(month_data))
        # Create a list of exchanges
        exchanges = month_data['Exchange'].drop_duplicates().tolist()
        transactions = month_data
        # Start out eveything not traded
        transactions['Traded'] = 0 # 0: Not Traded; 1: Partially Traded; 2: Fully Traded; 9: Could not be traded
        transactions['Pos'] = 0
        transactions['AmountAvailable'] = transactions['Volume']
        AvailableTrades = transactions.loc[transactions['Traded']!=2]
        AvailableTrades = AvailableTrades.loc[AvailableTrades['Traded']!=9]

        BuyCandidates = AvailableTrades.loc[AvailableTrades['Pos'] != -1]
        BuyCandidates = BuyCandidates.sort_values(by='Price', ascending=True).reset_index(drop=True)

        while len(BuyCandidates)>0:
            TradeDetails = []
            # Keep only the securities ready to trade

            if len(BuyCandidates)%100==0:
                print("Year: {} Month: {} Length of BC: {}".format(year,month,int(len(BuyCandidates)/100)))
            SellCandidates = AvailableTrades.loc[AvailableTrades['TID']!=BuyCandidates.loc[0,'TID']]
            SellCandidates = SellCandidates.loc[SellCandidates['Pos']!=1]
            SellCandidates = SellCandidates.loc[SellCandidates['Exchange']!=BuyCandidates.loc[0,'Exchange']]

            SellCandidates = SellCandidates.loc[SellCandidates['TradeDate']>(BuyCandidates.loc[0,'TradeDate']-60*MINS_PRIOR)]
            SellCandidates = SellCandidates.loc[SellCandidates['TradeDate']<=(BuyCandidates.loc[0,'TradeDate']+60*MINS_AFTER)]
            if(MINS_DELAY!=0):
                SellCandidates = SellCandidates.loc[SellCandidates['TradeDate']>=(BuyCandidates.loc[0,'TradeDate']+60*MINS_DELAY)]
                #print("Year: {} Month: {} Length: {}".format(year, month, len(SellCandidates)))
                #print("Buy: {}".format(BuyCandidates.loc[0,'TradeDate']+60*MINS_AFTER-(BuyCandidates.loc[0,'TradeDate']+60*MINS_DELAY)))
                #SellCandidates2 = SellCandidates.loc[SellCandidates['TradeDate']<=(BuyCandidates.loc[0,'TradeDate']-60*MINS_DELAY)]
                #SellCandidates = SellCandidates1.append(SellCandidates2)
            SellCandidates = SellCandidates.sort_values(by='Price',ascending=False).reset_index(drop=True)

            #print(BuyCandidates)
            if len(SellCandidates) > 0:
                if BuyCandidates.loc[0,'AmountAvailable']>SellCandidates.loc[0,'AmountAvailable']:

                    # Set their position type Long/Short (1/-1)
                    transactions.loc[transactions['TID']==BuyCandidates.loc[0,'TID'],'Pos'] = 1
                    transactions.loc[transactions['TID']==BuyCandidates.loc[0,'TID'],'Traded'] = 1
                    transactions.loc[transactions['TID']==BuyCandidates.loc[0,'TID'],'AmountAvailable'] = (BuyCandidates.loc[0,'AmountAvailable']-SellCandidates.loc[0,'AmountAvailable'])

                    amount_traded = SellCandidates.loc[0,'AmountAvailable']
                    transactions.loc[transactions['TID']==SellCandidates.loc[0,'TID'],'Pos'] =-1
                    transactions.loc[transactions['TID']==SellCandidates.loc[0,'TID'],'Traded'] = 2
                    transactions.loc[transactions['TID']==SellCandidates.loc[0,'TID'],'AmountAvailable'] = 0

                    # columns = ['BuyPrice','SellPrice','BuyDate','SellDate','BuyExchange','SellExchange','Volume']
                    TradeDetails.append(BuyCandidates.loc[0,'Price'])
                    TradeDetails.append(SellCandidates.loc[0,'Price'])
                    TradeDetails.append(BuyCandidates.loc[0,'TradeDate'])
                    TradeDetails.append(SellCandidates.loc[0,'TradeDate'])
                    TradeDetails.append(BuyCandidates.loc[0,'Exchange'])
                    TradeDetails.append(SellCandidates.loc[0,'Exchange'])
                    TradeDetails.append(amount_traded)
                    TradeDetails.append(1)
                    TradeLog = TradeLog.append(pd.DataFrame(TradeDetails).transpose())
                    #print("TRADE LOG")
                    #print(TradeLog)
                elif BuyCandidates.loc[0,'AmountAvailable']<SellCandidates.loc[0,'AmountAvailable']:

                    amount_traded = BuyCandidates.loc[0,'AmountAvailable']
                    transactions.loc[transactions['TID']==SellCandidates.loc[0,'TID'],'Pos'] =-1
                    transactions.loc[transactions['TID']==SellCandidates.loc[0,'TID'],'Traded'] = 1
                    transactions.loc[transactions['TID']==SellCandidates.loc[0,'TID'],'AmountAvailable'] = (SellCandidates.loc[0,'AmountAvailable']-BuyCandidates.loc[0,'AmountAvailable'])

                    # Set their position type Long/Short (1/-1)
                    transactions.loc[transactions['TID']==BuyCandidates.loc[0,'TID'],'Pos'] = 1
                    transactions.loc[transactions['TID']==BuyCandidates.loc[0,'TID'],'Traded'] = 2
                    transactions.loc[transactions['TID']==BuyCandidates.loc[0,'TID'],'AmountAvailable'] = 0

                    # columns = ['BuyPrice','SellPrice','BuyDate','SellDate','BuyExchange','SellExchange','Volume']
                    TradeDetails.append(BuyCandidates.loc[0,'Price'])
                    TradeDetails.append(SellCandidates.loc[0,'Price'])
                    TradeDetails.append(BuyCandidates.loc[0,'TradeDate'])
                    TradeDetails.append(SellCandidates.loc[0,'TradeDate'])
                    TradeDetails.append(BuyCandidates.loc[0,'Exchange'])
                    TradeDetails.append(SellCandidates.loc[0,'Exchange'])
                    TradeDetails.append(amount_traded)
                    TradeDetails.append(2)
                    TradeLog = TradeLog.append(pd.DataFrame(TradeDetails).transpose())

                elif BuyCandidates.loc[0,'AmountAvailable']==SellCandidates.loc[0,'AmountAvailable']:
                    amount_traded = BuyCandidates.loc[0, 'AmountAvailable']
                    transactions.loc[transactions['TID'] == SellCandidates.loc[0, 'TID'], 'Pos'] = -1
                    transactions.loc[transactions['TID'] == SellCandidates.loc[0, 'TID'], 'Traded'] = 2
                    transactions.loc[transactions['TID'] == SellCandidates.loc[0, 'TID'], 'AmountAvailable'] = 0

                    # Set their position type Long/Short (1/-1)
                    transactions.loc[transactions['TID'] == BuyCandidates.loc[0, 'TID'], 'Pos'] = 1
                    transactions.loc[transactions['TID'] == BuyCandidates.loc[0, 'TID'], 'Traded'] = 2
                    transactions.loc[transactions['TID'] == BuyCandidates.loc[0, 'TID'], 'AmountAvailable'] = 0

                    # columns = ['BuyPrice','SellPrice','BuyDate','SellDate','BuyExchange','SellExchange','Volume']
                    TradeDetails.append(BuyCandidates.loc[0, 'Price'])
                    TradeDetails.append(SellCandidates.loc[0, 'Price'])
                    TradeDetails.append(BuyCandidates.loc[0, 'TradeDate'])
                    TradeDetails.append(SellCandidates.loc[0, 'TradeDate'])
                    TradeDetails.append(BuyCandidates.loc[0, 'Exchange'])
                    TradeDetails.append(SellCandidates.loc[0, 'Exchange'])
                    TradeDetails.append(amount_traded)
                    TradeDetails.append(3)
                    TradeLog = TradeLog.append(pd.DataFrame(TradeDetails).transpose())
            else:
                transactions.loc[transactions['TID'] == BuyCandidates.loc[0, 'TID'], 'Traded'] = 9
            AvailableTrades = transactions.loc[transactions['Traded'] != 2]
            AvailableTrades = AvailableTrades.loc[AvailableTrades['Traded'] != 9]
            # Sort by price BuyCandidates
            BuyCandidates = AvailableTrades.loc[AvailableTrades['Pos']!=-1]
            BuyCandidates = BuyCandidates.sort_values(by='Price',ascending=True).reset_index(drop=True)
        if len(TradeLog)!=0:
            TradeLog['BuyPrice'] = TradeLog[0]
            TradeLog['SellPrice'] = TradeLog[1]
            TradeLog['BuyDate'] = TradeLog[2]
            TradeLog['SellDate'] = TradeLog[3]
            TradeLog['BuyExchange'] = TradeLog[4]
            TradeLog['SellExchange'] = TradeLog[5]
            TradeLog['AmountTraded'] = TradeLog[6]
            TradeLog['Type'] = TradeLog[7]
            TradeLog = TradeLog[['BuyPrice','SellPrice','BuyDate','SellDate','BuyExchange','SellExchange','AmountTraded','Type']]

            TradeLog.to_csv("C:\\Honors_Thesis\\Case"+str(CASE)+"\\Agg5RmLongOnlyTradeLog_"+str(year)+"_"+str(month)+".csv",index=False)
        print("Year: {} Month: {} Length: {}".format(year, month, len(TradeLog)))