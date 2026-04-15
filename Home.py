import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Stock Analysis Pro",
    page_icon="💹",
    layout="wide",
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background-color: #0e1117;
    }
    /* Custom Skill Cards */
    .skill-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
        margin-bottom: 10px;
    }
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d4ff, #0055ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)




# Header Section
col_t1, col_t2 = st.columns([2, 1])
with col_t1:
    st.header("Data-Driven Stock Analysis")
    st.subheader("Organizing, Cleaning, and Visualizing Market Trends")
    st.markdown("""
    > **Empowering investors with clean, actionable data.**  
    > This project demonstrates a full-stack data science approach to the financial markets—from raw data ingestion to high-level visual intelligence.
    """)

with col_t2:
    # Lottie or high-quality image
    st.image("stockprice.avif")

st.divider()

# Metrics Section (Market Pulse)
m1, m2, m3 = st.columns(3)
m1.metric("Database", "My SQL ", "Connected")
m2.metric("Processing", "Pandas", "Optimized")
m3.metric("Viz", "Power BI", "Live")


st.write("## ") # Spacing

# Content Section
col_a, col_b = st.columns([1, 1], gap="large")

with col_a:
    st.markdown("### 🎯 Project Overview")
    st.write("""
    Financial data is notoriously messy. This project tackles the complexity of market trends 
    by building a structured pipeline. We don't just show graphs; we ensure the data 
    underneath them is statistically sound and computationally efficient.
    
    **What this project solves:**
    - Eliminates data gaps in historical stock pricing.
    - Centralizes disparate market files into a structured SQL environment.
    - Provides interactive "What-If" scenarios using Streamlit and Power BI.
    """)

with col_b:
    st.markdown("### 🛠️ Skills & Takeaways")
    # Displaying skills as attractive colored tags/buttons
    skills = [
        ("🐍 Python", "Core Logic"), 
        ("🐼 Pandas", "Data Cleaning"), 
        ("📉 Statistics", "Trend Analysis"), 
        ("💾 SQL", "Data Organizing"), 
        ("📊 Power BI", "Visualizing"), 
        ("🚀 Streamlit", "Deployment")
    ]
    
    idx = 0
    for row in range(3):
        cols = st.columns(2)
        for col in cols:
            if idx < len(skills):
                with col:
                    st.markdown(f"""
                    <div class="skill-card">
                        <span style="color:#00d4ff; font-weight:bold;">{skills[idx][0]}</span><br>
                        <span style="font-size:0.8rem; color:#cbd5e0;">{skills[idx][1]}</span>
                    </div>
                    """, unsafe_allow_html=True)
                idx += 1

st.write("## ")
st.divider()
st.markdown("<center>Developed for the Finance Domain | Built with Python & Streamlit</center>", unsafe_allow_html=True)
