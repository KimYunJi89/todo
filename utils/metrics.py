import pandas as pd

status_palette = {
    "완료": "#2e7d32",
    "진행중": "#1565c0",
    "미착수": "#6d6d6d",
    "보류": "#9e9e9e",
}
status_group_order = ["완료","진행중","미착수","보류"]

def status_group_mapper(s: str) -> str:
    return s if s in status_group_order else "진행중"

def compute_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    done = int((df["상태그룹"]=="완료").sum())
    in_progress = int((df["상태그룹"]=="진행중").sum())
    not_started = int((df["상태그룹"]=="미착수").sum())
    due_soon = int((df["임박"]==True).sum())
    overdue = int((df["지연"]==True).sum())
    done_rate = (done/total*100) if total else 0.0
    return dict(total=total, done=done, in_progress=in_progress,
                not_started=not_started, due_soon=due_soon, overdue=overdue,
                done_rate=done_rate)
