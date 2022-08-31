from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = Dash(__name__, external_stylesheets=external_stylesheets)
app = Dash(__name__)
server = app.server

### dataframe stuff
df = pd.read_csv('2021-2022 Football Player Stats.csv',sep=';')
df = df[df['Min']>1400]

# position to dataframe position dictionary
pos_dict = {'GKs':['GK'],'DFs':['DF','DFFW','DFMF'],
			'MFs':['MF','MFFW','MFDF'],'FWs':['FW','FWDF','FWMF']}

# dropdown options
drop_opts = [
{'label':'Player age','value':'Age'},
{'label':'Matches played','value':'MP'},
{'label':'Matches started','value':'Starts'},
{'label':'Minutes played','value':'Min'},
{'label':'Minutes played/90','value':'90s'},
{'label':'Goals scored or allowed','value':'Goals'},
{'label':'Shots total','value':'Shots'},
{'label':'Shots on target','value':'SoT'},
{'label':'Shots on target accuracy','value':'SoT%'},
{'label':'Goals per shot','value':'G/Sh'},
{'label':'Goals per shot on target','value':'G/SoT'},
{'label':'Average shot distance','value':'ShoDist'},
{'label':'Shots from free kikcs','value':'ShoFK'},
{'label':'Shots from penalty kicks','value':'ShoPK'},
{'label':'Passes completed','value':'PasTotCmp'},
{'label':'Passes attempted','value':'PasTotAtt'},
{'label':'Passing accuracy','value':'PasTotCmp%'},
{'label':'Total distance (yds) of completed passes','value':'PasTotDist'},
{'label':'Total distance (yds) of progressive passes','value':'PasTotPrgDist'},
{'label':'Short passes completed (5-15 yds)','value':'PasShoCmp'},
{'label':'Short passes attempted (5-15 yds)','value':'PasShoAtt'},
{'label':'Short passes accuracy (5-15 yds)','value':'PasShoCmp%'},
{'label':'Medium passes completed (15-30 yds)','value':'PasMedCmp'},
{'label':'Medium passes attempted (15-30 yds)','value':'PasMedAtt'},
{'label':'Medium passes accuracy (15-30 yds)','value':'PasMedCmp%'},
{'label':'Long passes completed (30+ yds)','value':'PasLonCmp'},
{'label':'Long passes attempted (30+ yds)','value':'PasLonAtt'},
{'label':'Long passes accuracy (30+ yds)','value':'PasLonCmp%'},
{'label':'Assists','value':'Assists'},
{'label':'Assisted shots','value':'PasAss'},
{'label':'Passes into final third','value':'Pas3rd'},
{'label':'Passes into penalty area','value':'PPA'},
{'label':'Crosses into penalty area','value':'CrsPA'},
{'label':'Progressive passes','value':'PasProg'},
{'label':'Attempted passes','value':'PasAtt'},
{'label':'Live-ball passes','value':'PasLive'},
{'label':'Dead-ball passes','value':'PasDead'},
{'label':'Free kick passes','value':'PasFK'},
{'label':'Through balls','value':'TB'},
{'label':'Passes under pressure','value':'PasPress'},
{'label':'Flank-switching passes','value':'Sw'},
{'label':'Crosses','value':'PasCrs'},
{'label':'Corners','value':'CK'},
{'label':'Inswinging corners','value':'CkIn'},
{'label':'Outswinging corners','value':'CkOut'},
{'label':'Straight corners','value':'CkStr'},
{'label':'Ground passes','value':'PasGround'},
{'label':'Low passes','value':'PasLow'},
{'label':'High passes','value':'PasHigh'},
{'label':'Left foot passes','value':'PaswLeft'},
{'label':'Right foot passes','value':'PaswRight'},
{'label':'Head passes','value':'PaswHead'},
{'label':'Throw-ins','value':'TI'},
{'label':'Non-head/foot passes','value':'PaswOther'},
{'label':'Passes completed','value':'PasCmp'},
{'label':'Offside passes','value':'PasOff'},
{'label':'Out of bounds passes','value':'PasOut'},
{'label':'Passes intercepted','value':'PasInt'},
{'label':'Blocked passes','value':'PasBlocks'},
{'label':'Shot-creating actions','value':'SCA'},
{'label':'Shot-creating live-ball passes','value':'ScaPassLive'},
{'label':'Shot-creating dead-ball passes','value':'ScaPassDead'},
{'label':'Shot-creating dribbles','value':'ScaDrib'},
{'label':'Shot-creating shots','value':'ScaSh'},
{'label':'Shot-creating fouls drawn','value':'ScaFld'},
{'label':'Shot-creating defensive actions','value':'ScaDef'},
{'label':'Goal-creating actions','value':'GCA'},
{'label':'Goal-creating live-ball passes','value':'GcaPassLive'},
{'label':'Goal-creating dead-ball passes','value':'GcaPassDead'},
{'label':'Goal-creating dribbles','value':'GcaDrib'},
{'label':'Goal-creating shots','value':'GcaSh'},
{'label':'Goal-creating fouls drawn','value':'GcaFld'},
{'label':'Goal-creating defensive actions','value':'GcaDef'},
{'label':'Tackles','value':'Tkl'},
{'label':'Tackles won','value':'TklWon'},
{'label':'Tackles in defensive third','value':'TklDef3rd'},
{'label':'Tackles in center pitch','value':'TklMid3rd'},
{'label':'Tackles in attacking third','value':'TklAtt3rd'},
{'label':'Dribblers tackled','value':'TklDri'},
{'label':'Times dribbled past + number of tackles','value':'TklDriAtt'},
{'label':'Percentage of dribblers tackled','value':'TklDri%'},
{'label':'Times dribbled past','value':'TklDriPast'},
{'label':'Number of presses','value':'Press'},
{'label':'Successful presses','value':'PresSucc'},
{'label':'Press success','value':'Press%'},
{'label':'Presses in defensive third','value':'PresDef3rd'},
{'label':'Presses in center pitch','value':'PresMid3rd'},
{'label':'Presses in attacking third','value':'PresAtt3rd'},
{'label':'Blocks','value':'Blocks'},
{'label':'Blocked shots','value':'BlkSh'},
{'label':'Blocked shots on target','value':'BlkShSv'},
{'label':'Blocked passes','value':'BlkPass'},
{'label':'Interceptions','value':'Int'},
{'label':'Tackles + Interceptions','value':'Tkl+Int'},
{'label':'Clearances','value':'Clr'},
{'label':'Errors leading to a shot','value':'Err'},
{'label':'Touches','value':'Touches'},
{'label':'Touches in own penalty area','value':'TouDefPen'},
{'label':'Touches in defensive third','value':'TouDef3rd'},
{'label':'Touches in center pitch','value':'TouMid3rd'},
{'label':'Touches in attacking third','value':'TouAtt3rd'},
{'label':'Touches in attacking penalty area','value':'TouAttPen'},
{'label':'Touches, live-balls','value':'TouLive'},
{'label':'Successful dribbles','value':'DriSucc'},
{'label':'Attempted dribbles','value':'DriAtt'},
{'label':'Dribble success','value':'DriSucc%'},
{'label':'Number of players dribbled past','value':'DriPast'},
{'label':'Nutmegs','value':'DriMegs'},
{'label':'Carries','value':'Carries'},
{'label':'Total carry distance (yds)','value':'CarTotDist'},
{'label':'Progressive carry distance (yds)','value':'CarPrgDist'},
{'label':'Progressive carries','value':'CarProg'},
{'label':'Carries into final third','value':'Car3rd'},
{'label':'Carries into penalty area','value':'CPA'},
{'label':'Failed carries','value':'CarMis'},
{'label':'Dispossessed','value':'CarDis'},
{'label':'Number as target of attempted pass','value':'RecTarg'},
{'label':'Number of passes received','value':'Rec'},
{'label':'Passes received success','value':'Rec%'},
{'label':'Progressive passes received','value':'RecProg'},
{'label':'Yellow cards','value':'CrdY'},
{'label':'Red cards','value':'CrdR'},
{'label':'Second yellow card','value':'2CrdY'},
{'label':'Fouls committed','value':'Fls'},
{'label':'Fouls drawn','value':'Fld'},
{'label':'Offsides','value':'Off'},
{'label':'Crosses','value':'Crs'},
{'label':'Tackles won','value':'TklW'},
{'label':'Penalty kicks won','value':'PKwon'},
{'label':'Penalty kicks conceded','value':'PKcon'},
{'label':'Own goals','value':'OG'},
{'label':'Loose balls recovered','value':'Recov'},
{'label':'Aerials won','value':'AerWon'},
{'label':'Aerials lost','value':'AerLost'},
{'label':'Aerial success','value':'AerWon%'},
]


### app layout
app.layout = html.Div(
	children=[

	html.Div(
		children=[
			html.H1('Football player statistics - 2021/2022 season'),
			html.P(children="An interactive plotting tool to"
				" inspect statistical performances of players in"
				" the top five European leagues "
				"(Premier League, La Liga, Bundesliga, Serie A, Ligue 1)"
				" over the course of the 2021/2022 season."
				" This dashboard is a complementary tool to a"
				" project of mine."
				" Below you'll find drop-down menus for player"
				" positions and axes values for both 2-D and 3-D"
				" scatterplots. Simply select the values you want to"
				" see and click the 'SHOW ME!' button."
				" Feel free to play around and share your findings!"
			),

			html.A(children="Find my project here.",
					href="https://google.com")
		],
		className='headfoot',
	),

	html.Div(
		children=[
			html.Div(children=[
				html.Div(
					children=html.H2('2D Scatterplot'),
				),
				html.Div(
					children=html.H4('Position'),
				),
				dcc.Dropdown(
					id='input-2d-pos',
					options=[
						{'label':'Goalkeepers','value':'GKs'},
						{'label':'Defenders','value':'DFs'},	
						{'label':'Midfielders','value':'MFs'},	
						{'label':'Forwards','value':'FWs'},	
					],	
					value='DFs',
					clearable=False,
					searchable=False,
					style={'color':'black'},
				className='droppy'),
				html.Div(
					children=html.H4('X-axis'),
				),
				dcc.Dropdown(
					id='input-2d-x',
					options=drop_opts,
					value='PasProg',
					clearable=False,
					searchable=True,
					style={'color':'black'},
				className='droppy'),
				html.Div(
					children=html.H4('Y-axis'),
				),
				dcc.Dropdown(
					id='input-2d-y',
					options=drop_opts,
					value='PasMedCmp%',
					clearable=False,
					searchable=True,
					style={'color':'black'},
				className='droppy'),
			html.Button(id='submit-button-2d',n_clicks=0,
					children='Show me!',className='pltbutton'),
			]),
			html.Div(
				children=dcc.Graph(
					id='output-2d',
				),
			),
		]
	),

	html.Div(
		children=[
			html.Div(children=[
				html.Div(
					children=html.H2('3D Scatterplot'),
				),
				html.Div(
					children=html.H4('Position'),
				),
				dcc.Dropdown(
					id='input-3d-pos',
					options=[
						{'label':'Goalkeepers','value':'GKs'},
						{'label':'Defenders','value':'DFs'},	
						{'label':'Midfielders','value':'MFs'},	
						{'label':'Forwards','value':'FWs'},	
					],	
					value='DFs',
					clearable=False,
					searchable=False,
					style={'color':'black'},
				className='droppy'),
				html.Div(
					children=html.H4('X-axis'),
				),
				dcc.Dropdown(
					id='input-3d-x',
					options=drop_opts,
					value='PasProg',
					clearable=False,
					searchable=True,
					style={'color':'black'},
				className='droppy'),
				html.Div(
					children=html.H4('Y-axis'),
				),
				dcc.Dropdown(
					id='input-3d-y',
					options=drop_opts,
					value='PasMedCmp%',
					clearable=False,
					searchable=True,
					style={'color':'black'},
				className='droppy'),
				html.Div(
					children=html.H4('Z-axis'),
				),
				dcc.Dropdown(
					id='input-3d-z',
					options=drop_opts,
					value='SCA',
					clearable=False,
					searchable=True,
					style={'color':'black'},
				className='droppy'),
			html.Button(id='submit-button-3d',n_clicks=0,
					children='Show me!',className='pltbutton'),
			]),
			html.Div(
				children=dcc.Graph(
					id='output-3d',
				),
			),
		]
	),
	html.Div(children=' ',className='headfoot'),
])

@app.callback(
	Output(component_id='output-2d',component_property='figure'),
	Input('submit-button-2d','n_clicks'),
	[State('input-2d-pos','value'),
	State('input-2d-x','value'),
	State('input-2d-y','value')])
def update_2d(n,input_2d_pos,input_2d_x,input_2d_y):
	pos_list = pos_dict[input_2d_pos]
	ddf = df.loc[df['Pos'].isin(pos_list)] 
	ddf_features = ddf[[input_2d_x,input_2d_y]]
	ddf_info = ddf[['Player','Nation','Pos','Squad','Comp']]
	ddf_info.reset_index(drop=True,inplace=True)
	ddf_features.reset_index(drop=True,inplace=True)
	ddf_all = pd.concat([ddf_info,ddf_features],axis=1)
	scaler = StandardScaler()
	ddf_features_scaled = scaler.fit_transform(ddf_features)
	ddf_features_scaled = pd.DataFrame(ddf_features_scaled,
						columns=ddf_features.columns)
	tmp_X_2d = ddf_features_scaled[[input_2d_x,input_2d_y]]
	model_2d = KMeans(4)
	labels_2d = model_2d.fit_predict(tmp_X_2d)
	plot_2d = px.scatter(data_frame=ddf_all,
						x=input_2d_x,
						y=input_2d_y,
						color=labels_2d,
						hover_name='Player',
						hover_data=['Squad','Comp','Nation'],
						color_continuous_scale=px.colors.qualitative.Plotly)
	plot_2d.update_traces(marker={'size':5})
	plot_2d.update(layout_coloraxis_showscale=False)
	return plot_2d

@app.callback(
	Output(component_id='output-3d',component_property='figure'),
	Input('submit-button-3d','n_clicks'),
	[State('input-3d-pos','value'),
	State('input-3d-x','value'),
	State('input-3d-y','value'),
	State('input-3d-z','value')])
def update_3d(n,input_3d_pos,input_3d_x,input_3d_y,input_3d_z):
	pos_list_3d = pos_dict[input_3d_pos]
	ddf_3d = df.loc[df['Pos'].isin(pos_list_3d)] 
	ddf_3d_features = ddf_3d[[input_3d_x,input_3d_y,input_3d_z]]
	ddf_3d_info = ddf_3d[['Player','Nation','Pos','Squad','Comp']]
	ddf_3d_info.reset_index(drop=True,inplace=True)
	ddf_3d_features.reset_index(drop=True,inplace=True)
	ddf_3d_all = pd.concat([ddf_3d_info,ddf_3d_features],axis=1)
	scaler_3d = StandardScaler()
	ddf_3d_features_scaled = scaler_3d.fit_transform(ddf_3d_features)
	ddf_3d_features_scaled = pd.DataFrame(ddf_3d_features_scaled,
						columns=ddf_3d_features.columns)
	tmp_X_3d = ddf_3d_features_scaled[[input_3d_x,input_3d_y,input_3d_z]]
	model_3d = KMeans(4)
	labels_3d = model_3d.fit_predict(tmp_X_3d)
	plot_3d = px.scatter_3d(data_frame=ddf_3d_all,
						x=input_3d_x,
						y=input_3d_y,
						z=input_3d_z,
						color=labels_3d,
						hover_name='Player',
						hover_data=['Squad','Comp','Nation'],
						color_continuous_scale=px.colors.qualitative.Plotly)
	plot_3d.update_traces(marker={'size':5})
	plot_3d.update(layout_coloraxis_showscale=False)
	return plot_3d

if __name__ == '__main__':
	#app.run_server(debug=True)
	app.run_server()

