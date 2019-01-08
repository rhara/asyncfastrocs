from flask import request, render_template, redirect
from flask_socketio import SocketIO
from asyncfastrocs import qserver, misc, state, messaging, version
from threading import Lock
from werkzeug.contrib.fixers import ProxyFix
import os, time

print(f'AsyncFastROCS Server Web ver.{version.ASYNCFASTROCS_VERSION}')
print(f'({version.ASYNCFASTROCS_DATE})')

async_mode = None
app = qserver.QServer()
app.wsgi_app = ProxyFix(app.wsgi_app)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

os.environ['PYTHONUNBUFFERED'] = '1'

def background_thread():
    st = state.State()
    since = time.time() - app.config['MAX_DAYS']*60*60*24

    fp_old = ''

    while True:
        fp = st.get_footprint(since)

        if fp != fp_old:
            print(f'[LOG] list updated {fp}', flush=True)
            table = messaging.make_table(app.config)
            db_status = messaging.make_dbnote()

            args = dict(table=table, db_status=db_status)
            socketio.emit('listings_changed', args, broadcast=True, namespace='/listings')
        else:
            socketio.sleep(app.config['POLLING_INTERVAL'])

        fp_old = fp


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    class NoFileException(Exception): pass

    if request.method == 'POST':
        try:
            file = request.files['file']
            if file.filename == '':
                raise NoFileException()
        except:
            return redirect('/')
        if file and misc.is_allowed_file(file.filename):
            # remote_addr = request.access_route[0]
            remote_addr = request.environ['werkzeug.proxy_fix.orig_remote_addr']
            app.upload(file, remote_addr)
            return redirect('/')
    else:
        table = messaging.make_table(app.config)
        db_status = messaging.make_dbnote()
        return render_template('index.html', table=table, db_status=db_status,
                               version=version.ASYNCFASTROCS_VERSION,
                               date=version.ASYNCFASTROCS_DATE)

@app.route('/download/<klass>/<oid>')
def download(klass, oid):
    return app.download(klass, oid)

@app.route('/changedb_page')
def changedb_page():
    dbs = [dict(name=name, path=path) for name, path in misc.read_databases().items()]
    for d in dbs:
        d['molcount'] = misc.get_molcount(d['path'])
    return render_template('changedb.html', dbs=dbs)

@app.route('/changedb/<dbname>')
def changedb(dbname):
    app.changedb(dbname)
    return redirect('/')

@socketio.on('connect', namespace='/listings')
def listings_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
