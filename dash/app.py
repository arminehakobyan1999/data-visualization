import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]


app = dash.Dash(external_stylesheets = external_stylesheets)

data = pd.read_csv('Churn Modeling.csv')

data_1 = data.drop(['RowNumber', 'CustomerId', 'Surname'], axis = 1)
data_1['CreditScore_cat'] = ['bad'  if i >= 350 and i<=669 else 'good' if i>=670 and i<=739 else 'very good' for i in data['CreditScore']]
data_1['CreditScore_cat_num'] = [0  if i >= 350 and i<=669 else 1 if i>=670 and i<=739 else 2 for i in data['CreditScore']]
data_1['Exited_str'] = ['Exited' if i ==1 else 'Retained' for i in data['Exited']]
data_1['IsActiveMember_str'] = ['Active'if i == 1 else 'passive' for i in data['IsActiveMember']]
data_1['HasCrCard_str'] =  ['Has CrCard'if i == 1 else 'hasn\'t CrCard' for i in data['HasCrCard']]

counts_1, bins_1 = np.histogram(data_1.EstimatedSalary, bins=range(0, 102000, 2000))
counts_2, bins_2 = np.histogram(data_1.Age, bins=range(0, 100, 10))

bins_1 = 0.5 * (bins_1[:-1] + bins_1[1:])
bins_2 = 0.5 * (bins_2[:-1] + bins_2[1:])



data2 = dict(
        type = 'choropleth',
        colorscale = 'rainbow',
        locations = data_1['Geography'],
        locationmode = "country names",
        z = data_1['Exited'],
        text = data_1['Geography'],
        colorbar = {'title' : 'Customers'},
      )

l = dict(title = 'Customer Locations',
              geo = dict(projection = {'type':'mercator'})
             )



fig_4 = go.Figure(data = [data2],layout = l)

fig_1 = px.bar(x=bins_1, y=counts_1, labels={'x':'Estimated_salary', 'y':'number of observations'}, title='Working seconds')
fig_2 = px.bar(x=bins_2, y=counts_2, labels={'x':'Age', 'y':'number of observations'}, title='Annotator age')
fig_3 = px.box(data_1, y='Age', title='Age box plot')



app.layout = html.Div([
            html.Div([html.H1('Dash App')], className = 'row'),
             
            html.Div([
                   html.Div([dcc.Graph(figure = fig_1)], className = 'six columns'),
                    html.Div([dcc.Graph(figure = fig_2)], className = 'six columns')
            ], className = 'row'),
    
            html.Div([
                   html.Div([dcc.Graph(figure = fig_3)], className = 'nine columns')
            ], className = 'row'),
            html.Div([
                   html.Div([dcc.Graph(figure = fig_4)], className = 'nine columns')
            ], className = 'row'),
    
    
    
    html.Div([
        html.Div([dcc.Dropdown(
                                id = 'option_in',
                                options = [
                                        {'label': 'Existed', 'value': 'Exited'},
                                        {'label': 'Gender', 'value': 'Gender'},
                                        {'label': 'CreditScore_cat', 'value': 'CreditScore_cat'},
                                        {'label': 'IsActiveMember_str', 'value': 'IsActiveMember_str'},
                                        {'label': 'NumOfProducts', 'value': 'NumOfProducts'},
                                        {'label': 'HasCrCard_str', 'value': 'HasCrCard_str'}
                                    
        ], value = 'Gender')], className = 'four columns'),         
                 ], className = 'row'),
    
    dcc.Graph(id='our_graph')
    
], className = 'container')




@app.callback(Output(component_id='our_graph', component_property='figure'),
         [Input(component_id = 'option_in', component_property = 'value')]
)
def update_text_output(input_1):
    figure_1 = go.Figure(data=go.Bar(y=data_1[input_1].value_counts().index, x=data_1[input_1].value_counts(),orientation='h'))
    return figure_1





if __name__ == '__main__':
    app.run_server(debug = True)