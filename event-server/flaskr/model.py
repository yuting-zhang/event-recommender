from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db, get_rec
from flaskr.recommender import recommender

'''
List of all interests and the corresponding names in db and dict
'''
bp = Blueprint('model', __name__)
column_names = ['Artifical Intelligence', 'Machine Learning', 'Big Data', 'Algorithms', \
        'Augmented/Virtual Reality', 'Graphics', 'Biology', 'Linguistics', 'Statistics', 'Mathematics', 'Economics']
stemmed_names = [['artifici','intellig'], ['machin'], ['big','data'], ['algorithm'], \
        ['virtual','realiti'], ['graphic','numeric','imag'], ['biolog','biologist','biologes'], \
        ['linguist','linguistician','languag'], ['statist'], ['math','mathemat','mathematic'], ['economi','economist']]
db_names = ['ai', 'ml', 'big_data', 'algos', 'ar_vr', 'graphics', 'bio', 'linguistics', 'stats', 'math', 'econ']
joined_db_names = ', '.join(db_names)

'''
Main page user sees
'''
@bp.route('/', methods=('GET', 'POST'))
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
            # get user feedback and update accordingly
            lst_rel = []
            lst_non_rel = []
            for radio_option in request.form:
                if len(radio_option) > 9 and radio_option[:9] == 'feedback_':
                    idx = int(radio_option[9:])
                    if request.form[radio_option][0] == 'y':
                        lst_rel.append(idx)
                    else:
                        lst_non_rel.append(idx)
            rec.update_profile_vector(str(user_id), lst_rel, lst_non_rel)
            print("updating for", user_id)
            # hack to fix key errors
            if rec.get_events(str(user_id)) is None:
                rec.add_new_user(str(user_id))
            # set user interests
            for i in range(len(column_names)):
                if choices[i] == 1:
                    for stemmed_words in stemmed_names[i]:
                        rec.user_data[str(user_id)][stemmed_words] = 10.0
                else:
                    for stemmed_words in stemmed_names[i]:
                        rec.user_data[str(user_id)][stemmed_words] = 0.0
            # get events
            events = rec.get_events(str(user_id))
            rec.save_user_data()

    return render_template('model/index.html', events=events)

'''
Page to handle interests
'''
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

'''
Method to handle POST request from interests and update the events
'''
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

