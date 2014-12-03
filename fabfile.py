from fabric.operations import local, os

__author__ = 'yarg'


def _env(env, *args):
    if os.name == 'posix':
        local("/bin/bash -l -c 'source %s/bin/activate && %s'" % (env, ' && '.join(args)))


def db_create(env="venv"):
    _env(env,
         "python manage.py syncdb")


def db_migration_initial(env="venv", app="backend"):
    _env(env,
         "python manage.py schemamigration %s --initial" % app)


def db_migration_create(env="venv", app="backend"):
    _env(env,
         "python manage.py schemamigration %s --auto" % app)


def db_migrate(env="venv", app="", deleteGhost=False, fake=False):
    params = [app]
    if deleteGhost:
        params += ['--delete-ghost-migrations']
    if fake:
        params += ['--fake']

    _env(env,
         "python manage.py migrate %s" % ' '.join(params))


def env_create(env="venv", less=True):
    local("virtualenv --no-site-packages %s" % env)
    _env(env,
         "source %s/bin/activate" % env,
         "pip install -r requirements.txt")
    if less:
        _env(env,
             "nodeenv -p")
        _env(env,
             "npm install -g less")


def env_dump(env="venv"):
    _env(env,
         "pip freeze > requirements.txt")


def locale_make(env="venv", ignore=None):
    if ignore:
        ignore = ignore.split(',')
    else:
        ignore = []
    ignore += [env]
    ignoreStr = ''.join([" --ignore=%s" % i for i in ignore])

    _env(env,
         "python manage.py makemessages --all%s" % ignoreStr)


def locale_compile(env="venv"):
    _env(env,
         "python manage.py compilemessages")
