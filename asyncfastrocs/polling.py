import time
from asyncfastrocs import misc, state

def poll(app):
    d = misc.read_config()

    while True:
        st = state.State()
        for r in st.get_queue():
            # wait for active db to be ready
            while True:
                active_db = st.get_active()
                if active_db['ready'] == 1:
                    break
                time.sleep(d['POLLING_INTERVAL'])

            dbname = active_db['name']
            oid = r['oid']
            ext = r['ext']

            st.update_repo(oid, status=1, dbname=dbname)

            client = d['FASTROCS_CLIENT']
            host = d['FASTROCS_HOST']
            hit_size = d['HIT_SIZE']
            query = f'instance/{oid}/query.{ext}'
            hitlist = f'instance/{oid}/hitlist.sdf'
            command = f'{client} {host} {query} {hitlist} {hit_size}'
            print(f'[LOG:COMMAND] {command}', flush=True)

            proc = misc.run_proc(command)
            for line in misc.read_output(proc):
                print(line, flush=True)
            proc.wait()

            if r['reportable']:
                 # Correct SDF for ROCS_REPORT
                 misc.fix_sdf(hitlist)

                 rocs_report = d['ROCS_REPORT']
                 max_pages = d['MAX_PAGES']
                 report_pdf = f'instance/{oid}/report.pdf'
                 command = f"{rocs_report} -in {hitlist} -refmol {query} -out {report_pdf} " \
                           f"-maxpages {max_pages}"
                 print(f'[LOG:COMMAND] {command}', flush=True)

                 proc = misc.run_proc(command)
                 for line in misc.read_output(proc):
                     print(line, flush=True)
                 proc.wait()

            timestamp2 = time.time()

            st.update_repo(oid, timestamp2=timestamp2, status=2)
        time.sleep(d['POLLING_INTERVAL'])
