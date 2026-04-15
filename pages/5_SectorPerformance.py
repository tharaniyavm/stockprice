import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from database import df_to_mysql

def get_sector_analysis(price_df, sector_df):
    # 1. Calculate yearly return for each ticker
    price_df['date'] = pd.to_datetime(price_df['date'])
    price_df = price_df.sort_values(['Ticker', 'date'])
    
    summary = price_df.groupby('Ticker').agg(
        start_price=('close', 'first'),
        end_price=('close', 'last')
    )
    summary['return_pct'] = ((summary['end_price'] - summary['start_price']) / summary['start_price']) * 100
    
    # 2. Merge performance with sector information
    merged_df = summary.reset_index().merge(sector_df, on='Ticker')
    
    # 3. Calculate average yearly return per sector
    sector_summary = merged_df.groupby('sector')['return_pct'].mean().reset_index()
    sector_summary.columns = ['sector', 'Avg_Yearly_Return']
    
    return sector_summary

# Load datasets
try:
    stockpricedf = pd.read_csv("FullData.csv")
    sectordf = pd.read_csv("SectorData.csv")
    sectordf['Ticker'] = sectordf['Symbol'].str.split(':').str[1].str.strip()

    # Process data
    sector_performance = get_sector_analysis(stockpricedf, sectordf)
    sector_performance = sector_performance.sort_values(by='Avg_Yearly_Return', ascending=False)

    # --- STREAMLIT DISPLAY ---
    st.header("🏢 Sector-wise Performance")

    # Visualization: Matplotlib Bar Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Apply dark theme styling
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    # Create color map (RdYlGn replacement)
    norm = plt.Normalize(sector_performance['Avg_Yearly_Return'].min(), sector_performance['Avg_Yearly_Return'].max())
    colors = cm.RdYlGn(norm(sector_performance['Avg_Yearly_Return']))

    # Plot
    bars = ax.bar(sector_performance['sector'], sector_performance['Avg_Yearly_Return'], color=colors)

    # Formatting
    ax.set_title("Average Yearly Return by Industry Sector", color='white', pad=20)
    ax.set_ylabel("Average Return (%)", color='white')
    plt.xticks(rotation=45, ha='right')
    
    # Add a horizontal line at 0 for reference
    ax.axhline(0, color='white', linewidth=0.8, linestyle='--')

    st.pyplot(fig)

    # Data Table
    st.write("### Sector Summary Data")
    st.dataframe(
        sector_performance.style.format({"Avg_Yearly_Return": "{:.2f}%"}),
        use_container_width=True
    )

    # Adding to database
    table_name = "sectorperformance"
    df_to_mysql(sector_performance, table_name)

except FileNotFoundError as e:
    st.error(f"File missing: {e.filename}")
