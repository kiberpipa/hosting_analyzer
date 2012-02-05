import os
import pprint

from fabric.api import run, sudo, task, get , local, env

from status import Checker

env.hosts = ["dogbert.kiberpipa.org"]

env.store = {"nginx": "/tmp/nginx/", "apache": "/tmp/apache/"}
env.conf_dir = {
    "nginx": "/etc/nginx/sites-enabled/*",
    "apache": "/etc/apache2/sites-enabled/*"
}

def list_dir(dir_=None, local_=False):
    """docstring for list_dir"""
    dir_ = dir_ or env.cwd
    if local_:
        command_ = local
    else:
        command_ = sudo
    string_ = command_("for i in %s*; do echo $i; done" % dir_)
    files = string_.replace("\r","").split("\n")
    return files

def get_nginx_confs(dir_=None):
    """docstring for get_nginx_confs"""
    dir_ = dir_ or env.conf_dir["nginx"]
    store = env.store["nginx"]
    local("mkdir -p %s " % store)
    get(dir_, store)

def parse_nginx_conf(nginx_conf):
    """

    """
    domains = []
    with open(nginx_conf) as conf:
        for line in conf:
            if "server_name " in line and "#" not in line:
                d = line.strip().replace("server_name ", "").replace(";", "").split()
                domains.extend(d)
    return domains

def get_apache_confs(dir_=None):
    """docstring for get_apache_confs"""
    dir_ = dir_ or env.conf_dir["apache"]
    store = env.store["apache"]
    local("mkdir -p %s " % store)
    get(dir_, store)

def parse_apache_conf(apache_conf):
    """
    """
    domains = []
    with open(apache_conf) as conf:
        for line in conf:
            if "ServerAlias" in line and  "#" not in line:
                d= line.strip().replace("ServerAlias", "").split()
                domains.extend(d)
    return domains

@task
def get_confs():
    """Get configuration files (nginx and apache) from server"""


    get_nginx_confs()
    get_apache_confs()

@task
def check_domains():
    """Parses the configuration files and checks if the domains are up """
    domains = {"nginx": [], "apache": []}

    ok = []
    foo = []

    responses = []

    c = Checker()
    for conf in os.listdir(env.store["nginx"]):
        conf = os.path.join(env.store["nginx"], conf)
        domains["nginx"].extend(parse_nginx_conf(conf))
    for conf in os.listdir(env.store["apache"]):
        conf = os.path.join(env.store["apache"], conf)
        domains["apache"].extend(parse_apache_conf(conf))

    for url in domains["nginx"]:
        c.url = url
        r = c.check_url()
        responses.append(r)

        if r[0]:
            ok.append(r[0][0])
        else:
            foo.append(r[1])
            print "Domain is fubar:"
            print r

    for url in domains["apache"]:
        c.url = url
        r = c.check_url()
        responses.append(r)

        if r[0]:
            ok.append(r[0][0])
        else:
            foo.append(r[1])
            print "Domain is fubar:"
            print r

    print "These domains are OK (200)"
    print ok

    print "These domains are F00"
    print foo
