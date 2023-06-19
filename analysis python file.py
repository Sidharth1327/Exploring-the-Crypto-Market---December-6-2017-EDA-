# %% [markdown]
# # Data Analysis on Crypto Currency Market

# %%
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
df = pd.read_csv('coinmarketcap_06122017.csv')
print(df.head())

# %%
print(df.info())

# %% [markdown]
# We can observe that there are clearly a lot of issing values in certain coloumns.

# %%
df['name'].nunique()

# %% [markdown]
# So, here we can see that almost the cryptos are unique except two crypto have repeated. 

# %%
df[df['market_cap_usd'].isna()]

# %% [markdown]
# There are almost 295 rows which are filled with NaN. From the overview of the data, it can be interpreted as this are thos cryptos which doesnt even have capitalisation.Hence we can drop these values and analize the left data.

# %%
market_cap = df[['id', 'market_cap_usd']]
market_cap = market_cap[ market_cap['market_cap_usd'] > 0 ] 
market_cap_new = market_cap[ market_cap['market_cap_usd'] > 0 ] 

# %% [markdown]
# So we have eliminated almost all the values of those cryptos which didnt even had market capitalisation because it doesnt gonna affect much in the analysis we are doing. Now that we got the data correct, time to do some Exploratory Data Analysis.

# %%

market_cap = market_cap.head(10)
market_cap['market_cap_per'] = (market_cap['market_cap_usd']/market_cap['market_cap_usd'].sum()) *100
fig, ax = plt.subplots(figsize=(10, 6))
wedges, texts, autotexts = ax.pie(market_cap['market_cap_per'], labels=market_cap['id'], wedgeprops=dict(width=0.4), autopct='')
ax.set_title("Top 10 Cryptos")

# Adding percentage labels outside the donut
percentage_labels = [f'{p:.1f}%' for p in market_cap['market_cap_per']]
ax.legend(wedges, percentage_labels, loc='upper right', bbox_to_anchor=(1, 0, 0.5, 1))


plt.show()

# %% [markdown]
# You have definitely heard about the danger in investing in cryptos right. Ok, Lets analyze from the given data that how volatile the Crypto field is?
# 
# For analyzing this, we can hover over the feature price change in 1 day and also price change in 1 week.

# %%
change = df[['id', 'percent_change_24h', 'percent_change_7d']].dropna().set_index('id')
change = change.sort_values('percent_change_24h')
change.head()

# %%
def top10_subplot(change_col, title, plot_type):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    ax1 = axes[0]
    change_col[:10].plot(kind=plot_type, color='green', ax=ax1)
    ax1.set_ylabel('% change')
    ax1.set_title('Top 10 Losers')
    ax1.grid(axis='y', linestyle='--')
    ax2 = axes[1]
    change_col[-10:].plot(kind=plot_type, color='red', ax=ax2)
    ax2.set_ylabel('% change')
    ax2.set_title('Top 10 Winners')
    ax2.grid(axis='y', linestyle='--')
    fig.suptitle(title)
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig
Ttile_1 = "24 hours top losers and winners"
fig = top10_subplot(change.percent_change_24h, Ttile_1, 'bar')


# %%
Title_2 = "Weekly top losers and winners"

# Calling the top10_subplot function
fig = top10_subplot(change.percent_change_7d, Title_2,'bar')

# %% [markdown]
# Since there are lot of cryptos upcoming and lot of them are already establsihed, we will just look which all cryptos are very bigger, then somewhat lies in the mid level and also in the bottom level.

# %%

def count_market_caps(query_string):
    return market_cap_new.query(query_string).count().id

categories = ["Large", "Medium", "Small"]

large_caps = count_market_caps('market_cap_usd > 3E+8')
medium_caps = count_market_caps('market_cap_usd >= 5E+7 & market_cap_usd < 3E+8')
small_caps = count_market_caps('market_cap_usd < 5E+7')

values = [large_caps, medium_caps, small_caps]

plt.bar(range(len(values)), values, tick_label=categories)


