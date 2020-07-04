import mysql.connector as sqlcon
import pandas as pd
import statsmodels
import datetime
import plotly.graph_objects as go
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output 

#Creating connection to database and calling data
conn = sqlcon.connect(user = 'root', password = 'aybs1196', host = '127.0.0.1', database = 'py_vis')
query = 'SELECT * FROM alcoholsales'
cursor = conn.cursor()
cursor.execute(query)
alcohol_sales = cursor.fetchall()
alcohol_sales = pd.DataFrame(alcohol_sales)
colnames = list([i[0] for i in cursor.description])
alcohol_sales.columns = colnames
# print(alcohol_sales)
cursor.close()

# Transforming data into workable form
data = alcohol_sales.copy()
data['datestamp'] = pd.to_datetime(data['datestamp'])

fig = go.Figure(data = [go.Scatter(x = data.datestamp, y = data.salesvol, mode = 'lines+markers')])
# fig.show()
# Creating app in dash to display the time graph
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div(children = [
					html.Div(children = 'Alcohol Sales Volume', style = {'fontSize':50, 'fontWeight':30,
						 	'marginLeft':650, 'textDecoration':'underline'}),

					html.Div(children = dcc.Graph(id = 'Time Series Plot', figure = fig), style = {'marginLeft':30,
							 'width':'80%', 'display':'inline-block'})

	])

if __name__ == '__main__':
	app.run_server(debug = True, port = 8050)
