# importing libraries and dependencies
import numpy as np 
import pandas as pd 
import psycopg2 
from dash import Dash, html, dcc
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os 
#from lxml.parser import column
from lxml import html as lxml_html
#os.chdir('/home/ckapsalis/Desktop/mrkt_code_projects/vanderbilt/enhanced_indeed_raw/')


# connecting to a local PostgreSQL database & initializing the db's tables 
db_connector = psycopg2.connect(
    dbname='main',
    user='ckapsalis',
    password='ckapsalis',
    host='localhost',
    port='5432'
    )
cursor = db_connector.cursor()


# fetching the data to analyze from my postgresql views into pandas dataframes
cursor.execute(f'''
     SELECT *
    FROM _jobs_full
''')
# fetching the results of a query (this puts every line into a tuple, and the tuples are stored inside a list)
rows = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]
jobs_df = pd.DataFrame(rows, columns=column_names)
print('jobs view loaded with number of rows:', jobs_df.shape[0])

cursor.execute(f'''
    SELECT *
    FROM requirements_view_full
''')
# fetching the results of a query (this puts every line into a tuple, and the tuples are stored inside a list)
rows = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]
reqs_df = pd.DataFrame(rows, columns=column_names)
print('requirements view loaded with number of rows:', reqs_df.shape[0])

cursor.execute(f'''
    SELECT *
    FROM benefits_view_full
''')
# fetching the results of a query (this puts every line into a tuple, and the tuples are stored inside a list)
rows = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]
benefs_df = pd.DataFrame(rows, columns=column_names)
print('benefits view loaded with number of rows:', benefs_df.shape[0])




# Metrics to show: 
# total companies retrieved count #
companies_count = len(jobs_df['company_x_id'].unique())
#print(companies_count)

# total jobs retrieved count #
jobs_count = len(jobs_df['job_x_id'].unique())
#print(jobs_count)

# avg hourly salary across
avg_hourly_salary = jobs_df['min_hour_salary'].mean()
#print("{:.0f}".format(avg_hourly_salary))

# vacancy count per industry_cluster_1, broken down by industry_cluster_2
jobs_df['industry_cluster_1'] = jobs_df['industry_cluster_1'].replace({"NaN": None})
res_jobs_per_ind_cluster = pd.pivot_table(
    data=jobs_df,
    index=['industry_cluster_1', 'industry_cluster_2'],
    values='job_x_id',
    aggfunc=pd.Series.nunique    
)
# sort results in descending order by nunique jobs
res_jobs_per_ind_cluster.sort_values(by='job_x_id', ascending=False, inplace=True)
res_jobs_per_ind_cluster.rename({"job_x_id": "jobs_distinct_count"}, inplace=True)
# keeping only the top 5 entries
res_jobs_per_ind_cluster = res_jobs_per_ind_cluster.head(5)




# avg min hourly salary per industry_cluster_1
res_avg_sal_per_ind_cluster = pd.pivot_table(
    data=jobs_df,
    index='industry_cluster_1',
    values='min_hour_salary',
    aggfunc=pd.Series.mean
     # (missing values in min_hourly_salary are ignored by default by pandas
    
    )
# i want to format the avg min hourly salary as a number with no decimals
res_avg_sal_per_ind_cluster['min_hour_salary'] = res_avg_sal_per_ind_cluster['min_hour_salary'].apply(lambda x: f"{x:.0f}").astype('float64')
# sort results in descending order by avg min hour salary 
res_avg_sal_per_ind_cluster.sort_values(by='min_hour_salary', ascending=False, inplace=True)
res_avg_sal_per_ind_cluster.rename({"min_hour_salary": "avg_min_hour_salary"}, inplace=True)
# keeping only the top 5 entries
res_avg_sal_per_ind_cluster = res_avg_sal_per_ind_cluster.head(5)




# vacancy count per job function
res_jobs_per_function = pd.pivot_table(
    data=jobs_df,
    index='job_function_cluster',
    values='job_x_id',
    aggfunc=pd.Series.nunique    
)
# sort results in descending order by # jobs
res_jobs_per_function.sort_values(by='job_x_id', ascending=False, inplace=True)
res_jobs_per_function.rename({"job_x_id": "jobs_distinct_count"}, inplace=True)
# keeping only the top 5 entries
res_jobs_per_function = res_jobs_per_function.head(5)




# avg min hourly salary per job function
res_avg_sal_per_function = pd.pivot_table(
    data=jobs_df,
    index='job_function_cluster',
    values='min_hour_salary',
    aggfunc=pd.Series.mean
     # (missing values in min_hourly_salary are ignored by default by pandas
    )
# i want to format the avg min hourly salary as a number with no decimals
res_avg_sal_per_function['min_hour_salary'] = res_avg_sal_per_function['min_hour_salary'].apply(lambda x: f"{x:.0f}").astype('float64')
# sort results in descending order by avg min hour salary 
res_avg_sal_per_function.sort_values(by='min_hour_salary', ascending=False, inplace=True)
res_avg_sal_per_function.rename({"min_hour_salary": "avg_min_hour_salary"}, inplace=True)
# keeping only the top 5 entries
res_avg_sal_per_function = res_avg_sal_per_function.head(5)




# most widely offered benefits 
res_jobs_per_benefit_cluster = pd.pivot_table(
    data=benefs_df,
    index='benefit_cluster',
    values='job_x_id',
    aggfunc=pd.Series.nunique
)
res_jobs_per_benefit_cluster.sort_values(by='job_x_id', ascending=False, inplace=True)
res_jobs_per_benefit_cluster.rename({'job_x_id': 'jobs_distinct_count'}, inplace=True)
res_jobs_per_benefit_cluster = res_jobs_per_benefit_cluster.head(5)




# which benefits were offered by the top industry_cluster_1 (by avg min salary) jobs 
# the top 5 industry_cluster_1 values
ind_cluster_1_focus = res_avg_sal_per_ind_cluster.index
# finding the corresponding job_x_id values to filter the benefs_df with from the jobs_df
benefs_df['industry_cluster_1'] = benefs_df['industry_cluster_1'].replace({"NaN": None})
rel_benefit_cluster_by_ind_cluster_1_focus = pd.pivot_table(
    data=benefs_df[benefs_df['benefit_cluster'].isin(res_jobs_per_benefit_cluster.index)].dropna(subset=['industry_cluster_1', 'benefit_cluster'], how='any'),
    index='benefit_cluster',
    columns='industry_cluster_1',    
    values='job_x_id',
    aggfunc=pd.Series.nunique
)
# # plotting the previous in a heatmap 
# sns.heatmap(
#     rel_benefit_cluster_by_ind_cluster_1_focus,
#     annot=True, 
#     cmap='YlGnBu', 
#     cbar=False,   # Do NOT show color bars
#     linewidths=.5  
# )
# plt.show()





# most widely set requirements
rel_jobs_per_req_cluster = pd.pivot_table(
    data=reqs_df,
    index='requirement_cluster',
    values='job_x_id',
    aggfunc=pd.Series.nunique
)
rel_jobs_per_req_cluster.sort_values(by='job_x_id', ascending=False, inplace=True)
rel_jobs_per_req_cluster.rename({"job_x_id": "distinct_jobs_count"}, inplace=True)
rel_jobs_per_req_cluster = rel_jobs_per_req_cluster.head(5)


# which requirements were set by industry_cluster_1 (by avg min salary) jobs 
reqs_df['industry_cluster_1'] = reqs_df['industry_cluster_1'].replace({"NaN": None})
rel_req_cluster_by_ind_cluster_1_focus = pd.pivot_table(
    data=reqs_df[(reqs_df['requirement_cluster'].isin(rel_jobs_per_req_cluster.index.values))].dropna(subset=['industry_cluster_1', 'requirement_cluster'], how='any'),
    index='requirement_cluster',
    columns='industry_cluster_1',
    values='job_x_id',
    aggfunc=pd.Series.nunique
)
# # plotting the previous in a heatmap 
# sns.heatmap(
#     rel_req_cluster_by_ind_cluster_1_focus,
#     annot=True, 
#     cmap='YlGnBu', 
#     cbar=False,   # Do NOT show color bars
#     linewidths=.5  
# )
# plt.show()




#############################################################


# #### Creating the Report #### 


app = Dash(__name__)

# Creating visuals to show
# KPI indicators
kpi_fig = go.Figure()
kpi_fig.update_layout(
    grid={'rows': 1, 'columns': 7, 'pattern': 'independent'},
    paper_bgcolor="lightgray"
)

# KPI #1: Total Companies
kpi_fig.add_trace(go.Indicator(
    mode="number",
    value=companies_count,
    domain={'row': 0, 'column': 1},
    title={'text': "Total Companies Retrieved #", 'font':{'color':'black', 'size':20}}
))

# KPI #2: Total Vacancies
kpi_fig.add_trace(go.Indicator(
    mode="number",
    value=jobs_count,
    domain={'row': 0, 'column': 3},
    title={'text': "Total Vacancies Retrieved #", 'font':{'color':'black', 'size':20}}
))

# KPI #3: Average Hourly Salary
kpi_fig.add_trace(go.Indicator(
    mode="number",
    value=avg_hourly_salary,
    number={'prefix': '$', 'font': {'size': 80}},
    domain={'row': 0, 'column': 5},
    title={'text': 'Avg Minimum Hourly Salary $', 'font':{'color':'black', 'size':20}}
))

# Industry distribution (pie chart)
fig_ind_jobs = px.pie(res_jobs_per_ind_cluster.reset_index(), names="industry_cluster_1", values="job_x_id")
fig_ind_jobs.update_traces(
    #texttemplate= "%{label}:<br>(%{percent})",
    textposition='inside',
    # setting the font size of data labels
    textfont=dict(size=16)
)
fig_ind_jobs.update_layout(
    paper_bgcolor="lightgray",
    # setting the title of the plot
    title={'text': 'Vacancy Distribution by Industry', 'font':{'color':'black', 'size':20}},
    title_x=0.5,
    # setting the legend text's font
    legend=dict(
        font=dict(size=18)
        )
)

# Industry average salary (bar chart)
fig_ind_sals = px.bar(
    res_avg_sal_per_ind_cluster.reset_index(),
    x="industry_cluster_1",
    y="min_hour_salary",
    text='min_hour_salary',
    range_y=[0, res_avg_sal_per_ind_cluster['min_hour_salary'].max() * 1.1]
)
fig_ind_sals.update_traces(
    textposition='outside'
)
fig_ind_sals.update_layout(
    paper_bgcolor="lightgray",
    title={'text':'Average Minimum Salary per Hour by Industry', 'font':{'color':'black', 'size':20}},
    title_x=0.5,
    # setting axis titles
    xaxis_title="Industry",
    yaxis_title="Avg Minimum Hourly Salary",
    xaxis=dict(
        title_font=dict(size=16),
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title_font=dict(size=16),
        tickfont=dict(size=16)
    )
)

# Job function distribution (pie chart)
fig_function_jobs = px.pie(res_jobs_per_function.reset_index(), names="job_function_cluster", values="job_x_id")
fig_function_jobs.update_traces(
    #texttemplate= "%{label}:<br>(%{percent})", 
    textposition='inside',
    textfont=dict(size=16)
)
fig_function_jobs.update_layout(
    paper_bgcolor="lightgray",
    title={'text': 'Vacancy Distribution by Business Function', 'font':{'color':'black', 'size':20}},
    title_x=0.5,
    legend=dict(
        font=dict(size=18)
    )
)

# Job function average salary (bar chart)
fig_function_sals = px.bar(
    res_avg_sal_per_function.reset_index(),
    x="job_function_cluster",
    y="min_hour_salary",
    text='min_hour_salary',
    range_y=[0, res_avg_sal_per_function['min_hour_salary'].max() * 1.1]
)
fig_function_sals.update_traces(
    textposition='outside'
)
fig_function_sals.update_layout(
    paper_bgcolor="lightgray",
    title={'text': 'Average Minimum Salary per Hour by Business Function', 'font':{'color':'black', 'size':20}},
    title_x=0.5,
    xaxis_title="Job Business Function",
    yaxis_title="Avg Minimum Hourly Salary",
    xaxis=dict(
        title_font=dict(size=16),
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title_font=dict(size=16),
        tickfont=dict(size=16)
    )
)


# Benefit cluster (pie chart)
fig_bencluster_jobs = px.pie(res_jobs_per_benefit_cluster.reset_index(), names="benefit_cluster", values="job_x_id")
fig_bencluster_jobs.update_traces(
    #texttemplate="%{label}:<br>(%{percent})", 
    textposition='inside',
    textfont=dict(size=16)
)
fig_bencluster_jobs.update_layout(
    paper_bgcolor="lightgray",
    title={'text': 'Vacancy Distribution by Benefit Type', 'font':{'color':'black', 'size':20}},
    title_x=0.5,
    legend=dict(
        font=dict(size=18)
    )

)

# Benefit cluster heatmap
# fig_bencluster_top_ind_clusters = go.Figure(data=go.Heatmap(
#     z=rel_benefit_cluster_by_ind_cluster_1_focus.values,
#     x=rel_benefit_cluster_by_ind_cluster_1_focus.columns,
#     y=rel_benefit_cluster_by_ind_cluster_1_focus.index,
#     colorscale='YlGnBu',
#     showscale=False,
#     text=rel_benefit_cluster_by_ind_cluster_1_focus.values,
#     texttemplate='%{text}',
#     hoverongaps=False
# ))
# fig_bencluster_top_ind_clusters.update_layout(
#     title="Benefit Distribution by Top Industry Cluster 1",
#     xaxis_title="Industry Cluster 1",
#     yaxis_title="Benefit Cluster",
#     margin=dict(l=100, r=100, t=100, b=100),
#     height=600,
#     width=800
# )

# Requirement cluster pie chart
fig_reqcluster_jobs = px.pie(rel_jobs_per_req_cluster.reset_index(), names="requirement_cluster", values="job_x_id")
fig_reqcluster_jobs.update_traces(
    #texttemplate="%{label}:<br>(%{percent})", 
    textposition='inside',
    textfont=dict(size=16)
)
fig_reqcluster_jobs.update_layout(
    paper_bgcolor="lightgray",
    title={'text': 'Vacancy Distribution by Requirement Type', 'font':{'color':'black', 'size':20}},
    title_x=0.5,
    legend=dict(
        font=dict(size=18)
    )

)


# Requirement cluster heatmap
# fig_reqcluster_top_ind_clusters = go.Figure(data=go.Heatmap(
#     z=rel_req_cluster_by_ind_cluster_1_focus.values,
#     x=rel_req_cluster_by_ind_cluster_1_focus.columns,
#     y=rel_req_cluster_by_ind_cluster_1_focus.index,
#     colorscale='YlGnBu',
#     showscale=False,
#     text=rel_req_cluster_by_ind_cluster_1_focus.values,
#     texttemplate='%{text}',
#     hoverongaps=False
# ))
# fig_reqcluster_top_ind_clusters.update_layout(
#     title="Requirement Distribution by Top Industry Cluster 1",
#     xaxis_title="Industry Cluster 1",
#     yaxis_title="Requirement Cluster",
#     margin=dict(l=100, r=100, t=100, b=100),
#     height=600,
#     width=800
# )

# creating the app layout
app.layout = html.Div([
    html.H1("Nashville Job Market Analysis Dashboard", style={'text-align': 'center'}),
    
    # KPI Graph
    html.Div(
        children=[
        html.H4("Basic KPIs", style={'text-align': 'center'}),
        dcc.Graph(figure=kpi_fig, style={'height': '300px', 'width':'100%'})
        ], 
        style={'width': '100%', 'display': 'flex', 'flex-direction':'column','align-items': 'center', 'padding-bottom': '10px'}  
    ),
    
    # First row: Industry Distribution

    html.Div([
        # H4 on the center of the page prior to the two corresponding graphs
        html.Div(
            html.H4("Industry Focus", style={'text-align': 'center'}),
            style={'width': '100%', 'display': 'flex', 'justify-content': 'center'}
        ),
        
        # row graphs
        html.Div([
            html.Div(dcc.Graph(figure=fig_ind_jobs), style={'flex': '1', 'padding': '5px'}),
            html.Div(dcc.Graph(figure=fig_ind_sals), style={'flex': '1', 'padding': '5px'})
        ], style={'display': 'flex', 'width': '100%', 'align-items': 'center', 'justify-content': 'space-between'})
    ], style={'width': '100%'}), 

    # Second row: Job Function Distribution
    html.Div([
        # row heading
        html.Div(
            html.H4("Job Function Function", style={'text-align': 'center'}),
            style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'padding': '10px'}
        ),
        
        # row graphs
        html.Div([
            html.Div(dcc.Graph(figure=fig_function_jobs), style={'flex': '1', 'padding': '5px'}),
            html.Div(dcc.Graph(figure=fig_function_sals), style={'flex': '1', 'padding': '5px'})
        ], style={'display': 'flex', 'width': '100%', 'align-items': 'center', 'justify-content': 'space-between'})
    ], style={'width': '100%'}),  # I need to dictate that the outer div occupies the whole width of the page


    # Third row: Benefits and Requirements
    html.Div([
        # row heading
        html.Div(
            html.H4("Job Benefits-Requirements Focus", style={'text-align': 'center'}),
            style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'padding': '10px'}
        ),
        
        # row graphs
        html.Div([
            html.Div(dcc.Graph(figure=fig_bencluster_jobs), style={'flex': '1', 'padding': '5px'}),
            html.Div(dcc.Graph(figure=fig_reqcluster_jobs), style={'flex': '1', 'padding': '5px'})
        ], style={'display': 'flex', 'width': '100%', 'align-items': 'center', 'justify-content': 'space-between'})
    ], style={'width': '100%'}
    )
])
    


# running the app
if __name__ == '__main__':
    app.run_server(debug=True)
