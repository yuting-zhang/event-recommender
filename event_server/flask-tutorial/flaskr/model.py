from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('model', __name__)

@bp.route('/')
def index():
    posts = {}
    return render_template('model/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    user_id = session.get('user_id')
    db = get_db()
    column_names = db.execute('PRAGMA table_info(checkboxes)').fetchone()
    print column_names
    options = db.execute(
        'SELECT ai_ml, big_data FROM checkboxes c JOIN user u ON c.id = u.id WHERE u.id='+str(user_id)
    ).fetchone()
    if len(options) == 0:
        print "Need to create new"
        db.execute(
            'INSERT INTO checkboxes (id, ai_ml, big_data) VALUES (?, ?, ?)',
            (user_id, 0, 0)
        )
        db.commit()
        options = db.execute(
            'SELECT ai_ml, big_data FROM checkboxes c JOIN user u ON c.id = u.id WHERE u.id='+str(user_id)
        ).fetchall()
    print options
    return render_template('model/interests.html', checkboxes=list(options))

@bp.route("/options", methods=['POST'])
def getinfo():
    if request.method == 'POST':
        test = request.form.getlist('checks')
        print test # debug
        return redirect('/')
    else:
        return redirect('/')

def get_events(id, check_author=True):
    events = {}
    return events
