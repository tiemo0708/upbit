import time
import pandas
import pyupbit
import datetime

access = "jwGN9gGJ7aX9ZtHTZfYo3pXr81QIdZjW5kjMpvZx"
secret = "KurZYaCvxWOvGhvwWn9vqfE8RAp0q4aN4ffyBACX"

upbit = pyupbit.Upbit(access, secret)

# print(upbit.get_balance("KRW"))
# print(upbit.get_balance("KRW-XRP"))

# 이용할 코인 리스트
coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-BCH", "KRW-EOS"] # Coin ticker 추가
lower28 = []
higher70 = []

# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)


def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")  

# 시장가 매수 함수
def buy(coin):
    money = upbit.get_balance("KRW")
    if money < 20000 :
        res = upbit.buy_market_order(coin, money*0.9995)
    elif money < 50000:
        res = upbit.buy_market_order(coin, money*0.4)
    elif money < 100000 :
        res = upbit.buy_market_order(coin, money*0.3)
    else :
        res = upbit.buy_market_order(coin, money*0.2)
    return

# 시장가 매도 함수
def sell(coin):
    amount = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin)
    total = amount * cur_price
    if total < 20000 :
        res = upbit.sell_market_order(coin, amount*0.9995)
    elif total < 50000:
        res = upbit.sell_market_order(coin, amount*0.4)
    elif total < 100000:
        res = upbit.sell_market_order(coin, amount*0.3)        
    else :
        res = upbit.sell_market_order(coin, amount*0.2)
    return

    
while(True): 
    for i in range(len(coinlist)):
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
        now_rsi = rsi(data, 14).iloc[-1]
        print("코인명: ", coinlist[i])
        print("현재시간: ", datetime.datetime.now())
        print("RSI :", now_rsi)
        print()
        if now_rsi <= 28 : 
            lower28[i] = True
        elif now_rsi >= 33 and lower28[i] == True:
            buy(coinlist[i])
            lower28[i] = False
        elif now_rsi >= 70 and higher70[i] == False:
            sell(coinlist[i])
            higher70[i] = True
        elif now_rsi <= 60 :
            higher70[i] = False
    time.sleep(1)
