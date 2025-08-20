from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from models import db, User, Movie, WatchHistory, user_favorite_movies, Recommendation, TVShow
import re
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt 
from werkzeug.security import check_password_hash
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy.sql import func
import random
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt()
load_dotenv()

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email') 
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')
    
    if not confirmPassword or not password:
        return jsonify({'message': 'Passwords fields cannot be empty!'}) 
    if confirmPassword != password:
        return jsonify({'message': 'Password do not match!'})
    if not username.strip() or not password.strip() or not email.strip():
        return jsonify({'message': 'All fields are required!'}), 400
    if len(username) < 3 or len(username) > 20:
        return jsonify({'message': 'Username must be between 3 and 20 chracters!'}), 400
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'message': 'Username can only contain letters,numbers and underscores!'}), 400
    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format!'}), 400
    if len(password) < 6:
        return jsonify({'message': 'Password is too short'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Usarname already registered'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'This email already in system'}), 400
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration succesful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({'access_token': access_token,'refresh_token': refresh_token,'message': 'Login succesful!'}), 200

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)
   
def fetch_and_save_movies():
    api_key = app.config["API_KEY"]
    count = 0
    for page in range(10, 80):
        url = f'{app.config["BASE_URL1"]}popular?api_key={api_key}&language=en-US&page={page}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() 
            for movie_data in data['results']:
                movie = {
                    'tmdb_id': str(movie_data['id']),
                    'title': movie_data['title'],
                    'genre': movie_data['genre_ids'][0] if movie_data['genre_ids'] else 'N/A',
                    'description': movie_data['overview'],
                    'release_date': movie_data['release_date'] if movie_data['release_date'] else None,
                    'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data['poster_path'] else None,
                    'imdb_id': None,
                    'imdb_rating': movie_data['vote_average'],
                    'vote_count': movie_data['vote_count'] if 'vote_count' in movie_data else 0,
                    'runtime': 'N/A'
                }
                if not Movie.query.filter_by(tmdb_id=movie['tmdb_id']).first():
                    movie_object = Movie(**movie)
                    db.session.add(movie_object)
                    count += 1
            db.session.commit()
        else: 
            print(f"Error fetching page {page}:{response.status_code}")
            break
    print(f'{count} movies have been added to database.')

def fetch_and_save_tvshows():
    api_key = app.config["API_KEY"]
    count = 0
    for page in range(80, 100):
        url = f'{app.config["BASE_URL2"]}popular?api_key={api_key}&language=en-US&page={page}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for tv_show_data in data['results']:
                tv_show = {
                    'tmdb_id': str(tv_show_data['id']),
                    'title': tv_show_data.get('name', 'Uknown title'),
                    'genre': tv_show_data['genre_ids'][0] if tv_show_data['genre_ids'] else 'N/A',
                    'description': tv_show_data['overview'],
                    'release_date': tv_show_data['first_air_date'] if tv_show_data['first_air_date'] else None,
                    'poster_url': f"https://image.tmdb.org/t/p/w500{tv_show_data['poster_path']}" if tv_show_data['poster_path'] else None,
                    'imdb_id': None,
                    'imdb_rating': tv_show_data['vote_average'],
                    'vote_count': tv_show_data['vote_count'] if 'vote_count' in tv_show_data else 0,
                    'number_of_seasons': tv_show_data.get('number_of_seasons', None),
                    'number_of_episodes': tv_show_data.get('number_of_episodes'),
                }
                if not TVShow.query.filter_by(tmdb_id=tv_show['tmdb_id']).first():
                    tv_show_object = TVShow(**tv_show)
                    db.session.add(tv_show_object)
                    count += 1
            db.session.commit()        
        else:
            print(f"Error fetching page {page}:{response.status_code}")
            break
    print(f'{count} tvshows have been added to database.')

@app.route('/movie/popular', methods=['GET'])
def get_popular_movie():
    movies = Movie.query.filter(Movie.vote_count > 10000).order_by(Movie.imdb_rating.desc()).limit(12)
    return jsonify([movie.serialize() for movie in movies])

@app.route('/tvshow/popular', methods=['GET'])
def get_popular_tvshow():
    tvshows = TVShow.query.filter(TVShow.vote_count > 10000).order_by(TVShow.imdb_rating.desc()).limit(12)
    return jsonify([tvshow.serialize() for tvshow in tvshows])  

@app.route('/movie/new', methods=['GET'])
def get_new_movie():
    new_release_date = datetime(2023, 1, 1)
    movies = Movie.query.filter(Movie.release_date > new_release_date, Movie.vote_count > 3000).order_by(Movie.imdb_rating.desc()).limit(12)    
    return jsonify([movie.serialize() for movie in movies])
     
@app.route('/tvshow/new', methods=['GET'])  
def get_new_tvshow():
    new_release_date = datetime(2023, 1, 1)
    tvshows = TVShow.query.filter(TVShow.release_date > new_release_date, TVShow.vote_count > 500).order_by(TVShow.imdb_rating.desc()).limit(12)
    return jsonify([tvshow.serialize() for tvshow in tvshows]) 

@app.route('/movie/random', methods=['GET'])
def get_random_movie():
    total_movies = Movie.query.filter(Movie.vote_count > 5000, Movie.imdb_rating > 8.5).count()
    random_index = random.randint(0, total_movies - 1)
    movie = Movie.query.filter(Movie.vote_count > 5000, Movie.imdb_rating > 8.0).offset(random_index).first()
    return jsonify(movie.serialize() if movie else jsonify({'msg': 'Movie not found'}))

@app.route('/tvshow/random', methods=['GET'])
def get_random_tvshow():
    total_tvshows = TVShow.query.filter(TVShow.vote_count > 2000, TVShow.imdb_rating > 8.0).count()
    random_index = random.randint(0, total_tvshows - 1)
    tvshow = TVShow.query.filter(TVShow.vote_count > 2000, TVShow.imdb_rating > 8).offset(random_index).limit(2).first()
    return jsonify(tvshow.serialize() if tvshow else jsonify({'msg': 'TVShow not found'})) 

@app.route('/watch-history/add', methods=['POST'])
@jwt_required()
def add_watch_history():
    user_id = get_jwt_identity()
    data = request.get_json()
    movie = data.get("movie_id")
    tv_show = data.get("tv_show_id")
    rating = data.get("rating")
    if ((movie and tv_show) or (not movie and not tv_show)):
        return jsonify({'error': 'You must specify exactly one content type (movie or tvshow)'}), 400
    if movie:
        movie = Movie.query.get(movie)
        if not movie:
            return jsonify({'error': 'Specified movie not found!'}), 404
    if tv_show:
        tv_show = TVShow.query.get(tv_show)
        if not tv_show:
            return jsonify({'error': 'Specified tvshow not found!'}), 404
    existing_record = WatchHistory.query.filter_by(user_id=user_id, tv_show_id=tv_show.id if tv_show else None, movie_id=movie.id if movie else None).first()
    if existing_record:
        existing_record.rating = rating or existing_record.rating 
        db.session.commit()
        return jsonify({'message': 'Watch history updated'}), 200
    new_watch = WatchHistory(user_id=user_id, movie_id=movie.id if movie else None, tv_show_id=tv_show.id if tv_show else None, rating=rating)
    db.session.add(new_watch)    
    db.session.commit()
    return jsonify({'message': 'Watch history added'}), 201

@app.route('/search', methods=['GET'])
def search(): 
    query = request.args.get('query', '').strip() 
    if not query:
        return jsonify({'error': 'Query parameter is required!'})
    movies = Movie.query.filter(Movie.title.ilike(f'%{query}%')).all()
    tvshows = TVShow.query.filter(TVShow.title.ilike(f'%{query}%')).all()
    results = {
        'movies': [m.serialize() for m in movies],
        'tvshows': [t.serialize() for t in tvshows] 
    }
    return jsonify(results)

@app.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    user_id = get_jwt_identity()
    watched = WatchHistory.query.filter_by(user_id=user_id).all()  
    watched_movie_ids = [w.movie_id for w in watched if w.movie_id]
    watched_tvshow_ids = [w.tv_show_id for w in watched if w.tv_show_id]
    recommend_movies = Movie.query.filter(~Movie.id.in_(watched_movie_ids)).order_by(Movie.imdb_rating.desc()).limit(5).all()
    recommend_tvshows = TVShow.query.filter(~TVShow.id.in_(watched_tvshow_ids)).order_by(TVShow.imdb_rating.desc()).limit(5).all()
    return jsonify({'movies': [m.serialize() for m in recommend_movies],'tvshows': [t.serialize() for t in recommend_tvshows]})

@app.route('/watch-history/list', methods=['GET'])
@jwt_required()
def get_watch_history():
    user_id = get_jwt_identity() 
    history = WatchHistory.query.filter_by(user_id=user_id).all()
    movie_ids = list({record.movie_id for record in history if record.movie_id})
    tvshow_ids = list({record.tv_show_id for record in history if record.tv_show_id})  
    return jsonify({'movies': movie_ids,'tvshows': tvshow_ids})

if __name__ == '__main__':
    app.run()
