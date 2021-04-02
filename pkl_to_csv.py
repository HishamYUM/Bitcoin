import pandas as pd
import pickle as pkl
import csv
from datetime import datetime
with open("LTC-BTC.pkl", "rb") as f:
    object = pkl.load(f)
    
df = pd.DataFrame(object)
df.to_csv(r'LTC-BTC.csv')
data = pd.read_csv("LTC-BTC.csv", sep="\t")
with open("BTC-USD.pkl", "rb") as f:
    object = pkl.load(f)
    
df = pd.DataFrame(object)
df.to_csv(r'BTC-USD.csv')
ALPHA = pd.read_csv("BTC-USD.csv", sep="\t")

