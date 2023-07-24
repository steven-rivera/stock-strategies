## About

This program utilizes the Alpha Vantage API to obtain past stock prices and uses this 
data to calculate some metrics summarizing those prices, and ultimately report on potentially opportune 
times to buy or sell the stock, based on one of a few automated buying-and-selling strategies. 


## Indicators

The core of yjr analysis will be comparing daily price and volume data against the values of 
indicators. There are three kinds of indicators used:

| Indicators            | Description                                                                                                                                                                                                                                                                                                                                             | 
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| True range            | The range of prices (highest price minus lowest price) for the current day, including any movement since the previous day's close.                                                                                                                                                                                                                      |
| Simple moving average | The *N-day simple moving average* at the end of a particular day is the average of the most recent N closing prices. Days on which there is no trading are not counted.                                                                                                                                                                                 |
| Directional indicator | The *N-day directional indicator* for a stock is the number of closing prices out of the most recent N on which the stock's price went up (i.e., it closed at a higher price than the previous close) *minus* the number of days out of the most recent N on which the stock's price went down (i.e., closed at a lower price than the previous close). |


## Requirements 

This program requires an Aplha Vantage API key which can gotten [here](https://www.alphavantage.co/support/#api-key). Once API key is 
obtained, place the key in a file named `apikey.txt`


## How to Run

- `python main.py`