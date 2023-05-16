import datetime as dt

import requests as rq

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

symbol = 'ETCUSDT'
TIME_start = dt.datetime(2023, 2, 15, 0, 0, 0)
TIME_end = dt.datetime(2023, 4, 15, 0, 0, 0)

url = f'https://api.binance.com/api/v1/klines?symbol={symbol}&interval=1m&startTime={int(TIME_start.timestamp()) * 1000}&endTime={int(TIME_end.timestamp()) * 1000}&limit=1000'
res = rq.request('GET', url)
raw_data = pd.DataFrame.from_records(res.json()).iloc[:200, 1].map(float)
data = raw_data.to_numpy()

raw_data.plot()


def exponential_smoothing(data, alpha):

    smoothed_data = data[0]

    for i in range(1, len(data)):
        smoothed_data = alpha * data[i] + (1 - alpha) * smoothed_data

    return smoothed_data


def modified_exponential_smoothing(data, window_size, alpha):
    initial_data = data.copy()
    for i in range(window_size, len(data)):
        current_window = data[i - window_size:i]
        forecast = exponential_smoothing(current_window, alpha)

        initial_data[i - 1] = forecast

    return initial_data


plt.plot(modified_exponential_smoothing(data,10, 0.1))
plt.show()
