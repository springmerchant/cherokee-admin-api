"""
This file is dynamically generated by cherokee and I should find a
better way to access this info.
"""

from os.path import (dirname,
                     join)

STEP_SOURCE = 1
STEP_RULE   = 10
STEP_VSERVER   = 100

BASEDIR = dirname(__file__)
configuration_dirs  = (join(BASEDIR, "templates", "configurations"),)

PREFIX     = "/usr"
LIBDIR     = "/usr/lib"
DATADIR    = "/usr/share"
DOCDIR     = "/usr/share/doc/cherokee-doc"
LOCALEDIR  = "/usr/share/locale"
WWWROOT    = "/var/www"
SYSCONFDIR = "/etc"
LOCALSTATE = "/var"
VERSION    = "001000000"


CHEROKEE_SERVER     = join(PREFIX, "sbin/cherokee")
CHEROKEE_WORKER     = join(PREFIX, "sbin/cherokee-worker")
CHEROKEE_ADMINDIR   = join(PREFIX, "share/cherokee/admin")
CHEROKEE_ICONSDIR   = join(PREFIX, "share/cherokee/icons")
CHEROKEE_THEMEDIR   = join(PREFIX, "share/cherokee/themes")
CHEROKEE_PANIC_PATH = join(PREFIX, "share/cherokee/cherokee-panic")
CHEROKEE_PLUGINDIR  = join(LIBDIR, "cherokee")
CHEROKEE_DATADIR    = join(DATADIR, "cherokee")
CHEROKEE_DEPSDIR    = join(DATADIR, "cherokee/deps")
CHEROKEE_CONFDIR    = join(SYSCONFDIR, "cherokee")
CHEROKEE_VAR_LOG    = join(LOCALSTATE, "log")
CHEROKEE_VAR_RUN    = join(LOCALSTATE, "run")
CHEROKEE_RRD_DIR    = join(LOCALSTATE, "lib/cherokee/graphs")
CHEROKEE_GRAPHS_DIR = join(LOCALSTATE, "lib/cherokee/graphs/images")

DEFAULT_PID_LOCATIONS = [
    '/var/run/cherokee.pid',
    join (PREFIX, 'var/run/cherokee.pid')
]
