import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from auth import load_logged_in_user as check
from auth import login_required
from db import get_db

bp = Blueprint('messages', __name__, url_prefix='/messages')

def _send_message(message, sender, receiver):
    check()
    db = get_db()
    error = None
    q = "INSERT INTO messages (dt, message, sender, recipient) VALUES (datetime('now'),?,?,?)"
    db.execute(q, (message, sender, receiver))

    db.commit()
    return error

def _get_message_threads(username=None):
    """Return a list of message objects (as dicts)"""
    if (request.method == 'GET') or (request.method == 'POST'):
        check()
        db = get_db()
        error = None

        if username:
            username = str(username)  # Ensure that we have a valid id value to query
            q = "SELECT DISTINCT {} FROM messages WHERE {}=? ORDER BY dt DESC"
            rows = list(db.execute(q.format('recipient', 'sender'), (username,)))
            other_rows = list(db.execute(q.format('sender', 'recipient'), (username,)))
            rows += other_rows
            result = set(row[0:] for row in rows)
            results = {}
            for r in result:
                results[r] = results.get(r, 0) + 1
        
        else:
            q = "SELECT * FROM messages ORDER BY dt DESC"
            rows = db.execute(q)

        return [{'conversation': key[0]} for key, count in results.items()]

def _get_messages(username=None, recipient=None):
    """Return a list of message objects (as dicts)"""
    check()
    db = get_db()
    error = None
    if username and recipient:
        username = str(username)
        recipient = str(recipient)  
        q = "SELECT * FROM messages WHERE {}=? AND {}=? ORDER BY dt ASC"
        rows = list(db.execute(q.format('sender', 'recipient'), (username, recipient)))
        rows += list(db.execute(q.format('recipient', 'sender'), (username, recipient)))
        def myFunc(e):
            return e['dt']
        print(rows)
        rows.sort(key=myFunc)

    else:
        q = "SELECT * FROM messages ORDER BY dt ASC"
        rows = db.execute(q)

    return [{'id': r[0], 'dt': r[1], 'message': r[2], 'sender': r[3], 'recipient': r[4]} for r in rows]

@bp.route('/')
@bp.route('/home')
@bp.route('/index', methods=('GET', 'POST'))
@login_required
def home():
    if request.method == 'POST':
        session['recipient']=request.form['recipient']
        return redirect(url_for('messages.thread', thread_identifier=request.form['recipient']))

    return render_template('messages/index.html', messages=_get_message_threads(username=session.get('username')))

@bp.route('/thread/<thread_identifier>', methods=('GET', 'POST'))
@login_required
def thread(thread_identifier):
    sender = session.get('username')
    receiver = thread_identifier
    if request.method == 'POST':
        id = _send_message(request.form['message'], sender=sender, receiver=receiver)
        session.pop('message', None)
        return redirect(url_for('messages.thread', thread_identifier=thread_identifier))
        
    return render_template('messages/thread.html', thread=thread, messages=_get_messages(sender, receiver))

"""
@app.route('/items/<item_identifier>')
def show_item_info(item_identifier):
    print item_identfier
    # query the db for item and assign it item 
    # pass the item to template
    return render_template('item.html',item=item)
"""