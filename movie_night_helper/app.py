from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms import validators
from movie_api import movie_caller

app = Flask(__name__)
app.config['SECRET_KEY'] = 'meow'

class inputs(FlaskForm):
	select_genre = SelectField(label="Genre",
		choices=['action','adventure','animation','biography',
		'comedy','crime','documentary','drama',
		'family','fantasy','film-noir','game-show',
		'history','horror','music','musical',
		'mystery','news','reality-tv','romance',
		'sci-fi','short','sport','talk-show',
		'thriller','war','western'])

	select_number = SelectField(label="Top X",
		choices=[10,50,100])
	submit = SubmitField("Find me a movie!")

@app.route('/',methods=['GET','POST'])
def index():
	form = inputs()
	if form.validate_on_submit():
		session['select_genre'] = form.select_genre.data
		session['select_number'] = int(form.select_number.data)

		return redirect(url_for("result_page"))

	return render_template('home.html',form=form)

@app.route('/result_page')
def result_page():

	# here is where the api calls happen
	mc = movie_caller()
	# call top X for genre here and parse a random result
	tmp_id = mc.get_top_x(genre=session['select_genre'],
						limit=session['select_number'])
	# call metadata from result here
	tmp_res = mc.get_meat(tmp_id)
	# title, year, runningtime, poster, 
	# imdb rating, metacritic rating, genres, PG rating
	res_title = tmp_res[0]
	res_year = tmp_res[1]
	res_runtime = tmp_res[2]
	res_poster = tmp_res[3]
	res_rate1 = tmp_res[4]
	res_rate2 = tmp_res[5]
	res_genre = tmp_res[6]
	res_age = tmp_res[7]	
	#res_title = 'angry seagulls lower the drawbridge'
	#res_title = session['select_number']
	#res_year = '2000'
	#res_runtime = 155
	#res_poster ="https://m.media-amazon.com/images/M/MV5BYjhiNjBlODctY2ZiOC00YjVlLWFlNzAtNTVhNzM1YjI1NzMxXkEyXkFqcGdeQXVyMjQxNTE1MDA@._V1_.jpg" 
	#res_rate1 = 7.7
	#res_rate2 = 6.9
	#res_genre = ['a','b','c']
	#res_age = "PG-13"

	return render_template('result_page.html',res_title=res_title,
		res_year=res_year,
		res_runtime=res_runtime,
		res_poster=res_poster,
		res_rate1=res_rate1,
		res_rate2=res_rate2,
		res_genre=res_genre,
		res_age=res_age
		)

if __name__ == '__main__':
	app.run(debug=True)
