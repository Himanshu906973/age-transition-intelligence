import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Age Transition Intelligence System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        district_profile = pd.read_csv("district_intelligence.csv")
        time_trends = pd.read_csv("time_trends.csv")
        
        time_trends['date'] = pd.to_datetime(
            time_trends['year'].astype(str) + '-' + 
            time_trends['month'].astype(str) + '-01'
        )
        
        return district_profile, time_trends
    except FileNotFoundError:
        st.error("⚠️ Data files not found. Please ensure 'district_intelligence.csv' and 'time_trends.csv' are in the same directory.")
        return None, None


district_profile, time_trends = load_data()

if district_profile is None or time_trends is None:
    st.stop()

with st.sidebar:
    st.image("logo_adh.png", width=200)
    st.title("🎯 Age Transition Intelligence")
    st.markdown("---")
    
    st.header("🔍 Filters")

    all_states = ["All States"] + sorted(district_profile['state'].unique().tolist())
    selected_states = st.multiselect(
        "Select State(s)",
        options=all_states,
        default=["All States"]
    )
    st.subheader("Age Transition Index")
    ati_range = st.slider(
        "ATI Range",
        float(district_profile['avg_ATI'].min()),
        float(district_profile['avg_ATI'].max()),
        (float(district_profile['avg_ATI'].min()), float(district_profile['avg_ATI'].max()))
    )
    
    show_anomalies = st.checkbox("Show Only Anomalies", False)
    st.markdown("---")
    st.info("💡 **Tip**: Use filters to drill down into specific regions and patterns")

filtered_data = district_profile.copy()

if "All States" not in selected_states:
    filtered_data = filtered_data[filtered_data['state'].isin(selected_states)]

filtered_data = filtered_data[
    (filtered_data['avg_ATI'] >= ati_range[0]) & 
    (filtered_data['avg_ATI'] <= ati_range[1])
]

if show_anomalies:
    filtered_data = filtered_data[filtered_data['anomaly_flag'] == -1]

st.title("🇮🇳 Aadhaar Demographic Intelligence Platform")
st.markdown("### AI-Powered Policy Insights & Demand Forecasting")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

total_5_17 = filtered_data['total_5_17'].sum()
total_17_plus = filtered_data['total_17_plus'].sum()
avg_ati = filtered_data['avg_ATI'].mean()
anomaly_count = (filtered_data['anomaly_flag'] == -1).sum()

with col1:
    st.metric(
        label="📚 Total 5-17 Updates",
        value=f"{total_5_17:,.0f}",
        delta="Education Segment"
    )

with col2:
    st.metric(
        label="💼 Total 17+ Updates",
        value=f"{total_17_plus:,.0f}",
        delta="Workforce Segment"
    )

with col3:
    st.metric(
        label="📊 Average ATI",
        value=f"{avg_ati:.3f}",
        delta=f"{((avg_ati / district_profile['avg_ATI'].mean() - 1) * 100):.1f}% vs National"
    )

with col4:
    st.metric(
        label="⚠️ Anomaly Districts",
        value=f"{anomaly_count}",
        delta=f"{(anomaly_count / len(filtered_data) * 100):.1f}% of filtered",
        delta_color="inverse"
    )

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "🗺️ Geographic Analysis", 
    "📈 Time Series & Forecast", 
    "🔍 District Search", 
    "🎮 Scenario Planner"
])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏆 Top 15 Districts by Age Transition Index")
        top_districts = filtered_data.nlargest(15, 'avg_ATI')
        
        fig = px.bar(
            top_districts,
            y='district',
            x='avg_ATI',
            color='avg_ATI',
            orientation='h',
            color_continuous_scale='viridis',
            hover_data=['state', 'total_5_17', 'total_17_plus'],
            labels={'avg_ATI': 'Age Transition Index', 'district': 'District'}
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 ATI Distribution")
        fig = px.histogram(
            filtered_data,
            x='avg_ATI',
            nbins=30,
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            height=250,
            showlegend=False,
            xaxis_title="ATI",
            yaxis_title="Count"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔴 Anomaly Distribution")
        anomaly_dist = filtered_data['anomaly_flag'].value_counts()
        fig = px.pie(
            values=anomaly_dist.values,
            names=['Normal', 'Anomaly'],
            color_discrete_sequence=['#4ade80', '#f87171']
        )
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

    st.subheader("👥 Top 10 Districts: Education vs Workforce Demographics")
    top_demo = filtered_data.nlargest(10, 'total_17_plus')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Age 5-17 (Education)',
        x=top_demo['district'],
        y=top_demo['total_5_17'],
        marker_color='#3b82f6'
    ))
    fig.add_trace(go.Bar(
        name='Age 17+ (Workforce)',
        x=top_demo['district'],
        y=top_demo['total_17_plus'],
        marker_color='#8b5cf6'
    ))
    
    fig.update_layout(
        barmode='stack',
        height=400,
        xaxis_tickangle=-45,
        xaxis_title="District",
        yaxis_title="Total Updates"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🗺️ Geographic Distribution Analysis")
    col1, col2 = st.columns(2)
    with col1:
        state_agg = filtered_data.groupby('state').agg({
            'total_5_17': 'sum',
            'total_17_plus': 'sum',
            'avg_ATI': 'mean'
        }).reset_index().sort_values('total_17_plus', ascending=False).head(15)
        
        fig = px.bar(
            state_agg,
            x='state',
            y=['total_5_17', 'total_17_plus'],
            title="Top 15 States by Total Updates",
            labels={'value': 'Total Updates', 'variable': 'Age Group'},
            barmode='group',
            color_discrete_sequence=['#3b82f6', '#8b5cf6']
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            filtered_data,
            x='total_5_17',
            y='total_17_plus',
            size='avg_ATI',
            color='anomaly_flag',
            hover_data=['state', 'district'],
            title="District Clustering: Education vs Workforce",
            labels={
                'total_5_17': 'Education Updates (5-17)',
                'total_17_plus': 'Workforce Updates (17+)',
                'anomaly_flag': 'Type'
            },
            color_discrete_map={1: '#4ade80', -1: '#f87171'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("⚠️ AI-Detected Anomalous Districts")
    anomalies = filtered_data[filtered_data['anomaly_flag'] == -1].nlargest(20, 'avg_ATI')
    
    if len(anomalies) > 0:
        fig = px.scatter(
            anomalies,
            x='avg_ATI',
            y='total_17_plus',
            size='total_5_17',
            color='state',
            hover_data=['district'],
            title="Anomalous Districts (Unusual Age Transition Patterns)"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            anomalies[['state', 'district', 'avg_ATI', 'total_5_17', 'total_17_plus']].head(10),
            use_container_width=True
        )
    else:
        st.info("No anomalies detected in the filtered data.")
with tab3:
    st.subheader("📈 Monthly Aadhaar Demographic Update Trends")
    fig = go.Figure()   
    fig.add_trace(go.Scatter(
        x=time_trends['date'],
        y=time_trends['total_5_17'],
        mode='lines+markers',
        name='Age 5-17 (Education)',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=time_trends['date'],
        y=time_trends['total_17_plus'],
        mode='lines+markers',
        name='Age 17+ (Workforce)',
        line=dict(color='#8b5cf6', width=3)
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Total Updates",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Year-over-Year Growth")
        yearly_growth = time_trends.groupby('year').agg({
            'total_5_17': 'sum',
            'total_17_plus': 'sum'
        }).reset_index()
        
        yearly_growth['growth_5_17'] = yearly_growth['total_5_17'].pct_change() * 100
        yearly_growth['growth_17_plus'] = yearly_growth['total_17_plus'].pct_change() * 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=yearly_growth['year'],
            y=yearly_growth['growth_5_17'],
            name='5-17 Growth %',
            marker_color='#3b82f6'
        ))
        fig.add_trace(go.Bar(
            x=yearly_growth['year'],
            y=yearly_growth['growth_17_plus'],
            name='17+ Growth %',
            marker_color='#8b5cf6'
        ))
        fig.update_layout(height=300, barmode='group', yaxis_title="Growth %")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Monthly Seasonality")
        monthly_avg = time_trends.groupby('month').agg({
            'total_5_17': 'mean',
            'total_17_plus': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_avg['month'],
            y=monthly_avg['total_5_17'],
            mode='lines+markers',
            name='Avg 5-17',
            line=dict(color='#3b82f6')
        ))
        fig.add_trace(go.Scatter(
            x=monthly_avg['month'],
            y=monthly_avg['total_17_plus'],
            mode='lines+markers',
            name='Avg 17+',
            line=dict(color='#8b5cf6')
        ))
        fig.update_layout(
            height=300,
            xaxis_title="Month",
            yaxis_title="Avg Updates"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔮 Demand Forecast (Simple Projection)")
    
    last_12_months = time_trends.tail(12)
    avg_growth = (last_12_months['total_17_plus'].iloc[-1] / last_12_months['total_17_plus'].iloc[0]) ** (1/12) - 1
    
    future_months = 6
    last_date = time_trends['date'].max()
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=future_months, freq='MS')
    
    last_value = time_trends['total_17_plus'].iloc[-1]
    forecast_values = [last_value * (1 + avg_growth) ** i for i in range(1, future_months + 1)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_trends['date'],
        y=time_trends['total_17_plus'],
        mode='lines',
        name='Historical',
        line=dict(color='#8b5cf6')
    ))
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=forecast_values,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#f59e0b', dash='dash')
    ))
    fig.update_layout(height=400, xaxis_title="Date", yaxis_title="17+ Updates")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"📈 Projected monthly growth rate: {avg_growth*100:.2f}%")
with tab4:
    st.subheader("🔍 District Intelligence Search")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔎 Search for a district or state...", placeholder="Type district or state name")
    
    with col2:
        sort_by = st.selectbox("Sort by", ['avg_ATI', 'total_17_plus', 'total_5_17'])
    
    if search_term:
        search_results = filtered_data[
            (filtered_data['district'].str.contains(search_term, case=False, na=False)) |
            (filtered_data['state'].str.contains(search_term, case=False, na=False))
        ].sort_values(sort_by, ascending=False)
        
        st.write(f"Found **{len(search_results)}** matching districts")
        
        if len(search_results) > 0:
    
            st.dataframe(
                search_results[['state', 'district', 'avg_ATI', 'total_5_17', 'total_17_plus', 'anomaly_flag']],
                use_container_width=True,
                height=400
            )
          
            if len(search_results) <= 20:
                fig = px.bar(
                    search_results,
                    x='district',
                    y=['total_5_17', 'total_17_plus'],
                    title="Search Results Comparison",
                    barmode='group'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Enter a search term to find districts")
    
    st.markdown("---")
    
    st.subheader("⚖️ Compare Multiple Districts")
    
    compare_districts = st.multiselect(
        "Select districts to compare (max 5)",
        options=filtered_data['district'].unique(),
        max_selections=5
    )
    
    if compare_districts:
        comparison_data = filtered_data[filtered_data['district'].isin(compare_districts)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            for district in compare_districts:
                data = comparison_data[comparison_data['district'] == district]
                fig.add_trace(go.Bar(
                    name=district,
                    x=['5-17', '17+'],
                    y=[data['total_5_17'].values[0], data['total_17_plus'].values[0]]
                ))
            fig.update_layout(title="Updates Comparison", barmode='group', height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                comparison_data,
                x='district',
                y='avg_ATI',
                color='avg_ATI',
                title="ATI Comparison",
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("🎮 What-If Scenario Planner")
    st.markdown("**Simulate policy interventions and forecast impact**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Intervention Parameters")
        
        intervention_type = st.selectbox(
            "Intervention Type",
            ["School Enrollment Drive", "Job Training Program", "Digital Literacy Campaign", 
             "Aadhaar Update Drive", "Youth Employment Scheme"]
        )
        
        target_age_group = st.radio("Target Age Group", ["5-17 (Education)", "17+ (Workforce)", "Both"])
        
        growth_rate = st.slider("Expected Growth Rate (%)", -20, 100, 15)
        
        budget_allocation = st.number_input("Budget Allocation (₹ Crores)", 0, 10000, 500, step=100)
        
        target_states_scenario = st.multiselect(
            "Target States for Intervention",
            options=district_profile['state'].unique(),
            default=[]
        )
        
        duration_months = st.slider("Intervention Duration (Months)", 1, 24, 6)
    
    with col2:
        st.markdown("#### 📈 Projected Impact")
        
        if target_states_scenario:
            target_data = district_profile[district_profile['state'].isin(target_states_scenario)]
            
            if target_age_group == "5-17 (Education)":
                baseline = target_data['total_5_17'].sum()
                metric_name = "5-17 Updates"
            elif target_age_group == "17+ (Workforce)":
                baseline = target_data['total_17_plus'].sum()
                metric_name = "17+ Updates"
            else:
                baseline = target_data['total_5_17'].sum() + target_data['total_17_plus'].sum()
                metric_name = "Total Updates"
            
            projected = baseline * (1 + growth_rate/100)
            impact = projected - baseline
            cost_per_update = (budget_allocation * 10000000) / impact if impact > 0 else 0
            
            st.metric("Baseline Updates", f"{baseline:,.0f}")
            st.metric("Projected Updates", f"{projected:,.0f}", delta=f"+{impact:,.0f}")
            st.metric("Cost per Update", f"₹{cost_per_update:.2f}")
            st.metric("Total Districts Covered", len(target_data))
            
            avg_value_per_update = 500  
            roi = ((impact * avg_value_per_update) / (budget_allocation * 10000000)) * 100
            st.metric("ROI", f"{roi:.1f}%")
            
        else:
            st.info("👈 Select target states to see projections")
    
    if st.button("🚀 Run Simulation", type="primary"):
        if not target_states_scenario:
            st.warning("Please select at least one target state")
        else:
            st.success("✅ Simulation complete!")
        
            months = list(range(duration_months + 1))
            projection_values = [baseline * (1 + (growth_rate/100) * (m/duration_months)) for m in months]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months,
                y=projection_values,
                mode='lines+markers',
                name='Projected Growth',
                line=dict(color='#10b981', width=3),
                fill='tozeroy'
            ))
            fig.add_hline(y=baseline, line_dash="dash", line_color="red", 
                         annotation_text="Baseline")
            fig.update_layout(
                title=f"{intervention_type} - Projected Impact Over {duration_months} Months",
                xaxis_title="Months",
                yaxis_title=metric_name,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)          
            st.markdown("#### 💡 AI-Generated Recommendations")
            recommendations = {
                "School Enrollment Drive": [
                    "Focus on districts with low 5-17 update rates",
                    "Partner with local schools and education departments",
                    "Use mobile enrollment units in rural areas"
                ],
                "Job Training Program": [
                    "Target districts with high ATI but low employment rates",
                    "Collaborate with industry partners for skill development",
                    "Provide digital literacy training alongside vocational skills"
                ],
                "Digital Literacy Campaign": [
                    "Prioritize districts with older populations and low digital adoption",
                    "Set up community digital centers",
                    "Train local volunteers as digital ambassadors"
                ],
                "Aadhaar Update Drive": [
                    "Focus on anomaly districts identified by AI",
                    "Set up temporary update centers in high-demand areas",
                    "Use SMS/WhatsApp campaigns for awareness"
                ],
                "Youth Employment Scheme": [
                    "Target districts with high 17+ transition rates",
                    "Create job matching platforms",
                    "Incentivize local businesses to hire youth"
                ]
            }
            
            for i, rec in enumerate(recommendations[intervention_type], 1):
                st.markdown(f"**{i}.** {rec}")

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Data Summary")
    st.write(f"Total Districts: **{len(district_profile)}**")
    st.write(f"Total States: **{district_profile['state'].nunique()}**")

with col2:
    st.markdown("### 🤖 AI Model")
    st.write("Algorithm: **Isolation Forest**")
    st.write(f"Anomalies Detected: **{(district_profile['anomaly_flag'] == -1).sum()}**")

with col3:
    st.markdown("### 📅 Data Range")
    st.write(f"From: **{time_trends['date'].min().strftime('%b %Y')}**")
    st.write(f"To: **{time_trends['date'].max().strftime('%b %Y')}**")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b;'>"
    "🇮🇳 Built for Digital India Initiative | Powered by AI & Data Science"
    "</div>",
    unsafe_allow_html=True
)