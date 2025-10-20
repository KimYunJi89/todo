import streamlit as st
from utils.loader import load_data, normalize_df, add_derived_fields
from utils.metrics import compute_kpis, status_palette, status_group_mapper
from components.kpi_cards import render_kpi_row
from components.charts import status_distribution_chart, dept_status_chart, burndown_chart, completion_trend_chart
from components.tables import styled_tasks_table, download_button_for_df
import pandas as pd
import datetime as dt

st.set_page_config(page_title="지시사항 대시보드", page_icon="✅", layout="wide")

st.title("지시사항 대시보드")
with st.sidebar:
    st.header("필터")
    df_raw = load_data()
    df = normalize_df(df_raw)
    df = add_derived_fields(df)

    # Global filters
    # 기간 필터: 통보일자/이행기한
    date_basis = st.radio("기간 기준", ["통보일자", "이행기한"], horizontal=True)
    min_date = pd.to_datetime(df["통보일자"]).min() if date_basis=="통보일자" else pd.to_datetime(df["이행기한"]).min()
    max_date = pd.to_datetime(df["통보일자"]).max() if date_basis=="통보일자" else pd.to_datetime(df["이행기한"]).max()
    start, end = st.date_input("기간", value=(min_date.date() if pd.notna(min_date) else dt.date.today(),
                                           max_date.date() if pd.notna(max_date) else dt.date.today()))
    dept_opts = sorted([x for x in df["추진부서"].dropna().unique()])
    sel_depts = st.multiselect("추진부서", dept_opts, default=dept_opts)

    status_groups = ["전체","완료","진행중","미착수","보류"]
    sel_status = st.selectbox("진행현황", status_groups, index=0)

    eval_opts = ["전체","있음","없음"]
    sel_eval = st.selectbox("평가연계", eval_opts, index=0)

    keyword = st.text_input("지시내용 키워드 검색")

# Apply filters
mask = pd.Series(True, index=df.index)
if date_basis == "통보일자":
    mask &= df["통보일자"].dt.date.between(start, end)
else:
    mask &= df["이행기한"].dt.date.between(start, end)

if sel_depts:
    mask &= df["추진부서"].isin(sel_depts)

if sel_status != "전체":
    mask &= df["상태그룹"] == sel_status

if sel_eval != "전체":
    want_true = (sel_eval == "있음")
    mask &= df["평가연계_bool"] == want_true

if keyword:
    mask &= df["지시내용"].fillna("").str.contains(keyword, case=False)

dfv = df[mask].copy()

# KPI row
kpis = compute_kpis(dfv)
render_kpi_row(kpis)

# Overview section
st.subheader("개요")
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

download_button_for_df(dfv, label="현재 필터 결과 내려받기 (CSV)")
