import streamlit as st
from utils.loader import load_data, normalize_df, add_derived_fields
from utils.metrics import compute_kpis
from components.kpi_cards import render_kpi_row
from components.charts import status_distribution_chart, dept_status_chart, completion_trend_chart, burndown_chart
from components.tables import styled_tasks_table
import pandas as pd
import datetime as dt

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
st.title("Overview")

df = add_derived_fields(normalize_df(load_data()))

# Simple filters just for page
min_date = df["통보일자"].min()
max_date = df["이행기한"].max()
start, end = st.date_input("기간(통보일자 기준)", value=(min_date.date() if pd.notna(min_date) else dt.date.today(),
                                            max_date.date() if pd.notna(max_date) else dt.date.today()))
mask = df["통보일자"].dt.date.between(start, end)
dfv = df[mask].copy()

kpis = compute_kpis(dfv)
render_kpi_row(kpis)

col1, col2 = st.columns([1,1])
with col1:
    st.plotly_chart(status_distribution_chart(dfv), use_container_width=True)
with col2:
    st.plotly_chart(dept_status_chart(dfv), use_container_width=True)

col3, col4 = st.columns([1,1])
with col3:
    st.plotly_chart(completion_trend_chart(dfv), use_container_width=True)
with col4:
    st.plotly_chart(burndown_chart(dfv), use_container_width=True)

st.subheader("임박·지연 리스트")
crit = dfv[(dfv["임박"]==True) | (dfv["지연"]==True)].sort_values(["지연일수","D_day"], ascending=[False, True])
styled_tasks_table(crit)
