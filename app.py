import streamlit as st
import pandas as pd
import urllib.error
import time

# Function to fetch data from Binance API with retries
@st.cache  # Cache the data to improve performance
def fetch_data(url):
    MAX_RETRIES = 3
    retries = 0

    while retries < MAX_RETRIES:
        try:
            df = pd.read_json(url)
            return df
        except urllib.error.HTTPError as e:
            st.warning(f"Retry {retries + 1} failed: HTTP Error {e.code} - {e.reason}")
            retries += 1
            time.sleep(1)  # Wait for 1 second before retrying
    else:
        st.error("Failed to fetch data after multiple retries. Please try again later.")
        return None

# Set page config
st.set_page_config(page_icon="📈", page_title="Crypto Dashboard")

# Sidebar image
st.sidebar.image(
    "https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/z3ahdkytzwi1jxlpazje",
    width=50,
)

# Main content
st.markdown(
    """# **Crypto Dashboard**
A simple cryptocurrency price app pulling price data from the [Binance API](https://www.binance.com/en/support/faq/360002502072)
"""
)

st.header("**Selected Price**")

# Fetch market data from Binance API
df = fetch_data("https://api.binance.com/api/v3/ticker/24hr")

if df is not None:
    # Dictionary of cryptocurrencies to display
    crpytoList = {
        "Price 1": "BTCBUSD",
        "Price 2": "ETHBUSD",
        "Price 3": "BNBBUSD",
        "Price 4": "XRPBUSD",
        "Price 5": "ADABUSD",
        "Price 6": "DOGEBUSD",
        "Price 7": "SHIBBUSD",
        "Price 8": "DOTBUSD",
        "Price 9": "MATICBUSD",
    }

    # Display metrics
    col1, col2, col3 = st.columns(3)

    for i, (label, symbol) in enumerate(crpytoList.items()):
        selected_crypto_index = df.index[df['symbol'] == symbol].tolist()[0]
        col_df = df.iloc[selected_crypto_index]
        col_price = float(col_df['weightedAvgPrice'])
        col_percent = f"{float(col_df['priceChangePercent'])}%"
        
        if i < 3:
            with col1:
                st.metric(label, col_price, col_percent)
        elif 2 < i < 6:
            with col2:
                st.metric(label, col_price, col_percent)
        else:
            with col3:
                st.metric(label, col_price, col_percent)

    st.header("")

    # Download button for CSV
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="binance_data.csv",
        mime="text/csv",
    )

    # Display dataframe
    st.dataframe(df, height=2000)

# JavaScript libraries for rendering
st.markdown(
    """
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""",
    unsafe_allow_html=True,
)
