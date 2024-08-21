import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

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
# NB: I preferred neighbourhoods_grops to neighbourhoods because of amount of neighbourhoods (it's large)
room_types = tuple(data['room_type'].unique())
neighbourhood_groups = tuple(data['neighbourhood_group'].unique())

averages = {}
std_devs = {}
for room_type in room_types:
    grouped_data = data[data['room_type'] == room_type].groupby('neighbourhood_group')['availability_365']
    averages[room_type] = grouped_data.mean()
    std_devs[room_type] = grouped_data.std()  # Calculate standard deviation

x = np.arange(len(neighbourhood_groups))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute in room_types:
    offset = width * multiplier
    rects = ax.bar(x + offset, averages[attribute], width, label=attribute, yerr=std_devs[attribute], capsize=5)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Days')
ax.set_title('Availability by neighbourhood groups')
ax.set_xticks(x + width, neighbourhood_groups)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 250)

plt.show()

"""
4. Correlation Between Price and Number of Reviews
Plot: Develop a scatter plot with price on the x-axis and number_of_reviews on the y-axis.
"""
# wo  regression line - sorry, had not enough time
fig, ax = plt.subplots()
for room_type, color in zip(room_types, ['tab:blue', 'tab:orange', 'tab:green']):
    x, y = data[data['room_type'] == room_type][['price', 'reviews_per_month']].T.values
    ax.scatter(x, y, c=color, label=room_type,
               alpha=0.5, edgecolors='none')

ax.legend()
ax.grid(True)
ax.set_xlabel('Price')
ax.set_ylabel('Number of reviews')
ax.set_title('Correlation between Price and Number of Reviews')
plt.show()

"""
5. Time Series Analysis of Reviews
Plot: Create a line plot to show the trend of number_of_reviews over time (last_review) for each neighbourhood_group.
"""
# This task so far doesn't make sense for me. number_of_reviews column is a number of reviews for particular listing 
# (total, not over time)
# last_review column is also column designating date of last review for particular room, but I cannot 'dissect' number of 
# reviews over time, at least I cannot see how to aquire this data now.
# Would you be so kind to give a little clue on this in a review? Thank you. 

data['ones'] = [1 for i in range(data.shape[0])]
time_data = data.copy()
time_data['last_review'] = pd.to_datetime(time_data['last_review'], errors='coerce')
time_data = time_data[time_data['last_review'].notna()] # let's get rid of rows with NaT in last-review cells. 
time_data.set_index('last_review', inplace=True)
time_data = time_data[['neighbourhood_group', 'price', 'ones']]
time_data.groupby('neighbourhood_group').resample('ME').sum()

"""
6. Price and Availability Heatmap
Plot: Generate a heatmap to visualize the relationship between price and availability_365 across different neighborhoods.
Details: Use a color gradient to represent the intensity of the relationship, label the axes, and include a color bar for reference.
"""
# Again after trying some approaches, I cannot understand how can I group and aggregate data for heatmap
# Looks like it makes no sense in relating columns in question with each other:
# I can group data by neighbourhoods, but it looks like that it's impossible to group data further
# to obtain correct domain and range for heatmap
# I only can kindly ask if reviwer could give a clue in review, if I am wrong. Thank you.

aggregate = data.groupby('neighbourhood_group')['price'].mean()
avg_price = []
groups = []
availability = []

"""
7. Room Type and Review Count Analysis
Plot: Create a stacked bar plot to display the number_of_reviews for each room_type across the neighbourhood_group.
Details: Stack the bars by room type, use different colors for each room type, and add titles, axis labels, and a legend.
"""
room_types = tuple(data['room_type'].unique()) # species
neighbourhood_groups = tuple(data['neighbourhood_group'].unique())
grouped_data = data.groupby(['room_type', 'neighbourhood_group'])['number_of_reviews'].mean()
weight_counts = {x: [] for x in neighbourhood_groups}

for neighbourhood_group in neighbourhood_groups:
    for room_type in room_types:
        weight_counts[neighbourhood_group].append(grouped_data[(room_type, neighbourhood_group)])

width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(room_types, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Number_of_reviews for each room_type across the neighbourhood_group.")
ax.legend(loc="upper right")

plt.show()