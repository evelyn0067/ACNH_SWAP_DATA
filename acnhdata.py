import streamlit as st
import pandas as pd
import requests
from PIL import Image
import datetime
c1,c2 = st.columns([1,8])
c1.image(Image.open('Group 38042.png'))
c2.header('Swap ACNH, Win a Share of 50 AR!')
st.subheader('How to partcipate')
st.markdown(
    '''
       During the campaign period, the top 30 accounts with the highest ACNH trading amount (buys or sells ) on 
       Permaswap will be qualified to win a share of 50 AR!
       Swap Now!
    '''
)
st.subheader('Campagin Period')
st.markdown(
    '''10:00:00 on April 14, 2023 to 10:00:00 on April 20, 2023 (UTC)'''
)

def get_order_data():
    combined_df = pd.DataFrame()
    for x in range(1,100000):
        x = str(x)
        url = "https://router.permaswap.network/orders/?page=" + x
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data['orders'])
        combined_df = pd.concat([combined_df, df])
        print(url)
        date_obj = datetime.date(2023, 4, 12)
        datetime_obj = datetime.datetime.combine(date_obj, datetime.time.min)
        end_data = int(datetime_obj.timestamp() * 1000)
        print(combined_df.iloc[-1]['timestamp'],end_data)
        if combined_df.iloc[-1]['timestamp'] < end_data:
            break
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], unit='ms')
    combined_df.sort_values("id")
    combined_df = combined_df.rename({'timestamp': 'Time', 'address': 'Address','tokenInTag':'In Token','tokenOutTag':'Out Token','tokenInAmount':'In Token Amount','tokenOutAmount':'Out Token Amount','price':'Price'}, axis=1)
    print(combined_df)
    frame = combined_df.loc[:,['Time','Address','everHash','In Token','Out Token','In Token Amount','Out Token Amount','Price']]
    frame = frame.replace('arweave,ethereum-ar-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,0x4fadc7a98f2dc96510e42dd1a74141eeae0c1543', 'AR')
    frame = frame.replace('arweave-ardrive--8A6RexFkpfWwuyVO98wzSFZh0d6VJuI-buTJvlwOJQ', 'ARDRIVE')
    frame = frame.replace('ethereum-eth-0x0000000000000000000000000000000000000000', 'ETH')
    frame = frame.replace('ethereum-usdc-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'USDC')
    frame = frame.replace('ethereum-usdt-0xdac17f958d2ee523a2206206994597c13d831ec7', 'USDT')
    frame = frame.replace('everpay-acnh-0x72247989079da354c9f0a6886b965bcc86550f8a', 'ACNH')
    frame[['Price','In Token Amount','Out Token Amount']] = frame[['Price','In Token Amount','Out Token Amount']].astype(float)
    return frame

def get_token_order(symbol,dataframe):
    df1 = dataframe[(dataframe['In Token']==symbol)]
    df1 = df1.loc[:,['Address','In Token','In Token Amount']]
    df3 = df1.rename({'In Token':'Token','In Token Amount':'ACNH Swap Amount'},axis=1)
    print(df3)
    df3 = df3.loc[:,['Address','ACNH Swap Amount']]
    df2 = dataframe[(dataframe['Out Token']==symbol)]
    df2 = df2.loc[:,['Address','Out Token','Out Token Amount']]
    df4 = df2.rename({'Out Token':'Token','Out Token Amount':'ACNH Swap Amount'},axis=1)
    df4 = df4.loc[:,['Address','ACNH Swap Amount']]
    df5 = pd.concat([df3,df4])
    df = df5.groupby('Address').sum()
    df = df.sort_values("ACNH Swap Amount",ascending=False)
    rank_list=[]
    rewards_list=['10AR','7AR','4AR']
    for x in range(0,len(df)):
        rank_list.append('Top'+str(x+1))
        if x > 29:
            rewards_list.append('Sorry')
        elif x > 19:
            rewards_list.append('0.5AR')
        elif x > 9:
            rewards_list.append('1AR')
        elif x > 2 :
            rewards_list.append('2AR')  
    df['Rank']= rank_list
    df['Rewards'] = rewards_list
    add_emoji = lambda x: '🏅' + x if isinstance(x,str) else x
    df['Rank'] = df['Rank'].apply(add_emoji)
    df['Address'] = df.index
    frame = df.set_index('Rank', drop = True)
    return frame


# apply the function to the dataframe and display it
data = get_order_data()
df = get_token_order(symbol='ACNH',dataframe=data)


st.dataframe(df,use_container_width=False)

