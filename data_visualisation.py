import mysql.connector as sqlcon  # Calling required libraries and functions
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Establishing Connection and calling data from MySQL database
conn = sqlcon.connect(user = 'root', password = 'aybs1196', host = '127.0.0.1', database = 'py_vis')
query = 'SELECT * FROM plcmnt_stats'
cursor = conn.cursor()
cursor.execute(query)
plcmnt_records = cursor.fetchall()
plcmnt_records = pd.DataFrame(plcmnt_records)
colnames = list([i[0] for i in cursor.description])
plcmnt_records.columns = colnames
# print(plcmnt_records)
cursor.close()


# Replacing char values in columns with binaries for efficient working
data = plcmnt_records.copy()
data['sex'] = data['sex'].replace(['F','M'], [0,1])
data['ssc_b'] = data['ssc_b'].replace(['Others', 'Central'], [0,1])
data['hsc_b'] = data['hsc_b'].replace(['Others', 'Central'], [0,1])
data['hsc_s'] = data['hsc_s'].replace(['Commerce', 'Science', 'Arts'], [0,1,2])
data['degree_t'] = data['degree_t'].replace(['Sci&Tech', 'Comm&Mgmt', 'Others'], [0,1,2])
data['workex'] = data['workex'].replace(['No', 'Yes'], [0,1])
data['specialisation'] = data['specialisation'].replace(['Mkt&HR','Mkt&Fin'], [0,1])
data['status'] = data['status'].replace(['Placed', 'Not Placed'], [0,1])


# To create a summary table for above data containing information about columns
colnames = pd.Series(data.columns)				# Step1: Create pandas dataframe for summary
coltype = pd.Series(['categorical', 'numeric', 'categorical', 'numeric', 'categorical', 'categorical',
 			'numeric','categorical', 'categorical', 'numeric', 'categorical', 'numeric',
 			'categorical', 'numeric'])
miss_rows = list([])
factor = 100/len(data.index)
for i in range(len(data.columns)):
	x = round(sum(data.iloc[:,i].isna())*factor,2)
	miss_rows.append(x)
miss_rows = pd.Series(miss_rows)
description = pd.Series(['gender of candidate', 'marks(in%) in 10th std', '10th std board',
				'marks(in%) in 12th std','12th std board','12th std stream','marks(in%) in UG','UG stream',
				'have worked or not','employibility test score','mba specialisation','mba percentage',
				'placement status','salary package'])
data_summ = pd.concat([colnames, coltype, miss_rows, description], axis = 1)
data_summ.columns = ['name', 'type', 'perc_of_NAs', 'description']

fig1 = go.Figure(data = [go.Table(				#Step2: Create stylized table with plotly
							columnorder = [1,3,2,4],			# Change order of columns in plot
							columnwidth = [800, 800, 400, 800], # Note the column width is mapped to column given in cell values in same order
							header = dict(values = list(data_summ.columns),
											line_color = 'black',
											fill_color = 'grey', # Note for every column a diff color can be given by passing an array of colurs[c1,...,cN]
											font = dict(color = 'white', size = 18), # Note like fill_color diff values for all columns can be given for
											align = 'center', # font arguements and align by passing an array [arg1,...argN]
											height = 30),
							cells = dict(values = [data_summ.name, data_summ.type, data_summ.perc_of_NAs,
														 data_summ.description],
											line_color = 'black',
											fill_color = 'white', # Note like header diff values for all columns can be given for cells also
											font = dict(color = 'black', size = 15), # refer to comments above
											align = 'center',
											height = 25)
								)
						])
fig1.update_layout(width = 1000, height = 1500) # changes web page dimension
# fig1.show()


#Fig 2: Stacked Bar chart showing missing data information and column type with hover text
fig2 = go.Figure(data = [
			go.Bar(name = 'Available ', x = data_summ.name, y = 100 - data_summ.perc_of_NAs, hovertext = data_summ.type, marker_color = 'orange'),
			go.Bar(name = 'Missing ', x = data_summ.name, y = data_summ.perc_of_NAs, hovertext = data_summ.type, marker_color = 'blue')
		])
fig2.update_traces(marker_line_color = 'black', marker_line_width = 2, opacity = 0.6)
fig2.update_layout(title = 'Missing Data Information',xaxis_title = 'column', barmode = 'stack',
				   yaxis_title = 'Missing Data Information', font = dict(size = 18))
# fig2.show()


# Fig3: Pie chart showing how many columns are categorical and how many are numeric
fig3 = go.Figure(data = [
			go.Pie(labels = data_summ.iloc[0:-2,:].type.unique(),
					 values = data_summ.iloc[0:-2,:].type.value_counts(), hole = 0.4)
	])
fig3.update_traces(hoverinfo = 'label+percent', textinfo = 'value', textfont_size = 30,
				   marker_line_color = 'black', marker_line_width = 2, opacity = 0.6,
				   marker = dict(colors = ['orange', 'blue']))
fig3.update_layout()
# fig3.show()

#Fig4: Creating bar charts to show information about unique values

fig4 = make_subplots(rows = 2, cols = 4, subplot_titles = list(data_summ[data_summ.type == 'categorical'].name))
fig4.add_trace(go.Bar(name = 'sex', x = data.sex.unique(), y = data.sex.value_counts(),
						text = plcmnt_records.sex.unique(), marker_color = 'blue'),
					   row = 1, col = 1)
fig4.add_trace(go.Bar(name = 'ssc_b', x = data.ssc_b.unique(), y = data.ssc_b.value_counts(),
						text = plcmnt_records.ssc_b.unique(), marker_color = 'blue'),
					   row = 1, col = 2)
fig4.add_trace(go.Bar(name = 'hsc_b', x = data.hsc_b.unique(), y = data.hsc_b.value_counts(),
						text = plcmnt_records.hsc_b.unique(), marker_color = 'blue'),
						row = 1, col = 3)
fig4.add_trace(go.Bar(name = 'hsc_s', x = data.hsc_s.unique(), y = data.hsc_s.value_counts(),
						text = plcmnt_records.hsc_s.unique(), marker_color = 'blue'),
						row = 1, col = 4)
fig4.add_trace(go.Bar(name = 'degree_t', x = data.degree_t.unique(), y = data.degree_t.value_counts(),
						text = plcmnt_records.degree_t.unique(), marker_color = 'blue'),
						row = 2, col = 1)
fig4.add_trace(go.Bar(name = 'workex', x = data.workex.unique(), y = data.workex.value_counts(),
						text = plcmnt_records.workex.unique(), marker_color = 'blue'),
						row = 2, col = 2)
fig4.add_trace(go.Bar(name = 'specialisation', x = data.specialisation.unique(), y = data.specialisation.value_counts(),
						text = plcmnt_records.specialisation.unique(), marker_color = 'blue'),
						row = 2, col = 3)
fig4.add_trace(go.Bar(name = 'status', x = data.status.unique(), y = data.status.value_counts(),
						text = plcmnt_records.status.unique(), marker_color = 'blue'),
						row = 2, col = 4)

fig4.update_layout(showlegend = False)
fig4.show()



