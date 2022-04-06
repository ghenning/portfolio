import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

### app setup
app = Dash(__name__)

### dataframe manipulation
# read the csv
df = pd.read_csv('Deaths_by_Police_US.csv',encoding='windows-1252')
# drop some columns
df = df.drop(['id','name'],axis=1)
# drop NaN values
df = df.dropna()
# convert dates to datetime
df.date = pd.to_datetime(df.date)

### app layout
app.layout = html.Div(
	children=[

		html.Div( # top section here 
			children=[
				html.H1(
					children='Fatal Police Shootings in the USA',className='header-title'
				),
				html.P(
					children='This dataset is from the Washington Post,'
						' describing the circumstances of each fatal'
						' police shooting in the USA from 2015-2017.'
						' The dataset presented here has been reduced'
						' by roughly 10% due to NaN values.',
					className='header-description',
				),
			],
			className='header',
		),

		html.Div( # choropleth
			children=[
				html.Div(
					children=dcc.Graph(id='my_choropleth',config={'displayModeBar':False})#,figure={})
				),
			],
		),

		html.Div( # line plot and selector
			children=[
				html.Div(children=[
					html.Div(
						children=html.H2('Plot Type'),
					),
					dcc.Dropdown(
						id='slct_plot',
						options=[
							{"label":"Monthly Deaths","value":"monthly_deaths"},
							{"label":"Average Age","value":"average_age"},
							{"label":"Body Cams","value":"body_cams"},
						],
						value="monthly_deaths",
						clearable=False,
						searchable=False,
						style={'color':'black'},
					),
				],className='selector'),
				html.Div(
					children=dcc.Graph(
						id='my_plot',
					),
				),
			],
		),

		html.Div( # donuts and selector
			children=[
				html.Div(children=[
					html.Div(
						children=html.H2('Donut Type'),
					),
					dcc.Dropdown(
						id='slct_donut',
						options=[
							{"label":"Gender","value":"Gender"},
							{"label":"Race","value":"Race"},
							{"label":"Body Cam","value":"body_cams2"},
						],
						value="Gender",
						clearable=False,
						searchable=False,
						style={'color':'black'},
					),
				],className='selector'),
				html.Div(
					children=dcc.Graph(
						id='my_donut',
					)
				),
			],
		),
		html.Div(children=" ",className='footer'),
],className='main-body')

### connect plotly and dash components
@app.callback(
	[Output(component_id='my_choropleth',component_property='figure'),
	Output(component_id='my_plot',component_property='figure'),
	Output(component_id='my_donut',component_property='figure')],
	[Input(component_id='slct_plot',component_property='value'),
	Input(component_id='slct_donut',component_property='value')]
)

def update_charts(plot_select,donut_select):

	### choropleth
	# get the data
	df_by_state = df.groupby(by=['state'],as_index=False).agg({'date':pd.Series.count})
	# make the map
	chmap = px.choropleth(df_by_state,
						locations='state',
						locationmode='USA-states',
						scope='usa',
						color='date',
						hover_name='state',
						color_continuous_scale=px.colors.sequential.Viridis_r,
						labels={'date':'Deaths'})

	chmap.update_layout(title="Deaths caused by police in the USA (2015-2017)",
						coloraxis_showscale=True)

	### line plots
	# get the data
	df_deaths = df.groupby(df.date.dt.strftime('%Y-%m')).age.count()
	df_age = df.groupby(df.date.dt.strftime('%Y-%m')).age.mean()
	df_cam = df.groupby(df.date.dt.strftime('%Y-%m')).body_camera.value_counts()
	df_cam = df_cam.unstack().add_prefix('cam_').reset_index().rename_axis(None,axis=1)
	# make the plot
	if plot_select == 'monthly_deaths':
		linefig = px.line(df_deaths,
						x=df_deaths.index,
						y=df_deaths.values)
		linefig.update_layout(title="Deaths per month",
						xaxis_title='Month',
						yaxis_title='Deaths')
		linefig.update_xaxes(tickangle=45)
	elif plot_select == 'average_age':
		linefig = px.line(df_age,
						x=df_age.index,
						y=df_age.values.astype(int))
		linefig.update_layout(title="Average age of a person's death",
						xaxis_title='Month',
						yaxis_title='Age')
		linefig.update_xaxes(tickangle=45)
	elif plot_select == 'body_cams':
		linefig = px.line(df_cam,
						x=df_cam.date,
						y=df_cam.columns[1:],
						labels={'variable':'Body Cam'})
		linefig.update_layout(title="Were body cams used?",
						xaxis_title='Month',
						yaxis_title='Count')
		linefig.update_xaxes(tickangle=45)

	### donuts
	# get the data
	df_gender = df.groupby(by='gender',as_index=False).agg({'date':pd.Series.count})
	df_gender = df_gender.rename(columns={'date':'count'})
	df_race = df.groupby(by='race',as_index=False).agg({'date':pd.Series.count})
	df_race = df_race.rename(columns={'date':'count'})
	df_camcount = df.groupby(by='body_camera',as_index=False).agg({'date':pd.Series.count})
	df_camcount = df_camcount.rename(columns={'date':'count'})
	# make the plot
	if donut_select == 'Gender':
		donut = px.pie(data_frame=df_gender,
					values='count',
					hover_name = 'gender',
					hole=.4,
					names='gender',
					title='Deaths split into gender')
		donut.update_traces(textposition='inside',textinfo='label+percent')	
	elif donut_select == 'Race':
		donut = px.pie(data_frame=df_race,
					values='count',
					hover_name = 'race',
					hole=.4,
					names='race',
					title='Deaths split into race')
		donut.update_traces(textposition='inside',textinfo='label+percent')	
	elif donut_select == 'body_cams2':
		donut = px.pie(data_frame=df_camcount,
					values='count',
					hover_name = 'body_camera',
					hole=.4,
					names='body_camera',
					title='Deaths split into body cam usage')
		donut.update_traces(textposition='inside',textinfo='label+percent')	

	return chmap,linefig,donut

if __name__ == "__main__":
	#app.run_server(debug=True)
	app.run_server()
