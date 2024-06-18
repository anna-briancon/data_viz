import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('us_tornado_dataset_1950_2021.csv')

df['date'] = pd.to_datetime(df['date'])

df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

tornado_counts = df.groupby('month').size()

num_years = df['year'].nunique()

average_tornado_counts = tornado_counts / num_years

plt.figure(figsize=(10, 6))
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.bar(months, average_tornado_counts, color='skyblue')
plt.title('Moyenne des tornades par mois (1950-2021)')
plt.xlabel('Mois')
plt.ylabel('Nombre moyen de tornades')
plt.grid(True)
plt.savefig('assets/average_tornadoes_per_month.png')
plt.show()
