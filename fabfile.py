from fabric.api import *

env.project_name = 'lpad'
env.key_filename = '/home/bibhas/.ssh/ec2bi.pem'

env.dbname = 'lpad'

def webserver():
    "Use the actual webserver"
    env.hosts = ['23.21.195.1']
    env.user = 'ubuntu'
    env.path = '/home/%(user)s/sites' % env
    env.site_path = '/home/%(user)s/sites/%(project_name)s' % env
    env.virtualhost_path = env.path

def test():
    run('uname -a')
    sudo('tail -f /home/ubuntu/.pythonbrew/log/build.log')
    

def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    # sudo('apt-get install postfix')
    # sudo('mkdir -p %(path)s; chown %(user)s:%(user)s %(path)s;' % env, pty=True)
    with cd(env.site_path):
        # run('virtualenv %(project_name)s --no-site-packages' % env, pty=True)
        run('mkdir -p releases/previous; mkdir packages;' % env, pty=True)
        
def deploy():
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    upload_tar_from_git()
    install_requirements()
    install_site()
    restart_webserver()
    
def upload_tar_from_git():
    require('release', provided_by=[deploy])
    local('git archive --format=tar master | gzip > %(release)s.tar.gz' % env)
    put('%(release)s.tar.gz' % env, '%(site_path)s/packages/' % env)
    with cd(env.site_path):
        run('cd %(project_name)s && cp -ru * ../releases/previous/' % env, pty=True)
        run('cd %(project_name)s && rm -rf *' % env, pty=True)
        run('cd %(project_name)s && cp ../releases/previous/local_settings.py ./' % env, pty=True)
        run('cd %(project_name)s && tar zxf ../packages/%(release)s.tar.gz' % env, pty=True)
    local('rm %(release)s.tar.gz' % env)    

def install_site():
    "Add the virtualhost file to apache"
    # require('release', provided_by=[deploy])
    with cd(env.site_path):
        sudo('cp %(project_name)s/%(project_name)s /etc/apache2/sites-available/%(project_name)s' % env)
    sudo('cd /etc/apache2/sites-available/; a2ensite %(project_name)s' % env, pty=True) 
    
def install_requirements():
    with cd(env.site_path):
        with prefix('source bin/activate'):
            sudo('pip install -r %(project_name)s/requirements/project.txt' % env)
    
def db_setup():
    with cd(env.site_path):
        put('%(project_name)s.sql' % env, '%(project_name)s/')
        
def restart_webserver():
    # "Restart the web server"
    sudo('/etc/init.d/apache2 reload', pty=True)
    sudo('/etc/init.d/apache2 restart', pty=True)
