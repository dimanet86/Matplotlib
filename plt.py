import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# data loading
data = pd.read_csv('AB_NYC_2019.csv')

"""
Task 1: Neighbourhood Distribution of Listings  
Create a bar plot to show the distribution of listings across different neighbourhood_group.
"""
# Preparing data

data1 = data.groupby('neighbourhood_group')['id'].count()

# Actually plot
nbhgrps = data1.index.to_numpy()
counts = data1.to_numpy()
fig, ax = plt.subplots()
bar_labels = list(counts.astype(int))
bar_colors = ['tab:brown', 'tab:blue', 'tab:red', 'tab:orange', 'tab:green']
ax.bar(nbhgrps, counts, label=bar_labels, color=bar_colors)
ax.set_xlabel('Neighbourhoods')
ax.set_ylabel('Count of listings')
ax.set_title('Distribution of listings by neighbourhood group')
ax.legend(title='Distribution of listings')
plt.show()

"""
Task 2: Price Distribution Across Neighborhoods
Plot: Generate a box plot to display the distribution of price within each neighbourhood_group.
Create a bar plot to show the distribution of listings across different neighbourhood_group.
"""
neighbourhoods = data['neighbourhood_group'].unique()
prices = []
for neighbourhood_group in neighbourhoods:
    prices.append(data[data['neighbourhood_group']==neighbourhood_group]['price'].to_numpy())

labels = list(neighbourhoods)
colors = ['peachpuff', 'orange', 'tomato', 'yellow', 'blue']

fig, ax = plt.subplots()
ax.set_xlabel('Neighbourhoods')
ax.set_ylabel('Prices ($)')

flierprops = dict(marker='o', markerfacecolor='b', markersize=4, linestyle='none')

bplot = ax.boxplot(prices,
                   patch_artist=True,  
                   tick_labels=labels,
                   flierprops=flierprops) 

# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

plt.show()

"""
Task 3: Room Type vs. Availability
Plot: Create a grouped bar plot to show the average availability_365 for each room_type across the neighborhoods.
"""

