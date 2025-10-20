import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.metrics import status_group_order, status_palette

def status_distribution_chart(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
    s = df["상태그룹"].value_counts().reindex(status_group_order, fill_value=0)
    fig = px.pie(values=s.values, names=s.index, hole=0.5)
    fig.update_traces(textinfo="percent+label", marker=dict(colors=[status_palette.get(k) for k in s.index]))
    fig.update_layout(title="상태 분포")
    return fig

def dept_status_chart(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
    g = (df.groupby(["추진부서","상태그룹"])["관리번호"]
           .count().reset_index(name="건수"))
    fig = px.bar(g, x="추진부서", y="건수", color="상태그룹", barmode="stack",
                 category_orders={"상태그룹": status_group_order},
                 color_discrete_map=status_palette)
    fig.update_layout(title="부서별 상태 분포", xaxis_title="", legend_title="상태")
    return fig

def completion_trend_chart(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
    d = df[df["완료여부"]==True].copy()
    if d.empty:
        return go.Figure()
    d["월"] = d["이행일자"].dt.to_period("M").dt.to_timestamp()
    s = d.groupby("월")["관리번호"].count().reset_index(name="완료건수")
    fig = px.line(s, x="월", y="완료건수")
    fig.update_layout(title="월별 완료 추이", xaxis_title="", yaxis_title="건수")
    return fig

def burndown_chart(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
    # 기준: 통보월 단위로 미완료 누적 감소
    t = df.copy()
    t["월"] = t["통보일자"].dt.to_period("M").dt.to_timestamp()
    # 미완료는 이행일자 결측으로 간주
    t["미완료"] = ~t["완료여부"]
    s = t.groupby("월")["미완료"].sum().reset_index(name="미완료건수")
    fig = px.line(s, x="월", y="미완료건수")
    fig.update_layout(title="burndown chart(미완료 누적)", xaxis_title="", yaxis_title="건수")
    return fig

def dept_monthly_completion_chart(df: pd.DataFrame):
    d = df[df["완료여부"]==True].copy()
    if d.empty:
        return go.Figure()
    d["월"] = d["이행일자"].dt.to_period("M").dt.to_timestamp()
    s = d.groupby("월")["관리번호"].count().reset_index(name="완료건수")
    fig = px.bar(s, x="월", y="완료건수")
    fig.update_layout(title="월별 완료 건수", xaxis_title="", yaxis_title="건수")
    return fig

def timeline_chart(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
    d = df.copy()
    d["시작"] = d["통보일자"]
    d["종료"] = d["이행일자"].fillna(d["이행기한"])
    # 색상: 상태그룹
    fig = px.timeline(d, x_start="시작", x_end="종료", y="추진부서", color="상태그룹",
                      hover_data=["관리번호","지시내용","통보일자","이행기한","이행일자","D_day","지연일수"],
                      color_discrete_map=status_palette,
                      category_orders={"상태그룹": status_group_order})
    fig.update_layout(title="지시사항 타임라인", xaxis_title="", yaxis_title="부서", legend_title="상태")
    fig.update_yaxes(autorange="reversed")
    return fig
