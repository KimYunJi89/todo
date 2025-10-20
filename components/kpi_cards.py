import streamlit as st

def kpi_card(label, value, help_text=None, color=None):
    st.markdown(f"""
    <div style="border-radius:12px;padding:14px 16px;background:#ffffff;border:1px solid #eee;">
      <div style="font-size:13px;color:#666;">{label}</div>
      <div style="font-size:24px;font-weight:700;{f'color:{color};' if color else ''}">{value}</div>
      {f'<div style="font-size:12px;color:#999;">{help_text}</div>' if help_text else ''}
    </div>
    """, unsafe_allow_html=True)

def render_kpi_row(kpis: dict):
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: kpi_card("총 지시 건수", f"{kpis['total']:,}")
    with c2: kpi_card("완료 (완료율)", f"{kpis['done']:,} ({kpis['done_rate']:.1f}%)", color="#2e7d32")
    with c3: kpi_card("진행중", f"{kpis['in_progress']:,}", color="#1565c0")
    with c4: kpi_card("미착수", f"{kpis['not_started']:,}")
    with c5: kpi_card("기한 임박(7일)", f"{kpis['due_soon']:,}", color="#ef6c00")
    with c6: kpi_card("기한 경과(지연)", f"{kpis['overdue']:,}", color="#c62828")
    st.markdown("")
