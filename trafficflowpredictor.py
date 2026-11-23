import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Metro_Interstate_Traffic_Volume.csv")
df['date_time'] = pd.to_datetime(df['date_time'], format='%d-%m-%Y %H:%M')

df = df.drop_duplicates(subset=['date_time']).sort_values('date_time')
df['temp_f'] = ((df['temp'] - 273.15) * (1.8)) + 32
df['temp_c'] = df['temp'] - 273.15
df.drop(columns=['temp'])