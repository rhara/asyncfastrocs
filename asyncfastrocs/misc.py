from openeye import oechem
import time, os, re, shlex, json
import subprocess as sp

def read_config():
    d = {}
    _dir, name = os.path.split(__file__)
    for loc in ['.', './asyncfastrocs', _dir]:
        fname = f'{loc}/config.py'
        if os.path.exists(fname):
            break
    exec(open(fname, 'rt').read(), None, d)
    d['FASTROCS_SERVER'] = f'python -u {_dir}/ShapeDatabaseServer.py'
    d['FASTROCS_CLIENT'] = f'python -u {_dir}/ShapeDatabaseClient.py'
    return d

def run_proc(command, stdout=True, stderr=True):
    cmds = shlex.split(command)
    _out = sp.PIPE if stdout else sp.DEVNULL
    _err = sp.STDOUT if stderr else sp.DEVNULL
    proc = sp.Popen(cmds, stdout=_out, stderr=_err, universal_newlines=True)
    return proc

def read_output(proc):
    for line in iter(proc.stdout.readline, ''):
        line = line.rstrip()
        yield line

def read_databases():
    d = read_config()
    return d['DATABASES']

def get_molcount(path):
    db = oechem.OEMolDatabase(path)
    return db.NumMols()

def check_mol(path):
    mol = oechem.OEGraphMol()
    ifs = oechem.oemolistream(path)
    oechem.OEReadMolecule(ifs, mol)
    ifs.close()
    mw = oechem.OECalculateMolecularWeight(mol)
    if mw <= 100 or 1500 <= mw:
        return False
    return True

def is_allowed_file(name):
    d = read_config()
    return oechem.OEGetFileExtension(name) in d['ALLOWED_EXTENSIONS']

def iso_time(unixtime, millisec=False):
    s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unixtime))
    if millisec:
        msec = int((unixtime - int(unixtime))*1000)
        return f'{s}.{msec:03d}'
    else:
        return s

def fix_sdf(fname):
    lines = open(fname, 'rt').readlines()

    fout = open(fname, 'wt')
    for line in lines:
        line = line.rstrip()
        if line == '> <ShapeTanimoto>':
            line = '> <ROCS_ShapeTanimoto>'
        elif line == '> <ColorTanimoto>':
            line = '> <ROCS_ColorTanimoto>'
        elif line == '> <TanimotoCombo>':
            line = '> <ROCS_TanimotoCombo>'
        fout.write(line + '\n')
    fout.close()
