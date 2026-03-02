import streamlit as st
import joblib
import pandas as pd
import xgboost as xgb
import plotly.express as px

# --- STEP 1: FORCE WIDE LAYOUT & THEME ---
st.set_page_config(page_title="Coverage Analytics Pro", layout="wide")


# Custom CSS to fix spacing issues
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)



# --- STEP 2: ASSET LOADING ---
@st.cache_resource
def load_all():
    return (
        joblib.load('fall_yr_pred_model.pkl'),
        joblib.load('recovery_yr_pred_model.pkl'),
        joblib.load('state_label_encoder.pkl'),
        pd.read_csv("final_dataset_statewise_combined (1).csv")
    )

m_fall, m_rec, encoder, raw_data = load_all()

# --- STEP 3: SIDEBAR (The Control Room) ---
with st.sidebar:
    st.title(" Dashboard Controls")
    st.markdown("---")
    selected_state = st.selectbox(" Select Region", encoder.classes_)
    state_numeric = encoder.transform([selected_state])[0]
    
    st.markdown("### Prediction Parameters")
    drop_val = st.slider("Target Coverage (%)", 80.0, 99.0, 90.0)
    rec_val = st.slider("Recovery Rate", 0.01, 1.0, 0.10, step=0.01)
    
    st.divider()
    st.caption("v2.4.0 | Advanced Analytics Mode")

# --- STEP 4: MAIN HEADER ---
state_df = raw_data[raw_data['Region'] == selected_state].sort_values('year')

st.title(f"State Analysis: {selected_state}")

# (The Metrics and Dividers are gone now, it goes straight to the columns below)

# --- STEP 5: TWO-COLUMN MAIN CONTENT ---
left_col, right_col = st.columns(2, gap="large")
...

with left_col:
    with st.container(border=True):
        st.subheader(" Coverage Fall Projection")
        if st.button("Generate Fall Forecast", use_container_width=True, type="primary"):
            res = m_fall.predict(pd.DataFrame([[state_numeric, drop_val]], columns=['Region_encoded', 'coverage_drop_percentage']))
            year = int(res[0])
            st.write(f"### Estimated Year: :red[{year}]")
            
            fig = px.line(state_df, x='year', y='coverage_drop_percentage', markers=True, template="plotly_white")
            fig.add_scatter(x=[year], y=[drop_val], mode='markers+text', text=[f"Predicted: {year}"], 
                            textposition="top center", marker=dict(size=15, color='red', symbol='star'))
            st.plotly_chart(fig, use_container_width=True)

with right_col:
    with st.container(border=True):
        st.subheader("🔄 Recovery Trajectory")
        
        if st.button("Generate Recovery Forecast", use_container_width=True, type="primary"):
            res_r = m_rec.predict(pd.DataFrame([[state_numeric, rec_val]], 
                                             columns=['Region_encoded', 'coverage_recovery_rate']))
            predicted_year = int(res_r[0])
            
            state_row = raw_data[raw_data['Region'].str.strip() == selected_state.strip()]
            
            if not state_row.empty:
                start_cov = state_row['coverage_percent_2025'].iloc[0]
                
                # --- FIX: Adding a background to the metrics so WHITE text is visible ---
                # This creates a dark "well" for the metrics to sit in
                st.markdown(f"""
                    <div style="background-color:#172a45; padding:15px; border-radius:10px; margin-bottom:10px; border: 1px solid #00a3ff">
                        <div style="display: flex; justify-content: space-around;">
                            <div style="text-align: center;">
                                <p style="color:#ccd6f6; margin-bottom:0px; font-size:14px;">Current (2025)</p>
                                <h2 style="color:#00a3ff; margin-top:0px;">{start_cov:.1f}%</h2>
                            </div>
                            <div style="text-align: center;">
                                <p style="color:#ccd6f6; margin-bottom:0px; font-size:14px;">Target Year</p>
                                <h2 style="color:#00a3ff; margin-top:0px;">{predicted_year}</h2>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # --- 2. CREATE A SHORTENED CHART ---
                import plotly.graph_objects as go
                fig_r = go.Figure()

                fig_r.add_trace(go.Scatter(
                    x=[2025, predicted_year], 
                    y=[start_cov, 100],
                    mode='lines+markers',
                    line=dict(width=4, color='#00a3ff'), # Bright blue line
                    marker=dict(size=10, color='#ccd6f6'),
                    hovertemplate="Year: %{x}<br>Coverage: %{y:.2f}%<extra></extra>"
                ))

                # Update layout to match a DARK professional theme
                fig_r.update_layout(
                    height=250,
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor='rgba(0,0,0,0)', # Transparent background
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, color="#ccd6f6"),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', color="#ccd6f6", range=[min(start_cov, 95)-2, 105]),
                    template="plotly_dark", # Use dark template so gridlines are light
                    showlegend=False
                )

                st.plotly_chart(fig_r, width="stretch", config={'displayModeBar': False})
            else:
                st.error("Data not found.")
            
# --- STEP 6: DATA TABLE ---
with st.expander(" View Raw Historical Records"):
    st.dataframe(state_df, use_container_width=True)