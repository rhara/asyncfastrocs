SECRET_KEY = 'chugai'
INSTANCE_PATH = 'instance'
STATE_DB = 'instance/qserver.db'
MAX_DAYS = 8
POLLING_INTERVAL = 3
ALLOWED_EXTENSIONS = [
    'sdf',
    'sdf.gz',
    'mol',
    'mol.gz',
    'mol2',
    'mol2.gz',
    'pdb',
    'pdb.gz',
    'oeb',
    'oeb.gz',
    'sq',
]
DATABASES = {
    'out1_opt': '/home/rhara/share/data/test-fastrocs/db/out1_opt.oeb',
    'out2_opt': '/home/rhara/share/data/test-fastrocs/db/out2_opt.oeb',
    'eMolecules': '/home/rhara/share/data/omegadb/eMolecules/eMolecules_2017.2_maxconfs10_opt.oeb',
}
DEFAULT_DB = 'out1_opt'
FASTROCS_HOST = 'fastrocs.server:8080'
ROCS_REPORT = 'rocs_report'
