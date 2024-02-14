import pandas as pd

df = pd.read_csv('./test_empty_data.CSV')

data = df.Temp1
print(data.dropna().values)