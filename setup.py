from setuptools import setup, find_packages
from asyncfastrocs import version

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='asyncfastrocs',
    version=version.ASYNCFASTROCS_VERSION,
    author='Ryuichiro Hara',
    author_email='rhara@eyesopen.com',
    description='Asynchronous FastROCS Server Web',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # url='https://github.com/pypa/sampleproject',
    packages=find_packages(),
    package_data = {
        'asyncfastrocs': [
                '*.sql',
                'templates/*.html',
                'static/*.css',
                'static/*.js',
        ],
        'supp': [
            '*.sh',
            '*.tar.gz',
            '*.whl',
        ],
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
