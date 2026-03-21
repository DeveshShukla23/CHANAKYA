<div align="center">

<img src="layer12_streamlit_api/chanakya_logo.png" alt="CHANAKYA Logo" width="600"/>

# CHANAKYA — AI Commerce Intelligence Platform

### *"Data is the new Arthashastra. CHANAKYA masters both."*

<br/>

[![Live App](https://img.shields.io/badge/🚀%20LIVE%20APP-chanakya--ai.streamlit.app-00D4AA?style=for-the-badge)](https://chanakya-ai.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-DeveshShukla23-black?style=for-the-badge&logo=github)](https://github.com/DeveshShukla23)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Devesh%20Shukla-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/devesh-shukla23)

<br/>

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-Star%20Schema-orange?style=flat&logo=mysql)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?style=flat&logo=powerbi)
![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-orange?style=flat&logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?style=flat&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-green?style=flat)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-blue?style=flat&logo=scikit-learn)

</div>

---

## 🤔 What if you could build an entire Data Science ecosystem from scratch?

No Kaggle datasets. No YouTube tutorials. No shortcuts.

Just **raw Python**, **real business logic**, and **12 layers** of pure Data Science.

That's **CHANAKYA** — a 100% original end-to-end AI Commerce Intelligence Platform built on a **synthetically generated Indian e-commerce dataset** with real brands, real cities, real business patterns.

---

## 📊 The Numbers Speak

<div align="center">

| 🛒 Orders | 👥 Customers | 💰 Revenue | 📦 Products | 🏙️ Cities |
|-----------|-------------|-----------|------------|----------|
| **5,010** | **1,000** | **₹2.67 Crore** | **50 Indian Brands** | **28 Cities** |

</div>

---

## 🖥️ Streamlit Live App

![CHANAKYA Streamlit Dashboard](assets/dashboard.png)

---

## 🤖 ARTHA — Agentic AI with Auto Visualizations

> *Named after Kautilya's Arthashastra — the ancient treatise on wealth and governance*

ARTHA doesn't just answer questions. It **thinks**, **analyzes**, and **visualizes** — all in real time.

![ARTHA AI](assets/artha_ai.png)

---

## 📊 Power BI Executive Dashboard

> Dark theme | 6 KPIs | 5 Visuals | 7 DAX Measures | 3 Interactive Slicers

![Power BI Dashboard](assets/CHANAKYA_Dashboard_HQ.png)

---

## 📈 Exploratory Data Analysis — Layer 4

> 16 professional charts revealing real business insights

![Revenue Analysis](layer4_eda/01_revenue_analysis.png)

![Customer Analysis](layer4_eda/02_customer_analysis.png)

![Order Analysis](layer4_eda/03_order_analysis.png)

![Product Analysis](layer4_eda/04_product_analysis.png)

---

## 🎬 RFM Customer Segmentation — Layer 5

> 9 customer segments | Animated visualization

![RFM Animated](layer5_rfm_segmentation/rfm_bar_animated.gif)

![RFM Segments](layer5_rfm_segmentation/05_rfm_segmentation.png)

---

## 🚨 Anomaly Detection — Layer 6

> 34 fraud accounts caught using Z-Score + Isolation Forest

![Revenue Anomaly](layer6_anomaly_detection/06_revenue_anomaly.png)

![Isolation Forest](layer6_anomaly_detection/07_isolation_forest.png)

---

## 🤖 ML Demand Forecasting — Layer 7

> 4 models compared | Gradient Boosting wins with R2: 0.2891

![ML Forecasting](layer7_ml_forecasting/08_ml_forecasting.png)

---

## 🧠 Deep Learning LSTM — Layer 8

> Time series revenue forecasting with TensorFlow

![LSTM Forecasting](layer8_deep_learning/09_lstm_v2.png)

---

## 📉 Churn Prediction — Layer 9

> 477 at-risk customers identified | Data leakage detected & fixed

![Churn Prediction](layer9_churn_prediction/10_churn_prediction.png)

---

## 💡 Key Business Insights
```
📈  Electronics drives 75% revenue — but has the LOWEST profit margin
🏆  129 Champion customers generate ₹83.4L — top 13% = 31% revenue
⚠️  34 fraud accounts detected using Z-Score + Isolation Forest
📉  477 customers predicted to churn — before they actually left
🎯  November is peak month — festive season spike clearly visible
💳  UPI dominates at 34.9% — Digital India is real
```

---

## 🏗️ 12 Layers of Pure Data Science
```
┌─────────────────────────────────────────────────────────────┐
│                     CHANAKYA ECOSYSTEM                       │
├──────┬──────────────────────────┬───────────────────────────┤
│ L1   │ Data Source + Simulation │ 5,010 live orders         │
│ L2   │ ETL Pipeline             │ Production-grade logging  │
│ L3   │ SQL Data Warehouse       │ Star Schema + 7 queries   │
│ L4   │ EDA                      │ 16 professional charts    │
│ L5   │ RFM Segmentation         │ 9 segments + animation 🎬 │
│ L6   │ Anomaly Detection        │ 34 frauds caught          │
│ L7   │ ML Demand Forecasting    │ Gradient Boosting wins    │
│ L8   │ Deep Learning LSTM       │ Time series forecasting   │
│ L9   │ Churn Prediction         │ 477 at-risk customers     │
│ L10  │ Power BI Dashboard       │ Dark theme + DAX measures │
│ L11  │ ARTHA Agentic AI         │ LLaMA 3.3 70B via Groq    │
│ L12  │ Streamlit Deployment     │ Live on the internet      │
└──────┴──────────────────────────┴───────────────────────────┘
```

---

## 🔬 Technical Depth

### SQL — 8 Concepts Used
```sql
WITH customer_ltv AS (
    SELECT customer_id, SUM(revenue) as lifetime_value,
    RANK() OVER (ORDER BY SUM(revenue) DESC) as ltv_rank
    FROM fact_order_items GROUP BY customer_id
)
SELECT * FROM customer_ltv ORDER BY lifetime_value DESC;
```

### ML — 4 Models Compared
```
Linear Regression    → R2: 0.2652
Decision Tree        → R2: 0.0780
Random Forest        → R2: 0.2522
Gradient Boosting    → R2: 0.2891 ✅ WINNER
```

### Data Leakage — Detected & Fixed
```
v1 with days_since_last  → 100% accuracy ❌ (LEAKAGE!)
v2 without leakage       → 67% accuracy  ✅ (HONEST)
```

---

## 🚀 Tech Stack
```
Language      : Python 3.11
Database      : MySQL (Star Schema)
ML Libraries  : Scikit-learn, TensorFlow, Keras
Data          : Pandas, NumPy, Faker (Indian locale)
Visualization : Matplotlib, Seaborn, Plotly, Power BI
AI Model      : LLaMA 3.3 70B via Groq API
Frontend      : Streamlit
Deployment    : Streamlit Cloud
Security      : python-dotenv
Version Ctrl  : Git + GitHub
```

---

## ⚡ Run Locally
```bash
git clone https://github.com/DeveshShukla23/CHANAKYA.git
cd CHANAKYA
pip install -r layer12_streamlit_api/requirements.txt
echo "GROQ_API_KEY=your_groq_key_here" > layer12_streamlit_api/.env
cd layer12_streamlit_api
streamlit run app.py
```

---

## 👨‍💻 Author

<div align="center">

**Devesh Shukla**
*Data Analyst | Data Scientist | Builder*

*6 months internship experience | Passionate about turning data into decisions*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/devesh-shukla23)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/DeveshShukla23)
[![Live App](https://img.shields.io/badge/🚀%20Try%20CHANAKYA-Live-00D4AA?style=for-the-badge)](https://chanakya-ai.streamlit.app)

</div>

---

<div align="center">

*"Most people download a dataset. I built one."*

**CHANAKYA** — Built with passion, data, and Arthashastra wisdom 🏛️

⭐ Star this repo if you found it useful!

</div>
