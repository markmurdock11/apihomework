# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Unit 5 - Financial Planning
# 

# %%
# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation

get_ipython().run_line_magic('matplotlib', 'inline')


# %%
# Load .env enviroment variables
load_dotenv()

# %% [markdown]
# ## Part 1 - Personal Finance Planner
# %% [markdown]
# ### Collect Crypto Prices Using the `requests` Library

# %%
# Set current amount of crypto assets
# YOUR CODE HERE!
my_btc = 1.2
my_eth = 5.3


# %%
# Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=CAD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=CAD"


# %%
# Fetch current BTC price
# YOUR CODE HERE!
btc_data = requests.get(btc_url)

btc_content = btc_data.content
btc_json = btc_data.json()
btc_price = btc_json["data"]["1"]["quotes"]["USD"]["price"]
# Fetch current eth price
# YOUR CODE HERE!]
eth_data = requests.get(eth_url)

eth_content = eth_data.content
eth_json = eth_data.json()
eth_price = eth_json["data"]["1027"]["quotes"]["USD"]["price"]


# %%
# Compute current value of my crpto
# YOUR CODE HERE!
cv_crypto = btc_price + eth_price
# Print current crypto wallet balance
print(f"The current value of your {my_btc} BTC is ${btc_price * my_btc}")
print(f"The current value of your {my_eth} eth is ${eth_price * my_eth}")
print(f"The current value of your crypto holdings is ${cv_crypto}!")

# %% [markdown]
# ### Collect Investments Data Using Alpaca: `SPY` (stocks) and `AGG` (bonds)

# %%
# Set Alpaca API key and secret
# YOUR CODE HERE!
alpaca_api_key = os.getenv("APCA_API_KEY")
alpaca_secret_key = os.getenv("APCA_API_SECRET_KEY")
# Create the Alpaca API object
# YOUR CODE HERE!
alpaca = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version="v2")


# %%
# Current amount of shares
# YOUR CODE HERE!
my_agg = 200
my_spy = 50


# %%
# Format current date as ISO format
# YOUR CODE HERE!
today = pd.Timestamp("2020-10-13", tz="America/New_York").isoformat()
# Set the tickers
tickers = ["AGG", "SPY"]

# Set timeframe to '1D' for Alpaca API
timeframe = "1D"

# Get current closing prices for SPY and AGG
# YOUR CODE HERE!
portfolio = alpaca.get_barset(
    tickers,
    timeframe,
    start= today,
    end = today
).df
# Preview DataFrame
# YOUR CODE HERE!
portfolio


# %%
# Pick AGG and SPY close prices
# YOUR CODE HERE!
closing_prices = pd.DataFrame()
closing_prices["AGG"] = portfolio["AGG"]["close"]
closing_prices["SPY"] = portfolio["SPY"]["close"]

closing_prices.index = closing_prices.index.date

closing_prices


# %%
agg_close = closing_prices["AGG"][0]
spy_close = closing_prices["SPY"][0]


# %%
# Print AGG and SPY close prices
print(f"Current AGG closing price: ${agg_close}")
print(f"Current SPY closing price: ${spy_close}")


# %%
# Compute the current value of shares
# YOUR CODE HERE!
cv_shares = (my_spy * spy_close) + (my_agg * agg_close)
# Print current value of share
print(f"The current value of your {my_spy} SPY shares is ${my_spy * spy_close}")
print(f"The current value of your {my_agg} AGG shares is ${my_agg * agg_close}")
print(f"The total value of your shares are ${cv_shares}!")

# %% [markdown]
# ### Savings Health Analysis

# %%
# Set monthly household income
# YOUR CODE HERE!
monthly_income = 12000
# Create savings DataFrame
# YOUR CODE HERE!
savings_df = pd.DataFrame([cv_crypto, cv_shares])
investment = ["crypto", "shares"]
savings_df["investment"] = investment
savings_df = savings_df.rename(columns= {0 : "amount"})
savings_df = savings_df.set_index("investment")

# Display savings DataFrame
display(savings_df)


# %%



# %%
# Plot savings pie chart
# YOUR CODE HERE!
plot = savings_df.plot.pie(y="amount",x=" ")


# %%
# Set ideal emergency fund
emergency_fund = monthly_income * 3

# Calculate total amount of savings
# YOUR CODE HERE!
total_savings = cv_crypto + cv_shares
# Validate saving health
# YOUR CODE HERE!
if total_savings > emergency_fund:
    print("Congrats! You have enough money in your emergency fund")
else:
    print("Uh-oh, you need to start saving!")

# %% [markdown]
# ## Part 2 - Retirement Planning
# 
# ### Monte Carlo Simulation

# %%
# Set start and end dates of five years back from today.
# Sample results may vary from the solution based on the time frame chosen
timeframe = "1D"
start_date_retirement = pd.Timestamp('2015-10-14', tz='America/New_York').isoformat()
end_date_retirment = pd.Timestamp('2020-10-14', tz='America/New_York').isoformat()


# %%
# Get 5 years' worth of historical data for SPY and AGG
# YOUR CODE HERE!
retirement = alpaca.get_barset(
    tickers,
    timeframe,
    start=start_date_retirement,
    end=end_date_retirment
).df
# Display sample data
retirement.head()


# %%



# %%
# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns
# I initially did this with 1000 simulations but it made my github push too large.
# YOUR CODE HERE!
forecast = MCSimulation(
    portfolio_data=retirement,
    weights= [cv_shares/total_savings, cv_crypto/total_savings],
    num_simulation = 100,
    num_trading_days = 252*30
)


# %%
# Printing the simulation input data
# YOUR CODE HERE!
forecast.portfolio_data.head()


# %%
# Running a Monte Carlo simulation to forecast 30 years cumulative returns
# YOUR CODE HERE!
forecast.calc_cumulative_return()


# %%
# Plot simulation outcomes
# YOUR CODE HERE!
forecast_plot = forecast.plot_simulation()


# %%
# Plot probability distribution and confidence intervals
# YOUR CODE HERE!
forecast_distribution = forecast.plot_distribution()

# %% [markdown]
# ### Retirement Analysis

# %%
# Fetch summary statistics from the Monte Carlo simulation results
# YOUR CODE HERE!
monte_carlo_summary = forecast.summarize_cumulative_return()
# Print summary statistics
# YOUR CODE HERE!
print(monte_carlo_summary)

# %% [markdown]
# ### Calculate the expected portfolio return at the 95% lower and upper confidence intervals based on a `$20,000` initial investment.

# %%
# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
# YOUR CODE HERE!
monte_lower = round(monte_carlo_summary[8]*initial_investment, 2)
monte_upper = round(monte_carlo_summary[9]*initial_investment, 2)
# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${monte_lower} and ${monte_upper}")

# %% [markdown]
# ### Calculate the expected portfolio return at the `95%` lower and upper confidence intervals based on a `50%` increase in the initial investment.

# %%
# Set initial investment
initial_investment_1 = 20000 * 1.5

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000
# YOUR CODE HERE!
monte_lower = round(monte_carlo_summary[8]*initial_investment_1, 2)
monte_upper = round(monte_carlo_summary[9]*initial_investment_1, 2)
# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment_1} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${monte_lower} and ${monte_upper}")

