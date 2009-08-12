import os, datetime
from fabric.api import *

mthday = datetime.datetime.today().strftime('%m%d')

cassandra_settings = {
    'repo':         'http://svn.apache.org/repos/asf/incubator/cassandra/trunk',
    'srcdir':       '/home/asenchi/src/svn/cassandra',
    'confdir':      '/home/asenchi/src/svn/cassandra/conf',
    'run':          'cassandra',
    'debug':        'cassandra -f',
    'targz':        '/home/asenchi/cassandra-%s.tgz' % (mthday),
}

env.update(cassandra_settings)

def get_java():
    sudo("aptitude -y install openjdk6-jre openjdk6-jre ant")

def setup():
    run('mkdir -p /home/asenchi/src/svn')

def checkout():
    run('cd /home/asenchi/src/svn && svn co %(repo)s cassandra' % env)

def update():
    run('cd %(srcdir)s && svn update' % env)

def test():
    run('cd %(srcdir)s && ant test' % env)

def build():
    run('cd %(srcdir)s && ant' % env)

def mv_conf():
    curdir = os.path.dirname(__file__)
    run('mv -f %(confdir)s/storage-conf.xml{,.orig}' % env)
    run('cp -f %s/storage-conf.xml %(confdir)s' % env)

def package():
    run('cd /home/asenchi/src/svn && tar -zcf %(targz) cassandra' % env)

def copy_package(arg):
    run('scp %(targz)s %s:~/' % (env, arg))

def deflate():
    run('cd /home/asenchi/src/svn && tar -zxf %(targz)s' % env)
