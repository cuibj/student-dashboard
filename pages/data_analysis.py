import streamlit as st
import pandas as pd
import openpyxl
from sqlalchemy import create_engine
import sqlite3
import datetime
import plotly.express as px

# 获取数据
@st.cache_data
def get_data(date):
    print(date)
    db_path = '/Users/amber/workspace/student-dashboard/data/student.db'
    conn = sqlite3.connect(db_path)

    data = pd.read_sql_query("SELECT * FROM scores", conn)
    return data


st.write("# 成绩分析")

# if st.button("获取数据"):
# today = datetime.date.today()
now = datetime.datetime.now()
data = get_data(now)
st.write("## 班级分学科平均成绩")
exam_lst = data["考试名称"].unique() 
exam = st.selectbox("考试", exam_lst)

cols1 = ['语文','数学','英语','物理','化学','生物','地理','政治','历史','总分']

data0 = data.melt(id_vars=['班级','姓名', '考试名称',"考试日期"], value_vars = cols1,  var_name="学科", value_name="成绩")
# st.dataframe(data0)
data1 = data0.loc[data0["考试名称"]==exam, :].groupby(by = ["班级","学科"])["成绩"].mean().reset_index()
# st.dataframe(data1)
st.bar_chart(data1.loc[data1['学科']=="总分"], x="学科", y="成绩", color="班级", stack=False)
st.bar_chart(data1.loc[data1['学科']!="总分"], x="学科", y="成绩", color="班级", stack=False)

st.write("## 班级各科成绩分布")
class_lst = data["班级"].unique()
class_lst.sort()
cl=st.selectbox("班级", class_lst, index=1)
data2 = data0.loc[(data0["考试名称"]==exam)&(data0["班级"]==cl),:]

f1,f2=st.columns((4, 10))
fig0 = px.box(
    data2.loc[data2["学科"]=="总分", :],
    x="学科",          # 横坐标为学科
    y="成绩",          # 纵坐标为成绩
    title="各学科成绩分布箱线图",
    color="学科",       # 按学科颜色区分（可选）
    # points="all"       # 显示所有原始数据点
)
# 优化布局
fig0.update_layout(
    xaxis_title="学科",
    yaxis_title="成绩",
    hovermode="x unified",
    showlegend=False,   # 隐藏图例（颜色已通过学科区分）
    # hoverinfo="skip"  
)
f1.plotly_chart(fig0, use_container_width=True)

# 绘制箱线图
fig1 = px.box(
    data2.loc[data2["学科"]!="总分", :],
    x="学科",          # 横坐标为学科
    y="成绩",          # 纵坐标为成绩
    title="各学科成绩分布箱线图",
    color="学科",       # 按学科颜色区分（可选）
    # points="all"       # 显示所有原始数据点
)
# 优化布局
fig1.update_layout(
    xaxis_title="学科",
    yaxis_title="成绩",
    hovermode="x unified",
    showlegend=False,   # 隐藏图例（颜色已通过学科区分）
    # hoverinfo="skip"  
)

f2.plotly_chart(fig1, use_container_width=True)


st.write("## 学生历史成绩分析")

stu_lst = data.loc[data["班级"]==cl,"姓名"].unique()
stu_lst.sort()

stu = st.selectbox("学生", stu_lst)

data0["排名"] = data0.groupby(by=["考试名称","考试日期","学科"])["成绩"].rank(method='min', ascending=False)

stu_class = st.selectbox("学科", cols1)
stu_data = data0.loc[(data0["学科"]==stu_class)&(data0["姓名"]==stu), : ]
st.line_chart(stu_data, x="考试日期",y="排名")













    
    



