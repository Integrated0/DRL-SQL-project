from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS     # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """  
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200) 

  
def get_actor_by_id():
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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'name' in data.keys():
        if 'date_of_birth' in data.keys():
            if 'gender' in data.keys():
                try:
                    data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
                except:
                    err = 'Wrong data format'
                    return make_response(jsonify(error=err), 400)
                if data['gender'].isalpha():
                    try:
                        new_record = Actor.create(**data)
                        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
                    except:
                        err = 'Record with such id does not exist'
                        return make_response(jsonify(error=err), 400)
                    return make_response(jsonify(new_actor), 200)
                else:
                    err = 'Wrong gender format'
                    return make_response(jsonify(error=err), 400)
            else:
                err = 'No gender specified'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No date_of_birth specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No name specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###

def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    for key in data.keys():
        if key not in ACTOR_FIELDS:
            err = 'Wrong keys'
            return make_response(jsonify(error=err), 400)
    #data = dict(data)
    try:
        id = int(data.pop('id'))
    except:
        err = 'Wrong id format'
        return make_response(jsonify(error=err), 400)
    if data.get('date_of_birth'):
        try:
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
        except:
            err = 'Wrong date format'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
    upd_record =  Actor.update(id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)

def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 
        obj = Actor.delete(row_id)
        if obj ==1:
            # use this for 200 response code
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
        else:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    if 'id' in data.keys():
        if 'relation_id' in data.keys():
            try:
                actor_id = int(data['id'])
            except:
                err = "actor_id must be an integer"
                return make_response(jsonify(error=err), 400)
            try:
                row_m_id = int(data['relation_id'])
            except:
                err = "movie_id must be integer"
                return make_response(jsonify(error=err), 400)
            movie = Movie.query.filter_by(id=row_m_id).first()
            actor = Actor.add_relation(actor_id, movie)
            try:
                rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        else:
            err = 'No relation_id specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 
        try:
            actor = Actor.clear_relations(row_id)    # clear relations here
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 
        # use this for 200 response code
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 
    ### END CODE HERE ###