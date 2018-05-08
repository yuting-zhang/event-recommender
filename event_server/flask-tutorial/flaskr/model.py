from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.recommender import recommender

bp = Blueprint('model', __name__)
column_names = ['AI/ML', 'Big Data']

@bp.route('/')
def index():
    user_id = session.get('user_id')
    events = {}
    if user_id is not None:
        db = get_db()
        choices = db.execute(
            'SELECT ai_ml, big_data FROM checkboxes c, user u WHERE c.id = u.id AND u.id='+str(user_id)
        ).fetchone() 
        if choices is not None:
        	print "updating for ", user_id
        	for i in range(len(column_names)):
        		if choices[i] == 1:
        			g.recommender.user_data[str(user_id)][column_names[i]] = 10.0
        		else:
        			g.recommender.user_data[str(user_id)][column_names[i]] = 0.0
        	events = g.recommender.get_events(str(user_id))

    return render_template('model/index.html', events=events)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    user_id = session.get('user_id')
    db = get_db()
    print column_names # debug
    options = db.execute(
        'SELECT ai_ml, big_data FROM checkboxes c, user u WHERE c.id = u.id AND u.id='+str(user_id)
    ).fetchone() 
    if options is None:
        print "Need to create new" # debug
        db.execute(
            'INSERT INTO checkboxes (id, ai_ml, big_data) VALUES (?, ?, ?)',
            (user_id, 0, 0)
        )
        db.commit()
        options = db.execute(
            'SELECT ai_ml, big_data FROM checkboxes c JOIN user u ON c.id = u.id WHERE u.id='+str(user_id)
        ).fetchone()
    print options # debug
    values = zip(column_names, list(options))
    print values # debug
    return render_template('model/interests.html', checkboxes=values)

@bp.route("/options", methods=['POST'])
def getinfo():
    if request.method == 'POST':
        test = request.form.getlist('checks')
        print test # debug
        user_id = session.get('user_id')
        arr = [0 for i in range(len(column_names))]
        for yes in test:
            arr[column_names.index(yes)] = 1
        insert_string = 'INSERT INTO checkboxes (id, ai_ml, big_data) VALUES ('+str(user_id)
        for val in arr:
            insert_string += ', '+str(val)
        insert_string += ')'
        print insert_string # debug
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
