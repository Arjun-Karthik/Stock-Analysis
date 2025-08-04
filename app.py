import streamlit as st
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center;'>📈 Stock Performance Dashboard</h1>
    <hr style='border-top: 3px solid #bbb;'>
""", unsafe_allow_html=True)

# Upload CSV File
file = st.file_uploader("📂 Upload your Stock Market CSV file", type=['csv'])

if file:
    data = pd.read_csv(file, parse_dates=['date'])
    data.sort_values(by=['Ticker', 'date'], inplace=True)

    # Yearly Return Calculation
    returns = []
    for symbol, group in data.groupby('Ticker'):
        group = group.set_index('date').resample('YE').last()
        if len(group) >= 2:
            start_price = group['close'].iloc[-2]
            end_price = group['close'].iloc[-1]
            yearly_return = ((end_price - start_price) / start_price) * 100
        else:
            yearly_return = None
        returns.append({'Ticker': symbol, 'Yearly Return (%)': yearly_return})

    result_df = pd.DataFrame(returns)
    result_df.dropna(subset=['Yearly Return (%)'], inplace=True)

    # Summary Metrics
    green_count = (result_df['Yearly Return (%)'] > 0).sum()
    loss_count = (result_df['Yearly Return (%)'] < 0).sum()
    avg_price = data['close'].mean()
    avg_volume = data['volume'].mean()

    # Tabs
    tab1, tab2 = st.tabs(['📋 Overview', '📈 Visualizations'])

    with tab1:
        st.markdown("<h3>💹 Top 10 Green Stocks</h3>", unsafe_allow_html=True)
        top_green = result_df.sort_values(by='Yearly Return (%)', ascending=False).head(10)
        top_green.index = range(1, len(top_green) + 1)
        st.dataframe(top_green.style.background_gradient(cmap='Greens'))

        st.markdown("<h3>📉 Top 10 Loss Stocks</h3>", unsafe_allow_html=True)
        top_loss = result_df.sort_values(by='Yearly Return (%)', ascending=True).head(10)
        top_loss.index = range(1, len(top_loss) + 1)
        st.dataframe(top_loss.style.background_gradient(cmap='Reds_r'))

        st.markdown("---")
        st.markdown("<h3>📊 Market Summary</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🟢 Green Stocks", green_count)
        col2.metric("🔴 Loss Stocks", loss_count)
        col3.metric("💰 Avg. Price", f"₹{avg_price:.2f}")
        col4.metric("📦 Avg. Volume", f"{avg_volume:,.0f}")

    with tab2:
        # Volatility Analysis
        vol_df = pd.read_csv("Power Bi CSV Data/Volatility by Ticker.csv")
        fig_vol = px.bar(vol_df, 
                        x='Volatility', 
                        y='Ticker', 
                        color='Volatility', 
                        title = '📊 Top 10 Most Volatile Stocks',
                        color_continuous_scale='reds',
                    )
        
        fig_vol.update_layout(
            yaxis={'categoryorder': 'total ascending'} 
        )
        st.plotly_chart(fig_vol, use_container_width=True)

        # Cumulative Return
        cum_df = pd.read_csv("Power Bi CSV Data/Cumulative Return.csv")
        fig_cum = px.line(cum_df, x='Month', y='Cumulative Return', color='Ticker',
                          title="📈 Cumulative Return Over Time",
                          color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_cum, use_container_width=True)

        # Sector-wise Performance
        sec_df = pd.read_csv("Power Bi CSV Data/Average Yearly Return by Sector-wise.csv")
        fig_sec = px.bar(sec_df, 
                        x='Sector', 
                        y='Average Yearly Return by Sector', 
                        color='Sector',
                        title="📊 Sector-wise Performance"
                    )
        st.plotly_chart(fig_sec, use_container_width=True)

        # Monthly Gainers & Losers
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        st.subheader("📊 Top 5 Gainers (Month-wise)")
        for i in range(0, len(months), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(months):
                    month = months[i + j]
                    path = f"Power Bi CSV Data/Top 5 Gainers of each month/Top Monthly Return (%) by Ticker ({month}).csv"
                    if os.path.exists(path):
                        df = pd.read_csv(path)
                        fig = px.bar(df, x="Ticker", y="Monthly Return (%)", title=month, color="Monthly Return (%)", color_continuous_scale="Greens")
                        cols[j].plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Top 5 Losers (Month-wise)")
        for i in range(0, len(months), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(months):
                    month = months[i + j]
                    path = f"Power Bi CSV Data/Top 5 Losers of each month/Bottom Monthly Return (%) by Ticker ({month}).csv"
                    if os.path.exists(path):
                        df = pd.read_csv(path)
                        fig = px.bar(df, x="Ticker", y="Monthly Return (%)", title=month, color="Monthly Return (%)", color_continuous_scale="reds")
                        fig.update_layout(coloraxis_reversescale=True)
                        cols[j].plotly_chart(fig, use_container_width=True)

        # Correlation
        st.subheader("📈 Stock Price Correlation Heatmap")
        corr_df = data.copy()
        pivot_df = corr_df.pivot(index='date', columns='Ticker', values='close')
        pivot_df = pivot_df.dropna(axis=1, thresh=len(pivot_df) * 0.9)
        daily_return = pivot_df.pct_change().dropna()
        corr_matrix = daily_return.corr()

        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_matrix, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
        st.pyplot(fig)

