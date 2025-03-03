import streamlit as st

upload_page = st.Page("./pages/upload_data.py", title="上传数据", icon=":material/add_circle:")
analysis_page = st.Page("./pages/data_analysis.py", title="成绩分析", icon=":material/delete:")

pg = st.navigation([upload_page, analysis_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
