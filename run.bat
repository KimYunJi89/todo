@echo off
REM Create venv, install deps, run Streamlit (Windows)
IF NOT EXIST .venv (
  py -3 -m venv .venv
)
CALL .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
