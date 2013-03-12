import os
import shutil
import shlex
import subprocess

from cherokee_admin_api.settings import (VERSION,
                                         configuration_dirs)
from cherokee_admin_api.config import Config

def get_version():
    raise NotImplementedError

def is_valid_config(config_file):
    args = shlex.split("cherokee -C %s -t" %config_file)
    proc = subprocess.Popen(args,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    
    EXPECTED_STDERR = 'Test on %s: OK\n' %config_file

    if  proc.stderr.read() == EXPECTED_STDERR:
        return True
    else:
        return False

def generate_config(config_file,
                    template="cherokee.conf.sample"):
    """
    This function generate a configuration file based on a template.
    
    Keyword arguments
        * config_file -- Path to the configuration file you want to generate
        * template -- Used to create the config file
    """

    for dir in configuration_dirs:
        if os.path.exists(os.path.join(dir, template)):
            shutil.copyfile(os.path.join(dir, template),
                            config_file)
            break
    
    config = Config(file=config_file)
    config["config!version"] = VERSION
    config.save()
    
    