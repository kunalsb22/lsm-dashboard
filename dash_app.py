import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

#file = r'https://github.com/kunalsb22/lsm-dashboard/blob/main/grid_dash.xlsx'
file = r'/app/lsm-dashboard/dash_app.py'
df = pd.read_excel(file)

                                                                    #FLYING
# Convert columns to lists
fly_list = df['FLYING'].tolist()
grid_list = df['GRID_ID'].tolist()

# Combine lists and convert to dictionary
fly_dict = dict(zip(grid_list, fly_list))

#iterate through each cell
flights = 0
no_of_col = len(fly_dict)
for v in fly_dict.keys():
    if fly_dict.get(v) == 'Y':
        flights += 1    
print('Drone flights completed = ', flights)

                                                                    # ORI
# Convert column to list
ori_list = df['ORI'].tolist()
grid_list = df['GRID_ID'].tolist()
#print(ori_list)
# Combine list and convert to dictionary
ori_dict = dict(zip(grid_list, ori_list))
#print(ori_dict)

#iterate through each cell
ori = 0
no_of_col = len(ori_dict)
for v in ori_dict.keys():
    if ori_dict.get(v) == 'Y':
        ori += 1
print('ORI generated = ', ori)
 
                                                                    # FE
# Convert column to list
fe_list = df['FE'].tolist()
grid_list = df['GRID_ID'].tolist()
#print(fe_list)
# Combine list and convert to dictionary
fe_dict = dict(zip(grid_list, fe_list))
#print(fe_dict)

#iterate through each cell
feu = 0
fer = 0
nil_fe = 0
no_of_col = len(fe_dict)
for v in fe_dict.keys():
    if fe_dict.get(v) == 'U':
        feu += 1
    elif fe_dict.get(v) == 'R':
        fer += 1
    else:
        nil_fe += 1
fe = feu + fer
print('Feature extraction completed = ', fe)
print('Feature extraction pending = ', nil_fe)
                                                                    # FINAL CHART
target = [30000, flights, ori]
actual = [flights, ori, fe]
index = ['FLYING', 'ORI', 'Feature extraction']
df = pd.DataFrame({'Completed': actual, 'Target':target}, index= index)

                                                                    # CREATE DASHBOARD USING STREAMLIT
st.set_page_config(
    page_title = 'HaLRMP Status Monitoring Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title
st.title("HaLRMP Status Monitoring Dashboard")

# creating a single-element container.
placeholder = st.empty()
with placeholder.container():
# create five columns
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
# fill in those five columns with respective metrics or KPIs 
    kpi1.metric(label="FLYING", value= flights)
    kpi2.metric(label="ORI", value= ori)
    kpi3.metric(label="FE Urban", value=  feu)
    kpi4.metric(label="FE Rural", value=  fer)
    kpi5.metric(label="Total FE", value=  fe)

# create two columns for charts 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Activity status")
        st.bar_chart(df, width=500, height=500, use_container_width=False)
    with col2: 
        f_pie = ['FE Urban', 'FE Rural', 'Balance FE']
        v_pie = [feu, fer, nil_fe]
        fig_pie = go.Figure(
            go.Pie(
            labels = f_pie,
            values = v_pie,
            hoverinfo = "label+percent",
            textinfo = "value"  
        ))  
        st.header("Feature extraction status")
        st.plotly_chart(fig_pie) 
    
    st.markdown("## Detailed Data View")
    st.dataframe(df)


