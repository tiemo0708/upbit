import time
import datetime

VERSION = 0.2
COIN = "BTC"
FIAT = "KRW"
TICKER = f"{FIAT}-{COIN}"

f = open("./upbit.key")
lines = f.readlines()
f.close()
@@ -28,12 +33,12 @@ def run(self):
            krw_balance = None 
            btc_balance = None 
            for balance in balances:
                if balance['currency'] == "KRW" and balance['unit_currency'] == "KRW":
                if balance['currency'] == "KRW" and balance['unit_currency'] == FIAT:
                    krw_balance= balance
                if balance['currency'] == "BTC" and balance['unit_currency'] == "KRW":
                if balance['currency'] == COIN and balance['unit_currency'] == FIAT:
                    btc_balance= balance

            btc_price = pyupbit.get_current_price("KRW-BTC")        
            btc_price = pyupbit.get_current_price(TICKER)        
            self.timeout.emit((btc_price, krw_balance, btc_balance))
            self.sleep(1)

@@ -61,7 +66,7 @@ def __init__(self):
        self.worker.start()

        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle("업비트 물타기봇 v1.0")
        self.setWindowTitle(f"업비트 물타기봇 v{VERSION}")
        self.create_table_widget()

        widget = QWidget()
@@ -111,11 +116,11 @@ def __init__(self):
        self.btn_start = QPushButton("무한매수 시작")
        self.btn_start.clicked.connect(self.start)

        #self.btn_sell = QPushButton("일괄 매도")
        #self.btn_sell.clicked.connect(self.sell)
        self.btn_reload = QPushButton("데이터 불러오기")
        self.btn_reload.clicked.connect(self.reload)

        layout_hbox.addWidget(self.btn_start)
        #layout_hbox.addWidget(self.btn_sell)
        layout_hbox.addWidget(self.btn_reload)
        layout_hbox.addStretch(2)

        self.plain_text = QPlainTextEdit()
@@ -146,6 +151,15 @@ def update_data(self, data):
            self.initialize_unit_seed()
            self.initialized = True 

    def reload(self):
        """database로부터 주요 파라미터를 로드하는 함수
        """
        with open("database.txt", "r") as f:
            lines = f.readlines()
            self.unit_num = int(lines[0].strip())
            self.unit_seed = float(lines[1].strip()) 
            self.plain_text.appendPlainText("database 로드 완료")

    def start(self):
        """무한매수 시작 버튼에 대한 slot
        """
@@ -167,7 +181,7 @@ def trigger_order(self):

            # 비트코인 잔고가 0이면 거래일 익절을 의미
            # 새로 파라미터 초기화 
            btc_balance = upbit.get_balance("KRW-BTC")
            btc_balance = upbit.get_balance(TICKER)
            if btc_balance == 0:
                self.initialize_unit_seed()

@@ -178,21 +192,27 @@ def trigger_order(self):
    def order(self):
        # buy bitcoin when current price is less than average buy price 
        if self.btc_avg_buy_price == 0 or self.btc_cur_price < self.btc_avg_buy_price:
            upbit.buy_market_order("KRW-BTC", self.unit_seed)
            upbit.buy_market_order(TICKER, self.unit_seed)
            self.unit_num -= 1

        # 매수 후 평단 재계산 
        # 지정가 매도 
        balance_dict = upbit.get_balance("KRW-BTC", verbose=True)
        balance_dict = upbit.get_balance(TICKER, verbose=True)
        self.btc_avg_buy_price = float(balance_dict['avg_buy_price'])
        volume = balance_dict['balance']

        price = self.btc_avg_buy_price * (1 + self.profit_ratio * 0.01)
        # 호가 규칙 적용 
        price = pyupbit.get_tick_size(price)
        self.order_data = upbit.sell_limit_order("KRW-BTC", price, volume)
        self.order_data = upbit.sell_limit_order(TICKER, price, volume)
        print(self.order_data)

        # backup 
        with open("database.txt", "w") as f:
            f.write(str(self.unit_num) + '\n')
            f.write(str(self.unit_seed) + '\n')
            self.plain_text.appendPlainText("database 쓰기 완료")

    def cancel_order(self):
        try:
            uuid = self.order_data['uuid']