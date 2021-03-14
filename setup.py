from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ddd-for-python',
    version='0.9.1',
    author='David Runemalm, 2021',
    author_email='david.runemalm@gmail.com',
    description=
    'A domain-driven design (DDD) framework for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/runemalm/ddd-for-python',
    project_urls={
        "Bug Tracker": "https://github.com/runemalm/ddd-for-python/issues",
    },
    package_dir={'': '.'},
    packages=find_packages(
        where='.',
        include=['ddd*',],
        exclude=[]
    ),
    license='GNU General Public License v3.0',
    install_requires=[
        'addict>=2.3.0',
        'aiokafka>=0.7.0',
        'APScheduler>=3.6.3',
        'arrow>=0.16.0',
        'asyncpg>=0.21.0',
        'azure-eventhub>=5.2.0',
        'azure-eventhub-checkpointstoreblob-aio>=1.1.1',
        'CMRESHandler>=1.0.0',
        'python-dotenv>=0.14.0',
        'slacker-log-handler>=1.7.1',
        'SQLAlchemy>=1.3.20',
        'uvloop>=0.14.0',
    ],
    tests_require=[
        'aiosonic>=0.7.2',
    ],
    python_requires='>=3.8.5',
)
