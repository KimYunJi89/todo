import streamlit as st
from utils.loader import load_data, normalize_df, add_derived_fields
from components.charts import timeline_chart
import pandas as pd

st.set_page_config(page_title="Timeline", page_icon="🗓️", layout="wide")
st.title("타임라인 / Gantt")

df = add_derived_fields(normalize_df(load_data()))

st.caption("시작=통보일자, 예정종료=이행기한, 실제종료=이행일자")

st.plotly_chart(timeline_chart(df), use_container_width=True)
