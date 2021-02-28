import time 

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import Response

from model import MyRecommender


app = Flask(__name__)

    
@app.route('/')
def ask_favorite_movie():
    return render_template('base.html')

@app.route('/recommendations', methods=['POST'])
def recommende_movies():
    robot = MyRecommender()
    favorite_movie = request.form['favorite_movie']
    movies = robot.recommende_movies(str(favorite_movie))
  
    return jsonify({'movies': movies})

def main():
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
    
if __name__ == '__main__':
    main()
    
    