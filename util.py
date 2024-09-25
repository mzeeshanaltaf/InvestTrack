import streamlit as st
from streamlit_pills import pills
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta


# This function let the user to configure investment related options
def display_configuration():
    # Application configuration
    st.subheader('Configurations:')

    # Option to select stock ticker
    with st.container(border=True):
        st.write("**Ticker Symbols**")
        ticker = pills('Select the Ticker Symbol:', ['AAPL', 'NVDA', 'GOOG', 'MSFT',
                                                     'AMZN', 'INTC', 'META', 'AMD', 'TSLA'])

    # Configure investment period like start and end date
    with st.container(border=True):
        st.write("**Investment Period**")
        col1, col2 = st.columns(2)
        current_date = datetime.datetime.now()
        one_month_before = current_date - relativedelta(months=1)
        start_date = col1.date_input("Investment Start Date:", datetime.date(2020, 1, 1),
                                     max_value=one_month_before, help='Investment start date')
        end_date = col2.date_input("Investment End Date:", datetime.date(2024, 1, 1),
                                   max_value=current_date, help='Investment end date')
        # st.write(current_date)
    # Configure investment plan
    with st.container(border=True):
        st.write("**Investment Plan**")
        col1, col2 = st.columns(2)
        interval = col1.select_slider('Investment Interval:',
                                      options=['Monthly', 'Quarterly', 'Bi-Annually', 'Annually'],
                                      value='Quarterly', help='Enter periodic investment interval ')
        amount = col2.number_input('Investment Amount ($):', min_value=100, max_value=10000, value=500, step=10,
                                   help='Enter your periodic investment Amount in USD')

        return ticker, start_date, end_date, interval, amount


# Function to display key statistics about investment
def display_key_statistics(total_investment, total_shares, final_portfolio_value):
    # Calculate the total profit and profit percentage
    total_profit = final_portfolio_value - total_investment
    profit_percentage = (total_profit / total_investment) * 100
    profit_percentage = "{:.2f}".format(profit_percentage)

    # Show key metrics about investment
    st.subheader('Key Statistics:')
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric('Total Investment', value="{:,.0f}".format(total_investment))
    with col2:
        with st.container(border=True):
            st.metric('Total Shares', value="{:,.0f}".format(total_shares))
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric('Final Portfolio Value', value="{:,.0f}".format(final_portfolio_value))
    with col2:
        with st.container(border=True):
            st.metric('Total Profit', value="{:,.0f}".format(total_profit), delta=f"{profit_percentage}%")


# Function to plot chart
def plot_chart(dca_df, ticker):
    st.subheader('Investment Performance Over Time:')
    plt.figure(figsize=(10, 6))
    plt.plot(dca_df['Date'], dca_df['Portfolio Value'], label='Portfolio Value')
    plt.plot(dca_df['Date'], dca_df['Total Investment'], label='Invested Amount')
    plt.xlabel('Date')
    plt.ylabel('Value in $')
    plt.title(f'Dollar Cost Averaging for {ticker}')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)


def display_footer():
    footer = """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            text-align: center;
            color: grey;
            padding: 10px 0;
        }
        </style>
        <div class="footer">
            Made with ❤️ by <a href="mailto:zeeshan.altaf@92labs.ai">Zeeshan</a>. 
        </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
