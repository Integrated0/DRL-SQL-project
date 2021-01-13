from flask import jsonify, make_response

from ast import literal_eval

from models.movie import Movie
from models.actor import Actor
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200) 


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 
    

def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    if 'name' in data.keys():
        if 'year' in data.keys():
            if 'genre' in data.keys():
                try:
                    if data['year'].isdigit() and len(data['year']) == 4 and data['genre'].isalpha():
                        new_record = Movie.create(**data)
                        try:
                            new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
                        except:
                            err = 'Record with such id does not exist'
                            return make_response(jsonify(error=err), 400)
                        return make_response(jsonify(new_movie), 200)
                    else:
                        return make_response(jsonify(error='ERROR'), 400)
                except:
                    return make_response(jsonify(error='ERROR'), 400)
            else:
                err = 'No genre specified'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No year specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No name specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    for key in data.keys():
        if key not in MOVIE_FIELDS:
            err = 'Wrong keys'
            return make_response(jsonify(error=err), 400)
    data = dict(data)
    try:
        id = int(data.pop('id'))
    except:
        err = 'Wrong id format'
        return make_response(jsonify(error=err), 400)
    if data.get('year'):
        try:
            data['year']=int(data['year'])
        except:
            err = 'Wrong year format'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
    upd_record =  Movie.update(id, **data)
    upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(upd_movie), 200)   


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 
        obj = Movie.delete(row_id)
        if obj == 1:
            # use this for 200 response code
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)    
        else:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 
    

def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    if 'id' in data.keys():
        if 'relation_id' in data.keys():
            try:
                movie_id = int(data['id'])
            except:
                err = "movie_id must be an integer"
                return make_response(jsonify(error=err), 400)
            try:
                row_a_id = int(data['relation_id'])
            except:
                err = "actor_id must be integer"
                return make_response(jsonify(error=err), 400)
            actor = Actor.query.filter_by(id=row_a_id).first()
            movie = Movie.add_relation(movie_id, actor)
            try:
                rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)
            # use this for 200 response code
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)
        else:
            err = 'No relation_id specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 
        try:
            movie = Movie.clear_relations(row_id)    # clear relations here
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 
        # use this for 200 response code
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 