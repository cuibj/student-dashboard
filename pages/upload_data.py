import streamlit as st
import pandas as pd
import openpyxl
from sqlalchemy import create_engine
import sqlite3

st.title('成绩分析')

uploaded_file = st.file_uploader("Choose a file", type = 'xlsx')

if uploaded_file is not None:
    wb = openpyxl.load_workbook(uploaded_file)
    sheetnames = wb.sheetnames
    sheet_selector = st.selectbox("Select sheet:",sheetnames)
    df = pd.read_excel(uploaded_file,sheet_selector)
    st.markdown(f"### Currently Selected: `{sheet_selector}`")
    st.write(df)
    exam_name = st.text_input("考试名称")
    df["考试"] = exam_name
    bt = st.button("上传数据")
    if bt:
        db_path = '/Users/amber/workspace/stu_dashboard/data/student.db'  # 替换为你的路径
        engine = create_engine(f'sqlite:///{db_path}', echo=False)
        df.to_sql('scores', con=engine, if_exists='append', index=False)
        st.success("Done!")



    
    



