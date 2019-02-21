from flask import Flask, send_from_directory
from werkzeug.utils import secure_filename
from openeye import oechem
import multiprocessing as mp
import os, uuid, time
from asyncfastrocs import state, fastrocs_server, polling, misc

class QServer(Flask):
    """
    Basic configuration of Queuing App
    """

    def __init__(self):
        Flask.__init__(self, __name__)

        self.config.from_mapping(misc.read_config())

        os.makedirs('instance', exist_ok=True)
        self.instance_path = os.path.abspath(self.config['INSTANCE_PATH'])

        st = state.State()
        st.initialize(self.config['DATABASES'])

        name = self.config['DEFAULT_DB']
        st.set_active(name)

        st.update_active_db(count=1)

        self.fastrocs_server_proc = mp.Process(target=fastrocs_server.run, args=(self,))
        self.fastrocs_server_proc.start()

        self.polling_proc = mp.Process(target=polling.poll, args=(self,))
        self.polling_proc.start()

    def changedb(self, dbname):
        st = state.State()

        if 0 < st.get_queue_count():
            return

        active_db = st.get_active()
        count = active_db['count']
        pid = active_db['pid']
        st.set_active(dbname)
        st.update_active_db(count=count+1)

        if 0 < pid:
            print('[LOG] killing', pid, flush=True)
            kill = misc.run_proc(f'kill -9 {pid}')
            kill.wait()
            time.sleep(2) # for safety releasing network port etc.

        self.fastrocs_server_proc = mp.Process(target=fastrocs_server.run, args=(self,))
        self.fastrocs_server_proc.start()

    def upload(self, file, hitsize, remote_addr):
        oid = uuid.uuid4().hex
        filename = secure_filename(file.filename)
        ext = oechem.OEGetFileExtension(filename)
        os.makedirs(f'instance/{oid}', exist_ok=True)
        opath = f'instance/{oid}/query.{ext}'

        file.save(opath)

        if ext != 'sq' and not misc.check_mol(opath):
            os.unlink(opath)
            return

        st = state.State()
        print('hitsize:', hitsize) #@@
        st.repo_new(oid, filename, hitsize, remote_addr)

    def download(self, klass, oid):
        st = state.State()
        r = st.get_one(oid)
        ext = r['ext']
        basename = r['basename']
        if klass == 'query':
            iname = f'{oid}/query.{ext}'
            oname = f'{basename}.{ext}'
        elif klass == 'result':
            iname = f'{oid}/hitlist.sdf'
            oname = f'{basename}_hitlist.sdf'
        else:
            iname = f'{oid}/report.pdf'
            oname = f'{basename}_report.pdf'
        if klass == 'query':
            return send_from_directory(self.instance_path, iname, as_attachment=True, \
                                       attachment_filename=oname)
        elif klass == 'result':
            return send_from_directory(self.instance_path, iname, as_attachment=True, \
                                       attachment_filename=oname)
        else:
            return send_from_directory(self.instance_path, iname, attachment_filename=oname)
