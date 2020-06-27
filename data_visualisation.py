import mysql.connector as sqlcon  # Calling required libraries and functions
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statistics as stats


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
data['status'] = data['status'].replace(['Not Placed', 'Placed'], [0,1])


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
											fill_color = 'limegreen', # Note for every column a diff color can be given by passing an array of colurs[c1,...,cN]
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
fig1.update_layout(width = 1000, height = 1500, title = {'text':'Summary Table', 'x': 0.08, 'y': 0.95},
				   font = dict(size = 18), template = 'presentation') # changes web page dimension
fig1.show()


#Fig 2: Stacked Bar chart showing missing data information and column type with hover text
fig2 = go.Figure(data = [
			go.Bar(name = 'Available ', x = data_summ.name, y = 100 - data_summ.perc_of_NAs, hovertext = data_summ.type, marker_color = 'blue'),
			go.Bar(name = 'Missing ', x = data_summ.name, y = data_summ.perc_of_NAs, hovertext = data_summ.type, marker_color = 'limegreen')
		])
fig2.update_traces(marker_line_color = 'black', marker_line_width = 2, opacity = 0.6)
fig2.update_layout(title = {'text':'Missing Data Information', 'y': 0.92},xaxis_title = 'column', barmode = 'stack',
				   yaxis_title = 'Missing Data Information', font = dict(size = 18), template = 'presentation')
fig2.show()


# Fig3: Pie chart showing how many columns are categorical and how many are numeric
fig3 = go.Figure(data = [
			go.Pie(labels = data_summ.iloc[0:-2,:].type.unique(),
					 values = data_summ.iloc[0:-2,:].type.value_counts(), hole = 0.4)
	])
fig3.update_traces(hoverinfo = 'label+percent', textinfo = 'value', textfont_size = 30,
				   marker_line_color = 'black', marker_line_width = 2, opacity = 0.6,
				   marker = dict(colors = ['limegreen', 'blue']))
fig3.update_layout(title = {'text': 'Categorical vs Numeric Variables Share', 'y':0.92},
				   font = dict(size = 18), template = 'presentation')
fig3.show()

# Fig4: Creating Boxplot to show features of numerical variables in data
fig4 = go.Figure(data = [
			go.Box(name = 'ssc_p',y = data.ssc_p, boxmean = True, boxpoints = 'all', marker_color = 'blue')
			])
fig4.add_trace(go.Box(name = 'hsc_p', y = data.hsc_p, boxmean = True, boxpoints = 'all', marker_color = 'blue'))
fig4.add_trace(go.Box(name = 'degree_p', y = data.degree_p, boxmean = True, boxpoints = 'all', marker_color = 'blue'))
fig4.add_trace(go.Box(name = 'mba_p', y = data.mba_p, boxmean = True, boxpoints = 'all', marker_color = 'blue'))
fig4.add_trace(go.Box(name = 'etest_p', y = data.etest_p, boxmean = True, boxpoints = 'all', marker_color = 'blue'))
fig4.add_trace(go.Scatter(x = ['ssc_p', 'hsc_p', 'degree_p', 'mba_p', 'etest_p'],
						  y = [stats.median(data.ssc_p), stats.median(data.hsc_p), stats.median(data.degree_p),
						  	   stats.median(data.mba_p), stats.median(data.etest_p)],
						  	   mode = 'lines + markers', name = 'median', 
						  	   line = dict(color = 'black', width = 2)))
fig4.add_trace(go.Scatter(x = ['ssc_p', 'hsc_p', 'degree_p', 'mba_p', 'etest_p'],
						  y = [stats.mean(data.ssc_p), stats.mean(data.hsc_p), stats.mean(data.degree_p),
						  	   stats.mean(data.mba_p), stats.mean(data.etest_p)],
						  	   mode = 'lines + markers', name = 'mean',
						  	   line = dict(color = 'black', width = 2, dash = 'dash')))
fig4.update_traces(opacity = 0.7)
fig4.update_layout(title = {'text':'Summary Statistics of Numerical Variables', 'y':0.91}, xaxis_title = 'Variable',
				   yaxis_title = 'Marks(in %)', font = dict(size = 18), template = 'presentation')
fig4.show()

#Fig5: Creating bar charts to show information about unique values

fig5 = go.Figure(data = [
			go.Bar(name = 'Female', x = ['sex'], y = [round(sum(data.sex == 0)*factor,2)], marker_color = 'blue', text = 'Female', textposition = 'auto'),
			go.Bar(name = 'Male', x = ['sex'], y = [round(sum(data.sex == 1)*factor,2)], marker_color = 'limegreen', text = 'Male', textposition = 'auto')		
		])

fig5.add_trace(go.Bar(name = 'Others', x = ['ssc_b'], y = [round(sum(data.ssc_b == 0)*factor,2)], marker_color = 'blue', text = 'Others', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Central', x = ['ssc_b'], y = [round(sum(data.ssc_b == 1)*factor,2)], marker_color = 'limegreen', text = 'Central', textposition = 'auto'))

fig5.add_trace(go.Bar(name = 'Others', x = ['hsc_b'], y = [round(sum(data.hsc_b == 0)*factor,2)], marker_color = 'blue', text = 'Others', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Central', x = ['hsc_b'], y = [round(sum(data.hsc_b == 1)*factor,2)], marker_color = 'limegreen', text = 'Central', textposition = 'auto'))

fig5.add_trace(go.Bar(name = 'Commerce', x = ['hsc_s'], y = [round(sum(data.hsc_s == 0)*factor,2)], marker_color = 'blue', text = 'Commerce', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Science', x = ['hsc_s'], y = [round(sum(data.hsc_s == 1)*factor,2)], marker_color = 'limegreen', text = 'Science', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Arts', x = ['hsc_s'], y = [round(sum(data.hsc_s == 2)*factor,2)], marker_color = 'lightskyblue', text = 'Arts', textposition = 'auto'))

fig5.add_trace(go.Bar(name = 'Sci&Tech', x = ['degree_t'], y = [round(sum(data.degree_t == 0)*factor,2)], marker_color = 'blue', text = 'Sci&Tech', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Comm&Mgmt', x = ['degree_t'], y = [round(sum(data.degree_t == 1)*factor,2)], marker_color = 'limegreen', text = 'Comm&Mgmt', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Others', x = ['degree_t'], y = [round(sum(data.degree_t == 2)*factor,2)], marker_color = 'lightskyblue', text = 'Others', textposition = 'auto'))

fig5.add_trace(go.Bar(name = 'No', x = ['workex'], y = [round(sum(data.workex == 0)*factor,2)], marker_color = 'blue', text = 'No', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Yes', x = ['workex'], y = [round(sum(data.workex == 1)*factor,2)], marker_color = 'limegreen', text = 'Yes', textposition = 'auto'))

fig5.add_trace(go.Bar(name = 'Mkt&HR', x = ['specialisation'], y = [round(sum(data.specialisation == 0)*factor,2)],
				marker_color = 'blue', text = 'Mkt&HR', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Mkt&Fin', x = ['specialisation'], y = [round(sum(data.specialisation == 1)*factor,2)],
				marker_color = 'limegreen', text = 'Mkt&Fin', textposition = 'auto'))

fig5.add_trace(go.Bar(name = 'Not Placed', x = ['status'], y = [round(sum(data.status == 0)*factor,2)], marker_color = 'blue', text = 'Not Placed', textposition = 'auto'))
fig5.add_trace(go.Bar(name = 'Placed', x = ['status'], y = [round(sum(data.status == 1)*factor,2)], marker_color = 'limegreen', text = 'Placed', textposition = 'auto'))

fig5.update_traces(marker_line_color = 'black',marker_line_width = 1, opacity = 0.8)
fig5.update_layout(barmode = 'stack', showlegend = False, 
					title = {'text':'Composition of Factors in a Categorical Variable', 'y': 0.92},
					xaxis_title = 'Variable', yaxis_title = 'factors(perc of rows)',
					font = dict(size = 20), template = 'presentation')
fig5.show()


#Fig6: A plot containing two subplots showcasing the statistical properties of th dependent variable ie salary
data_placed = data[data.status == 1]
salary = data_placed.salary.sort_values()
nbins = 10
temp_index = [int(len(salary)/nbins*i) for i in range(0,nbins+1,1)]
bins_avg = list([0])
i = 0
while i+1 < len(temp_index):
	x_mean = round(sum(salary.iloc[temp_index[i]:temp_index[i+1]])/sum(salary)*100,2)
	bins_avg.append(x_mean)
	i = i+1

cum_share = [sum(bins_avg[0:i]) for i in range(1,nbins+2)]
perc_index = [100/nbins*i for i in range(nbins+1)]

pkg_dist_table = pd.DataFrame([perc_index, bins_avg, cum_share]).T
pkg_dist_table.columns = ['popn_perc', 'salary_share', 'cum_share']

fig6A = go.Figure(data = [
			go.Scatter(name = 'salary_distribution', x = pkg_dist_table.popn_perc, y = pkg_dist_table.cum_share,
					   line = dict(color = 'blue', width = 3))
	])
fig6A.add_trace(go.Scatter(name = 'line of perfect equality', x = pkg_dist_table.popn_perc, y = pkg_dist_table.popn_perc,
						   line = dict(color = 'limegreen', width = 3)))
fig6A.update_layout(title = {'text': 'Package\'s Inequality', 'y':0.91}, font = dict(size = 18),
				    xaxis_title = 'Population Percentile(Placed)', yaxis_title = 'Salary Percentile',
				    template = 'presentation')
fig6A.show()

fig6B = make_subplots(rows = 2, cols = 1, subplot_titles = (' ', ' '),
					  shared_xaxes = True, vertical_spacing = 0.1, row_heights = [0.4, 0.7])
fig6B.add_trace(go.Box(name = ' ', x = salary, boxpoints = 'all', boxmean = True, marker_color = 'blue'), row = 1, col = 1)
fig6B.add_trace(go.Histogram(name = 'salary', x = salary, nbinsx = nbins*2, marker_color = 'limegreen', marker_line_color = 'black',
							 marker_line_width = 2), row = 2, col = 1)
fig6B.update_xaxes(title_text = 'Salary (in Rs)', row = 2, col = 1)
fig6B.update_yaxes(title_text = 'Number of Offers', row = 2, col =1)
fig6B.update_yaxes(title_text = ' ', row = 1, col = 1)
fig6B.update_xaxes(showgrid = False, row = 1, col = 1)
fig6B.update_traces(opacity = 0.8, showlegend = False)
fig6B.update_layout(template = 'presentation', title = {'text':'Statistical Summaries of Salary Package'}, font = dict(size = 18))

fig6B.show()

