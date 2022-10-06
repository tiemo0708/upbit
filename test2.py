import time
import pandas
import pyupbit
import datetime

access = "jwGN9gGJ7aX9ZtHTZfYo3pXr81QIdZjW5kjMpvZx"
secret = "KurZYaCvxWOvGhvwWn9vqfE8RAp0q4aN4ffyBACX"

upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW"))
print(upbit.get_balance("KRW-XRP"))