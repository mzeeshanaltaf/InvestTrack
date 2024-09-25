import pandas as pd
import yfinance as yf
from util import *

# Set the application title and description
page_title = "InvestTrack"
page_icon = "📊"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout='centered')
st.title(f'📊 {page_title}')
st.write(':blue[***See the power of consistent investing!💵🔄📈***]')
st.write("InvestTrack lets you simulate your investment journey! Input a stock ticker, set your start and end "
         "dates, interval, and investment amount, and find out how much your portfolio would be worth today. "
         "Visualize your regular investments against your current portfolio value and see what could have been! 💡📈")

# Display Configuration
ticker, start_date, end_date, interval, amount = display_configuration()

interval_mapper = {'Monthly': '1ME', 'Quarterly': '3ME', 'Bi-Annually': '6ME', 'Annually': '12ME'}
investment_interval = interval_mapper[interval]

# Download the stock ticker data
data = yf.download(ticker, start=start_date, end=end_date)
data = data.dropna()  # Drop null values (if any)
resampled_data = data.resample(investment_interval).first()  # Resampled the data based on investment interval
# st.write(resampled_data)

# Calculation for dollar cost average
total_investment = 0
total_shares = 0

dca_log = []

# Iterate over dataframe rows as index, series pairs
for date, row in resampled_data.iterrows():
    price = row['Adj Close']

    total_shares += amount/price
    total_investment += amount

    dca_log.append({
        'Date': date,
        'Price': price,
        'Total Shares': total_shares,
        'Total Investment': total_investment,
        'Portfolio Value': total_shares * price
    })

dca_df = pd.DataFrame(dca_log)

final_portfolio_value = total_shares * data.iloc[-1]['Adj Close']

# Display Key Statistics
display_key_statistics(total_investment, total_shares, final_portfolio_value)

# Plot the chart
plot_chart(dca_df, ticker)

# Display footer
display_footer()
