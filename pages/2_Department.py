import streamlit as st
from utils.loader import load_data, normalize_df, add_derived_fields
from utils.metrics import compute_kpis
from components.kpi_cards import render_kpi_row
from components.charts import dept_monthly_completion_chart
from components.tables import styled_tasks_table, download_button_for_df
import pandas as pd

st.set_page_config(page_title="Department", page_icon="🏢", layout="wide")
st.title("부서별 현황")

df = add_derived_fields(normalize_df(load_data()))
depts = sorted(df["추진부서"].dropna().unique().tolist())
sel = st.selectbox("부서 선택", options=depts)

dfv = df[df["추진부서"]==sel].copy()
kpis = compute_kpis(dfv)
render_kpi_row(kpis)

st.subheader("부서 작업 목록")
styled_tasks_table(dfv.sort_values(["지연","임박","D_day"], ascending=[False, False, True]))
download_button_for_df(dfv, label="이 부서 데이터 내려받기 (CSV)")

st.subheader("월별 완료 추이")
st.plotly_chart(dept_monthly_completion_chart(dfv), use_container_width=True)
