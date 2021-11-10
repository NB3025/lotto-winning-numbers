import pandas as pd


df = pd.read_csv('lotto-winning-numbers.csv', index_col='title')

# print(df.iloc[0])
print(df.index[0])
# print(int(df.iloc[0]['title']))