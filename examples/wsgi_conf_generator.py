import os
import sys

from cherokee_admin_api import generate_config
from cherokee_admin_api.admin import Admin

class ConfGenerator(object):
            
    def cherokee(self):
        generate_config(config_file="wsgi-cherokee-gene.conf")
        admin = Admin(config_file="wsgi-cherokee-gene.conf")
        vserver_dict = {
            'match' : 'target_ip',
            'match!to!1' : '127.0.0.1',
        }
        admin.create_vserver(nick="my_vserver", document_root="/dev/null",
                             **vserver_dict)
        my_vserver = admin.get_vserver_by_nick('my_vserver')
        source_host = "127.0.0.1:1234"
        uwsgi_module = "uwsgi_settings"
        current_dir = os.getcwd()
        python_home = sys.prefix
        uwsgi_bin = os.path.join(python_home, "bin", "uwsgi")
        source_dict = {
            'interpreter': '%s -s %s -H %s -w %s --pythonpath %s' % (uwsgi_bin,
                                                                     source_host,
                                                                     python_home,
                                                                     uwsgi_module,
                                                                     current_dir)
        }
        admin.create_source(nick="my_uwsgi_source", type="interpreter",
                            host=source_host,
                            **source_dict)
        
        
        my_uwsgi_source = admin.get_source_by_nick("my_uwsgi_source")

        rule_dict = {
            "disabled" : "0",
            "encoder!deflate" : "allow",
            "encoder!gzip" : "allow",
            "handler" : "uwsgi",
            "handler!balancer" : "round_robin",
            "handler!balancer!source!1" : my_uwsgi_source.split("!").pop(),
            "handler!change_user" : "0",
            "handler!check_file" : "0",
            "handler!error_handler" : "1",
            "handler!pass_req_headers" : "1",
            "handler!x_real_ip_access_all" : "0",
            "handler!x_real_ip_enabled" : "0",
            "handler!xsendfile" : "0",
            "match" : "directory",
            "match!directory" : "/wsgi_app",
            "match!final" : "1",
            "no_log" : "0",
            "only_secure" : "0",
        }
        admin.create_rule(vserver_path=my_vserver, **rule_dict)
        admin.config["server!bind!1!port"] = "82"
        admin.config.save()

        
if __name__ == '__main__':
    cg = ConfGenerator()
    cg.cherokee()