from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db, get_rec
from flaskr.recommender import recommender

bp = Blueprint('model', __name__)
column_names = ['Artifical Intelligence', 'Machine Learning', 'Big Data', 'Algorithms', 'Augmented/Virtual Reality', 'Cloud Computing', 'Graphics', 'Medicine', 'Biology', 'Chemistry', 'Linguistics', 'Statistics', 'Mathematics', 'Economics']
stemmed_names = ['artific', 'learn', 'data', 'algorithm', 'realiti', 'cloud', 'graphic', 'medicin', 'biolog', 'chemistri', 'linguist', 'statist', 'math', 'economi']
db_names = ['ai', 'ml', 'big_data', 'algos', 'ar_vr', 'cloud', 'graphics', 'meds', 'bio', 'chem', 'linguistics', 'stats', 'math', 'econ']
joined_db_names = ', '.join(map(str, db_names))

@bp.route('/')
def index():
    user_id = session.get('user_id')
    events = {}
    if user_id is not None:
        db = get_db()
        rec = get_rec()
        query_string = 'SELECT '+joined_db_names+' FROM checkboxes c, user u WHERE c.id = u.id AND u.id='+str(user_id)
        print(query_string)
        choices = db.execute(query_string).fetchone() 
        if choices is not None:
            print("updating for", user_id)
            for i in range(len(column_names)):
                if choices[i] == 1:
                    rec.user_data[str(user_id)][stemmed_names[i]] = 10.0
                else:
                    rec.user_data[str(user_id)][stemmed_names[i]] = 0.0
            events = rec.get_events(str(user_id))
            rec.save_user_data()

    return render_template('model/index.html', events=events)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    user_id = session.get('user_id')
    db = get_db()
    query_string = 'SELECT '+joined_db_names+' FROM checkboxes c, user u WHERE c.id = u.id AND u.id='+str(user_id)
    options = db.execute(query_string).fetchone() 
    if options is None:
        zero_string = ', '.join(['0' for i in range(len(db_names))])
        insert_string = 'INSERT INTO checkboxes (id, '+joined_db_names+') VALUES ('+str(user_id)+', '+zero_string+')'
        print(insert_string)
        db.execute(insert_string)
        db.commit()
        options = db.execute(query_string).fetchone() 
    values = zip(column_names, list(options))
    return render_template('model/interests.html', checkboxes=values)

@bp.route("/options", methods=['POST'])
def getinfo():
    if request.method == 'POST':
        test = request.form.getlist('checks')
        user_id = session.get('user_id')
        arr = [0 for i in range(len(column_names))]
        for yes in test:
            arr[column_names.index(yes)] = 1
        insert_string = 'INSERT INTO checkboxes (id, '+joined_db_names+') VALUES ('+str(user_id)
        for val in arr:
            insert_string += ', '+str(val)
        insert_string += ')'
        db = get_db()
        if db.execute('SELECT * FROM checkboxes WHERE id='+str(user_id)) is not None:
            db.execute('DELETE FROM checkboxes WHERE id='+str(user_id))
        db.execute(insert_string)
        db.commit()
        return redirect('/')
    else:
        return redirect('/')

def get_events(id, check_author=True):
    events = {}
    return events
