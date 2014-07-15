import os
from fabric.api import task, local
from code import db
from config import config


@task
def setup():
    '''Recreates database schema'''
    database = config.database['dbn']
    schema_commands = open(database + '.sql', 'r').read().split(';')
    for cmd in schema_commands:
        if cmd.strip():
            db.query(cmd)


@task
def server(port='8081'):
    '''Runs server on specified port'''
    port = os.environ.get('PORT', port)
    local('python code.py %s' % port)


@task
def test():
    '''Runs tests'''
    local('nosetests')


@task
def lint():
    '''Runs flakes8 lint'''
    local('flake8 . --exclude venv')


@task
def clean():
    '''Removes all .pyc files'''
    local('find . -name "*.pyc" -exec rm -rf {} \;')
