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
    'out3_opt': '/home/rhara/share/data/test-fastrocs/db/out3_opt.oeb',
    'out4_opt': '/home/rhara/share/data/test-fastrocs/db/out4_opt.oeb',
    'out5_opt': '/home/rhara/share/data/test-fastrocs/db/out5_opt.oeb',
    'out6_opt': '/home/rhara/share/data/test-fastrocs/db/out6_opt.oeb',
    'out7_opt': '/home/rhara/share/data/test-fastrocs/db/out7_opt.oeb',
    'out8_opt': '/home/rhara/share/data/test-fastrocs/db/out8_opt.oeb',
    'out9_opt': '/home/rhara/share/data/test-fastrocs/db/out9_opt.oeb',
    'eMolecules': '/home/rhara/share/data/omegadb/eMolecules/eMolecules_2017.2_maxconfs10_opt.oeb',
}
DEFAULT_DB = 'out1_opt'
FASTROCS_HOST = 'harara.com:8080'
ROCS_REPORT = 'rocs_report'
HIT_SIZE = 1000
MAX_PAGES = 51
