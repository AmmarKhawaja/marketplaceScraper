import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt

file_path = 'data/' + '2024-02-23' + '.csv'

df = pd.read_csv(file_path, on_bad_lines = 'warn')

print(df)

count = df['NAME'].value_counts()

count[1:20].plot(kind='bar', color='blue')

plt.tick_params(axis='x', labelsize=3)
print(count.mean())
plt.axhline(y=count.mean(), color='red', linestyle='--', label='Average')

plt.show()
