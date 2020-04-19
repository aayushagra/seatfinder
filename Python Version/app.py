from flask import Flask
from flask import render_template
from flask import request
import subprocess
import glob
import json

app = Flask(__name__)
num_of_seats = 3

def intToChar(i, j):
    return chr(i+97) + str(j+1)

@app.route('/')
def hello_world():
    data = glob.glob("movies/*.json")
    movies = []
    for i in data:
        with open(i) as f_in:
            movies.append(json.load(f_in))
    return render_template('index.html', movies=movies)

@app.route('/findseats')
def find_seats():
    numseats = request.args.get('numseats')
    movie_name = request.args.get('title')
    
    recommended_seats = subprocess.getoutput('node main.ts ' + str(numseats))
    return 'The recommended seats are: ' + recommended_seats

@app.route('/createmovie')
def create_movie():    
    movie_name = request.args.get('moviename')
    rows = request.args.get('numrows')
    cols = request.args.get('numcols')
    summary = request.args.get('summary')
    genre = request.args.get('genre')
    year = request.args.get('year')
    imdb = request.args.get('imdb')

    final = {
        'title': movie_name,
        'summary': summary,
        'genre': genre,
        'year': year,
        'imdb': imdb,
        'venue': {
            'layout': {
                'rows': 0,
                'columns': 0
            }
        },
        'seats': {}
    }

    final['venue']['layout']['rows'] = rows
    final['venue']['layout']['columns'] = cols

    for i in range(int(rows)):
        for j in range(int(cols)):
            seatId = intToChar(i, j)
            final['seats'][seatId] = {
                'id': seatId,
                'row': seatId[0],
                'column': seatId[1],
                'status': 'AVAILABLE'
            }

    with open('movies/' + movie_name + '.json', 'w') as f:
        f.write(json.dumps(final,sort_keys=True,indent=4))

    return json.dumps(final,sort_keys=True,indent=4)
