import os
import shutil
from unittest import TestCase

from nose.plugins.skip import Skip, SkipTest

from cherokee_admin_api import (get_version,
                                is_valid_config,
                                generate_config)

from cherokee_admin_api.admin import Admin
from cherokee_admin_api.config import Config
from cherokee_admin_api.settings import VERSION

BASE_DIR = os.path.dirname(__file__)
CHEROKEE_CONF = os.path.join(BASE_DIR,
                             "cherokee.conf")
TMP_CHEROKEE_CONF = os.path.join(BASE_DIR, "cherokee-tmp.conf")
UWSGI_INTERPRETER = "uwsgi26 -s 127.0.0.1:10092 -C \
-H /opt/webapps/dev.gwadeloop.com/ \
-w project_cms.conf.dev.uwsgi_settings -M -p 2 -t 10"

def _remove_tmp_cherokee_conf(tmp_conf_file):
    try: 
        os.remove(tmp_conf_file)
    except:
        pass
    try:
        os.remove(tmp_conf_file + ".backup")
    except:
        pass


class TestConfig(TestCase):
    def setUp(self):
        """
        Duplicate the template of the cherokee.conf before starting the test.
        """
        shutil.copyfile(CHEROKEE_CONF, TMP_CHEROKEE_CONF)
        self.cfg  = Config(file=TMP_CHEROKEE_CONF)
        
    def tearDown(self):
        _remove_tmp_cherokee_conf(TMP_CHEROKEE_CONF)
            
    def dummy_test(self):
        self.assertEqual(1+1,2)
        
    def test_change_save_configuration(self):
        self.assertEqual(self.cfg["vserver!40!match!domain"].get_val("1"),
                         "example.com")
        self.cfg["vserver!40!match!domain"].set_value("1","demo.com")
        self.assertEqual(self.cfg["vserver!40!match!domain"].get_val("1"),
                         "demo.com")
        self.cfg.save()
        with open(TMP_CHEROKEE_CONF, 'r') as f:
            conf_data = f.read()
            # check that demo.com is found in TMP_CHEROKEE_CONF
            self.assertEqual(conf_data.find("demo.com")>0,
                             True)
        
    def test_clone_normalise_vserver(self):
        new_vserver_path  = self.cfg.get_next_entry_prefix("vserver")
        self.cfg.clone("vserver!40", new_vserver_path)
        self.cfg.normalize(pre="vserver")
        self.cfg.save()
        vserver_keys = self.cfg["vserver"].keys()
        vserver_keys.sort()
        self.assertEqual(vserver_keys,
                         ['10', '20', '30', '40'])
        
class TestGenerateConfig(TestCase):
    def setUp(self):
        self.test_dir = "/tmp/test-suite"
        self.conf_file = "cherokee.conf"
        os.makedirs(self.test_dir)
    
    def tearDown(self):
        try:
            shutil.rmtree(self.test_dir)
        except:
            pass
    
    def test_generate_config(self):
        config_file = os.path.join(self.test_dir,self.conf_file)
        self.assertEqual(os.path.exists(config_file),
                         False)
        
        generate_config(config_file=config_file)
        self.assertEqual(os.path.exists(config_file),
                         True)
        
        cfg = Config(file=config_file)
        self.assertEqual(cfg["config"].get_val('version'),VERSION)   
            
  
  
class TestIsValidConfig(TestCase):
    def setUp(self):
        """
        Duplicate the template of the cherokee.conf before starting the test.
        """
        shutil.copyfile(CHEROKEE_CONF, TMP_CHEROKEE_CONF)
        self.config_file = TMP_CHEROKEE_CONF
        
    def tearDown(self):
        _remove_tmp_cherokee_conf(TMP_CHEROKEE_CONF)
        
    def test_is_valid_config(self):
        self.assertEqual(is_valid_config(config_file=self.config_file),True)
        
class TestAdmin(TestCase):
    def setUp(self):
        """
        Duplicate the template of the cherokee.conf before starting the test.
        """
        shutil.copyfile(CHEROKEE_CONF, TMP_CHEROKEE_CONF)
        self.admin = Admin(config_file=TMP_CHEROKEE_CONF)
        
    def tearDown(self):
        _remove_tmp_cherokee_conf(TMP_CHEROKEE_CONF)
        
    def test_get_vservers(self):
        vservers = self.admin.get_vservers()
        self.assertEqual(len(vservers), 3)
        self.assertEqual([vserver["nick"].value for vserver in self.admin.nodify(vservers)],
            ['default', 'example.com', 'django'])
    
    def test_get_sources(self):
        sources = self.admin.get_sources()
        self.assertEqual(len(sources), 3)
        self.assertEqual([source["nick"].value for source in self.admin.nodify(sources)],
            ['varnish_gwadeloop.com', 'uwsgi_gwadeloop.com', 'uwsgi_dev.gwadeloop.com'])
        
    def test_get_rules(self):
        vservers = self.admin.get_vservers()
        for vserver in vservers:
            if self.admin.config[vserver]["nick"]:
                if self.admin.config[vserver]["nick"].value == "django":
                    rules = self.admin.nodify(self.admin.get_rules(vserver))
        self.assertEqual([rule["match!directory"].value for rule in rules if rule["match"].value == "directory"],
            ['/', '/admin-media', '/test_app', '/cherokee_admin', '/media', '/static'])
        
    def test_get_vserver_by_domain(self):
        DOMAIN = "example.com"
        vservers = self.admin.get_vservers_by_domain(DOMAIN)
        self.assertEqual(vservers,
                         ['vserver!50', 'vserver!40'])
        
    def test_create_vserver(self):
        """
        This test create a new vserver.
        """
        self.assertEqual(self.admin.get_vserver_by_nick("foo"), None)
        self.assertEqual(len(self.admin.config["vserver"].keys()), 3)
        self.admin.create_vserver(nick="foo", document_root="/dev/null")
        vserver_path = self.admin.get_vserver_by_nick("foo")
        self.assertEqual(vserver_path, 'vserver!400')
        self.assertEqual(len(self.admin.config["vserver"].keys()), 4)
        
    def test_create_source(self):
        """
        This test create a source.
        """
        self.assertEqual(self.admin.get_source_by_nick("bar"), None)
        self.assertEqual(len(self.admin.config["source"].keys()), 3)
        self.admin.create_source(nick="bar", host="/tmp/bar.sock",
                      **{'type': "interpreter",
                       "interpreter": UWSGI_INTERPRETER})
        source_path = self.admin.get_source_by_nick("bar")
        self.assertEqual(source_path, 'source!4')
        self.assertEqual(self.admin.config[source_path].get_val("interpreter"),
                         UWSGI_INTERPRETER)
        self.assertEqual(len(self.admin.config["source"].keys()), 4)
        
    def test_create_rule(self):
        """
        This test create a rule
        """
        self.assertEqual(len(self.admin.get_rule_by_directory("/foo")),
                         0)
        rule_dict = {
            "disabled" : "0",
            "document_root" : "/var/www/example.com/foo",
            "handler" : "file",
            "handler!iocache" : "1",
            "match" : "directory",
            "match!directory" : "/foo",
            "match!final" : "1",
            "no_log" : "0",
            "only_secure" : "0",
        }
        self.admin.create_rule(vserver_path="vserver!10", **rule_dict)
        self.assertEqual(len(self.admin.get_rule_by_directory("/foo")),
                         1)
        

class TestAdminTutorial(TestCase):
       
    def tearDown(self):
        """
        Clean up the temporary file
        """
        _remove_tmp_cherokee_conf(TMP_CHEROKEE_CONF)
        
    def test_usage(self):
        generate_config(config_file=TMP_CHEROKEE_CONF)
        admin = Admin(config_file=TMP_CHEROKEE_CONF)
        admin.create_vserver(nick="my-vserver", document_root="/dev/null")
        admin.create_source(nick="my-source", type="host", host="/tmp/host_socket.sock")
        rule_dict = {
            "disabled" : "0",
            "document_root" : "/var/www/example.com/foo",
            "handler" : "file",
            "handler!iocache" : "1",
            "match" : "directory",
            "match!directory" : "/foo",
            "match!final" : "1",
            "no_log" : "0",
            "only_secure" : "0",
        }
        admin.create_rule(vserver_path="vserver!10", **rule_dict)
        
  
class TestToDo(TestCase):
    def test_get_version(self):
        try:
            get_version()
        except NotImplementedError:
            raise SkipTest
        

    