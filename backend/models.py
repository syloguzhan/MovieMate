from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_bcrypt import Bcrypt 


bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(80),unique = True,nullable = False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),unique = True,nullable = False)

    watch_history = db.relationship('WatchHistory',backref = 'user',lazy = True)

    def set_password(self,password):
        self.password = self.hash_password(password)
        
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)

    def __repr__(self):
        return f'User {self.username}'
    
class Movie(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    tmdb_id = db.Column(db.String(100),unique = True)
    title = db.Column(db.String(200),nullable = False)
    genre = db.Column(db.String(100))
    description = db.Column(db.Text())
    release_date = db.Column(db.Date())
    poster_url = db.Column(db.String(300))
    imdb_id = db.Column(db.String(20), unique = True)
    imdb_rating = db.Column(db.Float())
    vote_count = db.Column(db.Integer())
    runtime = db.Column(db.String(20))

    watch_history = db.relationship('WatchHistory',backref = 'movie',lazy = True)

    def serialize(self):
        return { 'id' : self.id,
                'title' : self.title,
                'poster_url' : self.poster_url,
                'imdb_rating' : self.imdb_rating if self.imdb_rating else 'N/A',
        }

    def __repr__(self):
        return f'Movie {self.title}'

class TVShow(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    tmdb_id = db.Column(db.String(100),unique = True )
    title = db.Column(db.String(200),nullable = False)
    genre = db.Column(db.String(100))
    description = db.Column(db.Text())
    release_date = db.Column(db.Date())
    poster_url = db.Column(db.String(300))
    imdb_id = db.Column(db.String(20),unique = True)
    imdb_rating =db.Column(db.Float())
    vote_count = db.Column(db.Integer())
    number_of_seasons = db.Column(db.Integer())
    number_of_episodes = db.Column(db.Integer())

    watch_history = db.relationship('WatchHistory',backref = 'tv_show',lazy = True)

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'poster_url' : self.poster_url,
            'imdb_rating' : self.imdb_rating if self.imdb_rating else 'N/A',
            'vote_count' : self.vote_count
        }



    def __repr__(self):
        return f'TVShow {self.title}'





class WatchHistory(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'),nullable = True)
    tv_show_id = db.Column(db.Integer(),db.ForeignKey('tv_show.id'),nullable = True)
    watched_at = db.Column(db.DateTime,default = datetime.utcnow)
    rating = db.Column(db.Float())


    def __repr__(self):
        return f'WatchHistory {self.user_id}-Movie:{self.movie_id}-TVShow{self.tv_show_id}'
    
    def validate(self):
        if (self.movie_id is None and self.tv_show_id is None) or (self.movie_id is not None and self.tv_show_id is not None):
            raise ValueError("Either movie_id or tv_show_id must be set,but not both")
        
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.validate()    


user_favorite_movies = db.Table('user_favorite_movies',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id'),nullable = False,primary_key = True),
    db.Column('movie_id',db.Integer,db.ForeignKey('movie.id'),nullable = False,primary_key = True)   ) 
 
user_favorite_tv_shows = db.Table('user_favorite_tv_shows',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id'),nullable = False,primary_key = True),
    db.Column('tv_show_id',db.Integer,db.ForeignKey('tv_show.id') ,nullable = False , primary_key = True)                                                            )    


class Recommendation(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'),nullable = True)
    tv_show_id = db.Column(db.Integer,db.ForeignKey('tv_show.id'),nullable = True)
    recomended_at = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return f'Reccomendation {self.user_id} - Movie:{self.movie_id} -TVShow:{self.tv_show_id}'
    
    def validate(self):
        if (self.movie_id is None and self.tv_show_id is None ) or (self.movie_id is not None and self.tv_show_id is not None ):
            raise ValueError('Either movie_id or tv_show_id must be set ,but not both!')
        
    def __init__(self,**kvargs):
        super().__init__(**kvargs)
        self.validate()    
