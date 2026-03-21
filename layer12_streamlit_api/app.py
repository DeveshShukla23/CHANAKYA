# CHANAKYA - AI Commerce Intelligence Platform
# Layer 12: Streamlit Deployment
# ARTHA - Agentic AI for Data Analysis
# Author: Devesh Shukla

import streamlit as st
import pandas as pd
import numpy as np
from groq import Groq
from dotenv import load_dotenv
import os
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

load_dotenv()

# Page config
st.set_page_config(
    page_title="CHANAKYA - AI Commerce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0D1117; color: white; }
    .stButton > button {
        background-color: #00D4AA;
        color: #0D1117;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        width: 100%;
    }
    .stTextInput > div > div > input {
        background-color: #1E1E2E;
        color: white;
        border: 1px solid #00D4AA;
    }
    [data-testid="stSidebar"] {
        background-color: #1E1E2E;
        border-right: 1px solid #00D4AA;
    }
    [data-testid="metric-container"] {
        background-color: #1E1E2E;
        border: 1px solid #00D4AA;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    PROCESSED_PATH = 'data/processed'
    df_products = pd.read_csv(f'{PROCESSED_PATH}/products_processed.csv')
    df_customers = pd.read_csv(f'{PROCESSED_PATH}/customers_processed.csv')
    df_orders = pd.read_csv(f'{PROCESSED_PATH}/orders_processed.csv')
    df_order_items = pd.read_csv(f'{PROCESSED_PATH}/order_items_processed.csv')
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], format='mixed')
    df_order_items['order_date'] = pd.to_datetime(df_order_items['order_date'], format='mixed')
    return df_products, df_customers, df_orders, df_order_items

df_products, df_customers, df_orders, df_order_items = load_data()

# ARTHA setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
delivered = df_order_items[df_order_items['order_status'] == 'Delivered']
total_revenue = delivered['revenue'].sum()
top_category = delivered.groupby('category')['revenue'].sum().idxmax()
top_product = delivered.groupby('product_name')['revenue'].sum().idxmax()

system_context = f"""
You are ARTHA, an intelligent Data Analysis AI for CHANAKYA - AI Commerce Intelligence Platform.
Inspired by Kautilya's Arthashastra, you provide wise, data-driven insights.

BUSINESS OVERVIEW:
- Total Products     : {len(df_products)} Indian products across 12 categories
- Total Customers    : {len(df_customers)} customers across Tier 1, 2, 3 cities
- Total Orders       : {len(df_orders)} orders (2023-2026)
- Total Revenue      : Rs. {total_revenue:,.2f}
- Top Category       : {top_category}
- Top Product        : {top_product}
- Delivery Rate      : 70%
- Cancellation Rate  : 12.7%
- Top Payment Method : UPI (34.9%)
- Peak Month         : November (festive season)
- Champions segment  : 129 customers generating Rs. 83.4L revenue

Always provide specific numbers, actionable recommendations, and be concise but insightful.
"""

def ask_artha(question, history):
    messages = [{"role": "system", "content": system_context}]
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content

def get_auto_visualization(question):
    question_lower = question.lower()

    if any(word in question_lower for word in ['revenue', 'trend', 'monthly', 'sales', 'growth']):
        monthly = delivered.copy()
        monthly['year_month'] = monthly['order_date'].dt.to_period('M').astype(str)
        monthly_rev = monthly.groupby('year_month')['revenue'].sum().reset_index()
        fig = px.area(monthly_rev, x='year_month', y='revenue',
                     title='Revenue Trend', color_discrete_sequence=['#00D4AA'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    elif any(word in question_lower for word in ['category', 'categories', 'product type', 'segment']):
        cat_rev = delivered.groupby('category')['revenue'].sum().reset_index()
        cat_rev = cat_rev.sort_values('revenue', ascending=True)
        fig = px.bar(cat_rev, x='revenue', y='category', orientation='h',
                    title='Revenue by Category', color_discrete_sequence=['#00D4AA'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    elif any(word in question_lower for word in ['churn', 'inactive', 'lost', 'retention', 'risk']):
        reference_date = pd.Timestamp('2026-03-18')
        last_order = df_orders.groupby('customer_id')['order_date'].max().reset_index()
        last_order['days_since'] = (reference_date - last_order['order_date']).dt.days
        last_order['status'] = last_order['days_since'].apply(
            lambda x: 'High Risk' if x >= 180 else 'Medium Risk' if x >= 90 else 'Active')
        status_counts = last_order['status'].value_counts().reset_index()
        fig = px.pie(status_counts, values='count', names='status',
                    title='Customer Churn Risk Distribution',
                    color_discrete_sequence=['#4CAF50', '#FF9800', '#F44336'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    elif any(word in question_lower for word in ['product', 'top', 'best', 'selling', 'item']):
        top_prods = delivered.groupby('product_name')['revenue'].sum().nlargest(10).reset_index()
        top_prods = top_prods.sort_values('revenue', ascending=True)
        fig = px.bar(top_prods, x='revenue', y='product_name', orientation='h',
                    title='Top 10 Products by Revenue',
                    color_discrete_sequence=['#00D4AA'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    elif any(word in question_lower for word in ['payment', 'upi', 'credit', 'debit', 'cod']):
        payment_counts = df_orders['payment_method'].value_counts().reset_index()
        fig = px.pie(payment_counts, values='count', names='payment_method',
                    title='Payment Method Distribution',
                    color_discrete_sequence=['#00D4AA','#F44336','#FF9800','#2196F3','#9C27B0','#8BC34A'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    elif any(word in question_lower for word in ['order', 'status', 'delivered', 'cancelled', 'return']):
        status_counts = df_orders['order_status'].value_counts().reset_index()
        fig = px.pie(status_counts, values='count', names='order_status',
                    title='Order Status Distribution',
                    color_discrete_sequence=['#00D4AA','#F44336','#FF9800','#2196F3','#9C27B0'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    elif any(word in question_lower for word in ['customer', 'tier', 'city', 'location']):
        tier_counts = df_customers['tier'].value_counts().reset_index()
        fig = px.pie(tier_counts, values='count', names='tier',
                    title='Customers by City Tier',
                    color_discrete_sequence=['#00D4AA','#2196F3','#FF9800'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    elif any(word in question_lower for word in ['insight', 'overview', 'summary', 'performance', 'increase']):
        cat_rev = delivered.groupby('category')['revenue'].sum().reset_index()
        cat_rev = cat_rev.sort_values('revenue', ascending=True)
        fig = px.bar(cat_rev, x='revenue', y='category', orientation='h',
                    title='Business Performance Overview',
                    color_discrete_sequence=['#00D4AA'])
        fig.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                         font_color='white', title_font_color='#00D4AA')
        return fig

    return None

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    logo_path = 'layer12_streamlit_api/chanakya_logo.png'
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    else:
        st.markdown("## 📊 CHANAKYA")

    st.markdown("### AI Commerce Intelligence")
    st.markdown("---")
    st.markdown("**Navigation**")
    page = st.radio("", ["Dashboard", "ARTHA AI", "Data Explorer"])
    st.markdown("---")

    st.markdown("""
    <div style='background-color: #0D1117; padding: 12px; border-radius: 8px;
    border: 1px solid #00D4AA; text-align: center;'>
        <p style='color: #00D4AA; font-size: 16px; font-weight: bold; margin: 0;'>⚡ ARTHA</p>
        <p style='color: #888; font-size: 11px; margin: 4px 0;'>Agentic AI for Data Analysis</p>
        <p style='color: #00D4AA; font-size: 11px; margin: 0;'>● Online & Ready</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Quick Stats**")
    st.metric("Total Revenue", "₹26.71M")
    st.metric("Total Orders", "5,010")
    st.metric("Delivery Rate", "70.02%")
    st.markdown("---")
    st.markdown("<center>Built by Devesh Shukla</center>", unsafe_allow_html=True)

# ============================================================
# DASHBOARD PAGE
# ============================================================
if page == "Dashboard":
    st.markdown("""
    <div style='background-color: #1E1E2E; padding: 20px; border-radius: 10px;
    border-bottom: 2px solid #00D4AA; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0;'>📊 CHANAKYA Executive Dashboard</h2>
        <p style='color: #888; margin: 5px 0 0 0;'>AI Commerce Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", "₹26.71M", "+25.91%")
    with col2:
        st.metric("Total Orders", "5,010", "+12%")
    with col3:
        st.metric("Avg Order Value", "₹5.33K")
    with col4:
        st.metric("Delivery Rate", "70.02%")

    st.markdown("---")

    st.markdown("""
    <div style='background: #1E1E2E; padding: 15px 20px; border-radius: 10px;
    border: 1px solid #00D4AA; margin-bottom: 20px;'>
        <span style='color: #00D4AA; font-size: 18px; font-weight: bold;'>
        ⚡ ARTHA is Active & Ready
        </span>
        <p style='color: #888; margin: 4px 0 0 0; font-size: 13px;'>
        Ask anything about your business data --- Switch to ARTHA AI from the sidebar
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        monthly = delivered.copy()
        monthly['year_month'] = monthly['order_date'].dt.to_period('M').astype(str)
        monthly_rev = monthly.groupby('year_month')['revenue'].sum().reset_index()
        fig1 = px.area(monthly_rev, x='year_month', y='revenue',
                      title='Monthly Revenue Trend',
                      color_discrete_sequence=['#00D4AA'])
        fig1.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                          font_color='white', title_font_color='#00D4AA', title_font_size=16)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        cat_rev = delivered.groupby('category')['revenue'].sum().reset_index()
        cat_rev = cat_rev.sort_values('revenue', ascending=True)
        fig2 = px.bar(cat_rev, x='revenue', y='category', orientation='h',
                     title='Revenue by Category', color_discrete_sequence=['#00D4AA'])
        fig2.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                          font_color='white', title_font_color='#00D4AA', title_font_size=16)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        status_counts = df_orders['order_status'].value_counts().reset_index()
        fig3 = px.pie(status_counts, values='count', names='order_status',
                     title='Order Status Distribution',
                     color_discrete_sequence=['#00D4AA','#F44336','#FF9800','#2196F3','#9C27B0'])
        fig3.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                          font_color='white', title_font_color='#00D4AA', title_font_size=16)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        top_prods = delivered.groupby('product_name')['revenue'].sum().nlargest(10).reset_index()
        top_prods = top_prods.sort_values('revenue', ascending=True)
        fig4 = px.bar(top_prods, x='revenue', y='product_name', orientation='h',
                     title='Top 10 Products by Revenue', color_discrete_sequence=['#00D4AA'])
        fig4.update_layout(plot_bgcolor='#1E1E2E', paper_bgcolor='#1E1E2E',
                          font_color='white', title_font_color='#00D4AA', title_font_size=16)
        st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# ARTHA AI PAGE
# ============================================================
elif page == "ARTHA AI":
    st.markdown("""
    <div style='background-color: #1E1E2E; padding: 25px; border-radius: 12px;
    border-left: 5px solid #00D4AA; margin-bottom: 25px;'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <span style='font-size: 40px;'>⚡</span>
            <div>
                <h1 style='color: #00D4AA; margin: 0; font-size: 36px;'>ARTHA</h1>
                <h4 style='color: white; margin: 5px 0;'>Agentic AI for Data Analysis</h4>
                <p style='color: #888; margin: 0; font-size: 13px;'>
                Inspired by Kautilya's Arthashastra &nbsp;|&nbsp;
                Powered by LLaMA 3.3 70B via Groq &nbsp;|&nbsp;
                <span style='color: #00D4AA;'>● Online</span>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div style='background:#0D1117; padding:12px; border-radius:8px;
        border:1px solid #00D4AA; text-align:center;'>
        <p style='color:#00D4AA; margin:0; font-size:20px;'>💬</p>
        <p style='color:white; margin:0; font-size:12px; font-weight:bold;'>Natural Language Q&A</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div style='background:#0D1117; padding:12px; border-radius:8px;
        border:1px solid #00D4AA; text-align:center;'>
        <p style='color:#00D4AA; margin:0; font-size:20px;'>🧠</p>
        <p style='color:white; margin:0; font-size:12px; font-weight:bold;'>Memory & Context</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div style='background:#0D1117; padding:12px; border-radius:8px;
        border:1px solid #00D4AA; text-align:center;'>
        <p style='color:#00D4AA; margin:0; font-size:20px;'>📊</p>
        <p style='color:white; margin:0; font-size:12px; font-weight:bold;'>Auto Visualizations</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div style='background:#0D1117; padding:12px; border-radius:8px;
        border:1px solid #00D4AA; text-align:center;'>
        <p style='color:#00D4AA; margin:0; font-size:20px;'>💡</p>
        <p style='color:white; margin:0; font-size:12px; font-weight:bold;'>Business Recommendations</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant", avatar="⚡"):
            st.write(chat["assistant"])
            if "viz" in chat and chat["viz"] is not None:
                st.plotly_chart(chat["viz"], use_container_width=True)

    st.markdown("**Quick Questions:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Top 3 Business Insights"):
            question = "What are the top 3 business insights from CHANAKYA data?"
            with st.spinner("ARTHA is thinking..."):
                answer = ask_artha(question, st.session_state.chat_history)
                viz = get_auto_visualization(question)
            st.session_state.chat_history.append({"user": question, "assistant": answer, "viz": viz})
            st.rerun()
    with col2:
        if st.button("Churn Risk Analysis"):
            question = "Which customers are at highest churn risk?"
            with st.spinner("ARTHA is thinking..."):
                answer = ask_artha(question, st.session_state.chat_history)
                viz = get_auto_visualization(question)
            st.session_state.chat_history.append({"user": question, "assistant": answer, "viz": viz})
            st.rerun()
    with col3:
        if st.button("Revenue Optimization"):
            question = "How can we increase revenue by 20%?"
            with st.spinner("ARTHA is thinking..."):
                answer = ask_artha(question, st.session_state.chat_history)
                viz = get_auto_visualization(question)
            st.session_state.chat_history.append({"user": question, "assistant": answer, "viz": viz})
            st.rerun()

    if prompt := st.chat_input("Ask ARTHA anything about CHANAKYA data..."):
        with st.spinner("ARTHA is thinking..."):
            answer = ask_artha(prompt, st.session_state.chat_history)
            viz = get_auto_visualization(prompt)
        st.session_state.chat_history.append({"user": prompt, "assistant": answer, "viz": viz})
        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================================
# DATA EXPLORER PAGE
# ============================================================
elif page == "Data Explorer":
    st.markdown("""
    <div style='background-color: #1E1E2E; padding: 20px; border-radius: 10px;
    border-bottom: 2px solid #00D4AA; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0;'>🔍 Data Explorer</h2>
        <p style='color: #888; margin: 5px 0 0 0;'>Browse all CHANAKYA datasets</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "👥 Customers", "🛒 Orders", "📋 Order Items"])
    with tab1:
        st.markdown(f"**Total Products: {len(df_products)}**")
        st.dataframe(df_products, use_container_width=True)
    with tab2:
        st.markdown(f"**Total Customers: {len(df_customers)}**")
        st.dataframe(df_customers, use_container_width=True)
    with tab3:
        st.markdown(f"**Total Orders: {len(df_orders)}**")
        st.dataframe(df_orders, use_container_width=True)
    with tab4:
        st.markdown(f"**Total Order Items: {len(df_order_items)}**")
        st.dataframe(df_order_items, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 10px;'>
    <span style='color: #00D4AA; font-weight: bold;'>CHANAKYA</span> - AI Commerce Intelligence Platform &nbsp;|&nbsp;
    Powered by <span style='color: #00D4AA; font-weight: bold;'>⚡ ARTHA</span> &nbsp;|&nbsp;
    Built by <span style='color: white;'>Devesh Shukla</span>
</div>
""", unsafe_allow_html=True)