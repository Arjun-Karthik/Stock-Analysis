import streamlit as st
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
st.set_page_config(
    page_title = "Stock Performance Analysis",
    page_icon = "📈",
    layout = "wide"
)
st.markdown("<h1 style = 'text-align : center;'>📈 Stock Performance Dashboard</h>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

file = st.file_uploader("Select Files", type=['csv'])
if file:
    csv_path = os.path.join(os.path.dirname(__file__), 'Stock Market Data.csv')
    data = pd.read_csv(csv_path)
    df = pd.read_csv(file, parse_dates=['date'])  # Use file directly
    df.sort_values(by=['Ticker', 'date'], inplace=True)

    # Compute Yearly Return
    returns = []
    for symbol, group in df.groupby('Ticker'):
        group = group.set_index('date').resample('YE').last()  # Ensure DatetimeIndex
        if len(group) >= 2:
            start_price = group['close'].iloc[-2]
            end_price = group['close'].iloc[-1]
            yearly_return = ((end_price - start_price) / start_price) * 100
        else:
            yearly_return = None

        returns.append({
            'Ticker': symbol,
            'Yearly Return (%)': yearly_return
        })

    # Final dataframe
    result_df = pd.DataFrame(returns)
    result_df.dropna(subset=['Yearly Return (%)'], inplace=True)

    def visualizer():
            tab1, tab2 = st.tabs(['📋 Data', '📈 Visualizations'])
            with tab1:
                #Top 10 Green Stocks
                st.markdown("<h3>💹	Top 10 Green Stocks (By Yearly Return)</h3>", unsafe_allow_html=True)
                top_green = result_df.sort_values(by='Yearly Return (%)', ascending=False).head(10)
                top_green.index = range(1, len(top_green) + 1)
                st.dataframe(top_green)

                #Top 10 Loss Stocks
                st.markdown("<h3>📉 Top 10 Loss Stocks (By Yearly Return)</h3>", unsafe_allow_html=True)
                top_loss = result_df.sort_values(by='Yearly Return (%)', ascending=True).head(10)
                top_loss.index = range(1, len(top_loss) + 1)
                st.dataframe(top_loss)

                #Compute green vs loss count, average price, average volume
                st.subheader("📊 Market Summary")

                green_count = (result_df['Yearly Return (%)'] > 0).sum()
                loss_count = (result_df['Yearly Return (%)'] < 0).sum()
                avg_price = data['close'].mean()
                avg_volume = data['volume'].mean()


                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🟢 Green Stocks", green_count)
                col2.metric("🔴 Loss Stocks", loss_count)
                col3.metric("💰 Average Price", f"₹{avg_price:.2f}")
                col4.metric("📦 Average Volume", f"{avg_volume:.0f}")

            with tab2:
                    #Volatile Analysis
                    vol_df = pd.read_csv("Visualization/Volatility Analysis.csv")
                    fig = px.bar(vol_df, x='Volatility', 
                        y='Ticker',
                        color='Volatility', 
                        color_continuous_scale='reds', 
                        title='📊 Top 10 Most Volatile Stocks'
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    #Cumulative Return
                    cum_df = pd.read_csv("Visualization/Cumulative Return.csv")
                    fig = px.line(
                        cum_df,
                        x="Month",
                        y="Cumulative Return",
                        color="Ticker",
                        title="📈 Cumulative Return Over Time"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    #Sector-wise Performance
                    sec_df = pd.read_csv("Visualization/Average Yearly Return by Sector-wise.csv")
                    fig = px.bar(
                        sec_df,
                        x = 'Sector',
                        y = 'Average Yearly Return by Sector',
                        color='Sector'
                    )
                    fig.update_layout(title="📊 Sector-wise Average Yearly Return")
                    st.plotly_chart(fig)

                    corr_df = pd.read_csv('Stock Market Data.csv')  # your file name
                    corr_df['date'] = pd.to_datetime(corr_df['date'])

                    # Sort by ticker and date to ensure proper calculation
                    corr_df = corr_df.sort_values(by=['Ticker', 'date'])

                    # Pivot table: rows = dates, columns = Tickers, values = close prices
                    pivot_df = corr_df.pivot(index='date', columns='Ticker', values='close')

                    # Drop any tickers with too many NaNs
                    pivot_df = pivot_df.dropna(axis=1, thresh=len(pivot_df) * 0.9)

                    # Calculate daily percentage change (return)
                    daily_return = pivot_df.pct_change().dropna()

                    correlation_matrix = daily_return.corr()

                    st.subheader("📈 Stock Price Correlation Heatmap")

                    plt.figure(figsize=(12, 10))
                    sns.heatmap(correlation_matrix, cmap='coolwarm', fmt=".2f", linewidths=0.5)
                    plt.title("Stock Price Correlation (Daily Returns)", fontsize=16)
                    st.pyplot(plt)

                    st.subheader("📊 Top 5 Gainers by Month")

                    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    folder_path = "Visualization/Top 5 Gainers of each month"

                    for i in range(0, len(months), 2):
                        col1, col2 = st.columns(2)

                        # First month in the row
                        month1 = months[i]
                        file1 = os.path.join(folder_path, f"Top Monthly Return (%) by Ticker ({month1}).csv")
                        if os.path.exists(file1):
                            df1 = pd.read_csv(file1)
                            fig1 = px.bar(df1, x="Ticker", y="Monthly Return (%)",
                                        title=f"Top 5 Gainers - {month1}",
                                        color="Monthly Return (%)",
                                        color_continuous_scale="Greens")
                            col1.plotly_chart(fig1, use_container_width=True)
                        else:
                            col1.warning(f"⚠️ No data for {month1}")

                        if i + 1 < len(months):
                            month2 = months[i + 1]
                            file2 = os.path.join(folder_path, f"Top Monthly Return (%) by Ticker ({month2}).csv")
                            if os.path.exists(file2):
                                df2 = pd.read_csv(file2)
                                fig2 = px.bar(df2, x="Ticker", y="Monthly Return (%)",
                                            title=f"Top 5 Gainers - {month2}",
                                            color="Monthly Return (%)",
                                            color_continuous_scale="Greens")
                                col2.plotly_chart(fig2, use_container_width=True)
                            else:
                                col2.warning(f"⚠️ No data for {month2}")

                    st.subheader("📊 Top 5 Losers by Month")

                    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    folder_path = "Visualization/Top 5 Losers of each month"

                    for i in range(0, len(months), 2):
                        col1, col2 = st.columns(2)

                        # First month in the row
                        month1 = months[i]
                        file1 = os.path.join(folder_path, f"Bottom Monthly Return (%) by Ticker ({month1}).csv")
                        if os.path.exists(file1):
                            df1 = pd.read_csv(file1)
                            fig1 = px.bar(df1, x="Ticker", y="Monthly Return (%)",
                                        title=f"Top 5 Losers - {month1}",
                                        color="Monthly Return (%)",
                                        color_continuous_scale="reds")
                            col1.plotly_chart(fig1, use_container_width=True)
                        else:
                            col1.warning(f"⚠️ No data for {month1}")

                        if i + 1 < len(months):
                            month2 = months[i + 1]
                            file2 = os.path.join(folder_path, f"Bottom Monthly Return (%) by Ticker ({month2}).csv")
                            if os.path.exists(file2):
                                df2 = pd.read_csv(file2)
                                fig2 = px.bar(df2, x="Ticker", y="Monthly Return (%)",
                                            title=f"Top 5 Losers - {month2}",
                                            color="Monthly Return (%)",
                                            color_continuous_scale="reds")
                                col2.plotly_chart(fig2, use_container_width=True)
                            else:
                                col2.warning(f"⚠️ No data for {month2}")

    visualizer()
