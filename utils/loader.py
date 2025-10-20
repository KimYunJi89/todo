import streamlit as st
import pandas as pd
from dateutil.parser import parse
import numpy as np

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    # 기본 경로
    path = "data/todo.xlsx"
    try:
        df = pd.read_excel(path, engine="openpyxl")
    except Exception:
        # 앱이 파일 없이도 동작하도록, 업로드 위젯 제공
        uploaded = st.file_uploader("`data/todo.xlsx`가 없습니다. 파일을 업로드하세요.", type=["xlsx"])
        if uploaded is not None:
            df = pd.read_excel(uploaded, engine="openpyxl")
        else:
            st.stop()
    return df

def _to_dt(s):
    try:
        return parse(str(s), dayfirst=False, yearfirst=True)
    except Exception:
        return pd.NaT

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # 컬럼 표준화 가정
    cols = ["관리번호","지시내용","통보일자","이행기한","추진부서","추진현황","이행일자","평가연계"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    d = df[cols].copy()

    # 날짜 파싱
    d["통보일자"] = pd.to_datetime(d["통보일자"].apply(_to_dt))
    d["이행기한"] = pd.to_datetime(d["이행기한"].apply(_to_dt))
    d["이행일자"] = pd.to_datetime(d["이행일자"].apply(_to_dt))

    # 평가연계 표준화
    d["평가연계"] = d["평가연계"].astype(str).str.strip()
    d["평가연계_bool"] = d["평가연계"].str.contains("1|Y|y|예|있음|True|true", na=False)

    # 추진현황 표준화(소문자/공백 제거 기반)
    def norm_status(x):
        s = str(x).strip().lower()
        if any(k in s for k in ["완료"]):
            return "완료"
        if any(k in s for k in ["미착수"]):
            return "미착수"
        if any(k in s for k in ["보류", "확인"]):
            return "보류"
        if s in ["nan", "", "none"]:
            return "진행중"  # 공란은 진행중으로 간주(조정 가능)
        return "진행중"
    d["상태그룹"] = d["추진현황"].apply(norm_status)

    return d

def add_derived_fields(d: pd.DataFrame) -> pd.DataFrame:
    today = pd.Timestamp.today().normalize()
    x = d.copy()
    x["완료여부"] = x["상태그룹"].eq("완료")
    x["D_day"] = (x["이행기한"] - today).dt.days

    # 임박/지연
    x["임박"] = (~x["완료여부"]) & (x["D_day"].between(0, 7, inclusive="both"))
    # 지연: 완료여부 상관 없이 기준일(완료는 이행일자, 미완료는 today)로 판단
    base_end = x["이행일자"].fillna(today)
    x["지연일수"] = (base_end - x["이행기한"]).dt.days.clip(lower=0).fillna(0).astype(int)
    x["지연"] = x["지연일수"] > 0

    return x
