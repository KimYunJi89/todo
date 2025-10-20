import streamlit as st
import pandas as pd

def _shorten(text: str, n=120):
    if not isinstance(text, str):
        return text
    return text if len(text) <= n else text[:n-1] + "…"

def styled_tasks_table(df: pd.DataFrame):
    if df.empty:
        st.info("표시할 데이터가 없습니다.")
        return
    view = df[["관리번호","지시내용","추진부서","통보일자","이행기한","D_day","상태그룹","이행일자","평가연계"]].copy()
    view["지시내용"] = view["지시내용"].apply(lambda x: _shorten(x, 140))
    view["통보일자"] = view["통보일자"].dt.date
    view["이행기한"] = view["이행기한"].dt.date
    view["이행일자"] = view["이행일자"].dt.date
    st.dataframe(view, use_container_width=True, hide_index=True)

def download_button_for_df(df: pd.DataFrame, label="다운로드 (CSV)"):
    if df.empty:
        return
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(label, data=csv, file_name="filtered_tasks.csv", mime="text/csv")
