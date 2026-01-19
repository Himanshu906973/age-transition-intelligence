# 🎯 Age-Transition Intelligence System (ATIS)
**Age-Transition Intelligence System (ATIS)** is a data-driven analytics and intelligence platform that studies **population age transitions** using **UIDAI Aadhaar enrolment and update data**.  
The system identifies **age-group shifts, temporal trends, and anomalies** to support **policy planning, social welfare decisions, and demographic forecasting**.


## 📌 Problem Statement

India’s demographic structure is constantly evolving due to:

- Birth rate changes  
- Migration patterns  
- Aging population  
- Digital inclusion initiatives (Aadhaar enrolment & updates)  

However, **traditional reporting systems fail to capture dynamic age transitions over time**.

### 👉 ATIS addresses this gap by:
- Tracking how populations transition across age groups  
- Detecting unusual or abnormal demographic patterns  
- Providing interactive, visual, and explainable insights  


## 💡 Solution Overview

ATIS transforms raw Aadhaar enrolment data into **actionable intelligence** using:

- 📊 Statistical analysis  
- 🤖 Machine learning (Anomaly Detection)  
- 📈 Time-series trend analysis  
- 🧠 Age Transition Index (ATI)  
- 🎛️ Interactive Streamlit dashboard  


## 🗂️ Dataset Used

**Source:** UIDAI – Aadhaar Enrolment & Update Dataset  
**Granularity:** State, District, Year, Month, Age Group  

### Key Columns:
- `state`
- `district`
- `year`
- `month`
- `age_group` (0–5, 5–17, 17+)
- `enrolment_count`

### Derived Datasets:
- `district_intelligence.csv`
- `time_trends.csv`


## 🧪 Methodology

### 1️⃣ Data Collection
- Loaded UIDAI Aadhaar enrolment and update datasets  
- Filtered relevant age-group fields  

### 2️⃣ Data Cleaning & Preprocessing
- Removed missing and inconsistent values  
- Normalized age group distributions  
- Aggregated monthly and yearly metrics  

### 3️⃣ Feature Engineering
- **Age Transition Index (ATI)**  
  → Measures shift intensity between age groups  
- Growth rates  
- Temporal change indicators  

### 4️⃣ Anomaly Detection
- **Isolation Forest**
- Detects abnormal enrolment spikes or drops  
- Helps identify:
  - Sudden migration  
  - Policy impact  
  - Data inconsistencies  

### 5️⃣ Time-Series Analysis
- Monthly and yearly trends  
- Transition flow visualization  


## 📊 Data Analysis & Visualisation

ATIS provides:

- 📍 District-wise Age Transition Heatmaps  
- 📈 Year-Month Trend Lines  
- 🚨 Anomaly Highlighting  
- 🎯 Age Transition Index Range Filters  
- 🗺️ State & District Comparison Views  

All visualisations are rendered **inside the notebook and Streamlit app** (no browser dependency for plots).


## 🖥️ Dashboard Features (Streamlit)

- Multi-state and district selection  
- ATI range slider  
- Toggle: **Show Only Anomalies**  
- Dynamic charts and tables  
- Clean dark UI with custom logo  


## 🛠️ Tech Stack

| Category | Tools |
|-------|------|
| Language | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn (Isolation Forest) |
| Visualization | Matplotlib, Plotly |
| Dashboard | Streamlit |
| IDE | Jupyter Notebook |
| Deployment | Streamlit Cloud |


## 🚀 How to Run the Project
streamlit run app.py

## 📌 Future Enhancements

- Predictive age transition forecasting 
- Deep learning-based anomaly detection 
- GIS map integration  
- API-based live data ingestion
- Policy impact simulation

##🌐 Live Application  
https://age-transition-intelligence.streamlit.app

## 👨‍💻 Author
Himanshu Bhoi





