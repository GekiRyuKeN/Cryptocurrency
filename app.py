import streamlit as st
import pandas as pd

# Prepare expanded data
data = {
    "symbol": [
        "BTCBUSD", "ETHBUSD", "BNBBUSD", "XRPBUSD", "ADABUSD",
        "DOGEBUSD", "SHIBBUSD", "DOTBUSD", "MATICBUSD", "LTCBUSD", "LINKBUSD", "UNIBUSD"
    ],
    "weightedAvgPrice": [45000, 3500, 300, 1.2, 2.5, 0.3, 0.0005, 30, 1.5, 150, 25, 20],
    "priceChangePercent": [2.5, 1.8, 0.5, -0.3, 3.1, -1.2, 0.8, 2.0, 4.5, -1.0, 1.2, 0.5]
}

df = pd.DataFrame(data)

# Set page config
st.set_page_config(page_icon="📈", page_title="Crypto Dashboard")

# Sidebar buttons
button_selection = st.sidebar.radio(
    "Select an action:",
    ("Show Metrics", "Download CSV", "Show Raw Data")
)

# Main content based on button selection
if button_selection == "Show Metrics":
    # Display metrics
    st.markdown(
        """# **Crypto Dashboard**
    A simple cryptocurrency price app using Binance API
    """
    )

    st.header("**Selected Price**")

    # Display metrics
    col1, col2, col3 = st.columns(3)

    for i, row in df.iterrows():
        col_price = row['weightedAvgPrice']
        col_percent = f"{row['priceChangePercent']}%"

        if i < 3:
            with col1:
                st.metric(row['symbol'], col_price, col_percent)
        elif 2 < i < 6:
            with col2:
                st.metric(row['symbol'], col_price, col_percent)
        else:
            with col3:
                st.metric(row['symbol'], col_price, col_percent)

elif button_selection == "Download CSV":
    # Download button for CSV
    @st.cache
    def convert_df(df):
        # Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="cryptocurrency_data.csv",
        mime="text/csv",
    )

elif button_selection == "Show Raw Data":
    # Display raw data
    st.markdown(
        """# **Raw Cryptocurrency Data**
    """
    )
    st.dataframe(df, height=2000)

# JavaScript libraries for rendering (if needed)
st.markdown(
    """
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""",
    unsafe_allow_html=True,
)
