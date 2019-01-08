from asyncfastrocs import misc, state

def run(app):
    FASTROCS_SERVER = misc.read_config()['FASTROCS_SERVER']

    st = state.State()

    active_db = st.get_active()
    name = active_db['name']
    path = active_db['path']
    command = f'{FASTROCS_SERVER} {path}'
    print(f'[LOG:COMMAND] {command}', flush=True)
    proc = misc.run_proc(command)

    st.update_active_db(pid=proc.pid)

    for line in misc.read_output(proc):
        print(line, flush=True)
        if line.startswith('Total:') and line.endswith('conformers processed.'):
            confcount = int(line.split()[1])
            st.update_db(name, confcount=confcount)
        if line.endswith('seconds to load database'):
            loadtime = float(line.split()[0])
            st.update_active_db(loadtime=loadtime, ready=1)
