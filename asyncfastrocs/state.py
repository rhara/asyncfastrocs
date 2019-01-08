from openeye import oechem
from asyncfastrocs import misc
import time, sqlite3, hashlib

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class State:
    def connect(self):
        conn = sqlite3.connect(self.state_db)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.row_factory = dict_factory
        return conn

    def __init__(self):
        self.state_db = misc.read_config()['STATE_DB']

    def initialize(self, dbdict):
        self('DELETE FROM db', commit=True)
        for name, path in dbdict.items():
            db = oechem.OEMolDatabase(path)
            nmols = db.NumMols()
            self('INSERT INTO db (name, path, molcount) VALUES (?,?,?)', (name, path, nmols),
                 commit=True)

    def __call__(self, *argv, commit=False, **kwargs):
        conn = self.connect()
        c =  conn.cursor()
        ret = c.execute(*argv, **kwargs)
        if commit:
            conn.commit()
        else:
            return ret

    def reset(self):
        self('DELETE FROM active_db', commit=True)

    def set_active(self, name):
        self.reset()
        self('INSERT INTO active_db (name) VALUES (?)', (name,), commit=True)

    def update_db(self, name, **kwargs):
        for k, v in kwargs.items():
            self(f'UPDATE db SET {k}=? WHERE name=?', (v, name), commit=True)

    def update_active_db(self, **kwargs):
        for k, v in kwargs.items():
            self(f'UPDATE active_db SET {k}=?', (v,), commit=True)

    def get_active(self):
        return self('SELECT * FROM active_db NATURAL JOIN db').fetchone()

    def get_one(self, oid):
        return self('SELECT * FROM repo WHERE oid=?', (oid,)).fetchone()

    def get_queue(self):
        for r in self('SELECT * FROM repo WHERE status < 2'):
            yield r

    def get_queue_count(self):
        count = 0
        for r in self.get_queue():
            count += 1
        return count

    def repo_new(self, oid, filename, remote_addr):
        ext = oechem.OEGetFileExtension(filename)
        basename = filename[:-len(ext)-1]
        reportable = 0 if ext == 'sq' else 1
        timestamp1 = time.time()

        self('INSERT into repo (oid, basename, ext, reportable, timestamp1, ip) '
             'VALUES (?,?,?,?,?,?)', \
             (oid, basename, ext, reportable, timestamp1, remote_addr),
             commit=True)

    def update_repo(self, oid, **kwargs):
        for k, v in kwargs.items():
            self(f'UPDATE repo SET {k}=? WHERE oid=?', (v, oid), commit=True)

    def get_list(self, since):
        for r in self(f'SELECT * from repo WHERE timestamp1 > {since} ORDER BY timestamp1 DESC'):
            yield r

    def get_footprint(self, since):
        s = ''
        for r in self.get_list(since):
            s += str(r)
        s += '+'
        s += str(self('SELECT * FROM active_db').fetchone())
        return hashlib.sha256(s.encode()).hexdigest()
