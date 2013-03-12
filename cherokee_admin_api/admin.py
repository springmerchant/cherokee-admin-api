from cherokee_admin_api.config import Config
from cherokee_admin_api.settings import (STEP_RULE,
                                         STEP_SOURCE,
                                         STEP_VSERVER,
                                         CHEROKEE_ICONSDIR,
                                         CHEROKEE_THEMEDIR)

class Admin(object):
    def __init__(self, config_file):
        self.config = Config(file=config_file)
        
    def get_vservers(self):
        _vservers = []
        for vserver_i in self.config["vserver"]:
            _vservers.append("vserver!%s" %vserver_i)
        return _vservers
    
    def get_sources(self):
        _sources = []
        for source_i in self.config["source"]:
            _sources.append("source!%s" %source_i)
        return _sources
    
    def get_rules(self, vserver):
        _rules = []
        for rule_i in self.config[vserver]['rule']:
            _rules.append("%s!rule!%s" %(vserver,rule_i))
        return _rules
        
    def get_vserver_by_nick(self, nick):
        for vserver in self.get_vservers():
            if self.config[vserver]["nick"]:
                if self.config[vserver]["nick"].value == nick:
                    return vserver
        else:
            return None
            
    def get_vservers_by_domain(self, domain_match):
        vservers_domain_match = []
        for vserver in self.get_vservers():
            if self.config[vserver]['match!domain']:
                for domain in self.config[vserver]['match!domain'] :
                    if self.config[vserver]['match!domain'][domain].value == domain_match:
                        vservers_domain_match.append(vserver)
        return vservers_domain_match
        
    def get_source_by_nick(self, nick):
        for source in self.get_sources():
            if self.config[source]["nick"]:
                if self.config[source]["nick"].value == nick:
                    return source
        else:
            return None
        
    def get_rule_by_directory(self, directory):
        _rule_paths = []
        for vserver_i in self.get_vservers():
            if self.config[vserver_i]["rule"]:
                for rule_i in self.get_rules(vserver_i):
                    if self.config[rule_i]["match"]["directory"]:
                        if self.config[rule_i]["match"]["directory"].value == directory:
                            _rule_paths.append(rule_i)
        return _rule_paths
        
    def nodify(self, key_list):
        nodes = []
        for key in key_list:
            nodes.append(self.config[key])
        return nodes
        
    def create_vserver(self, nick, document_root, **kwargs):
        return Admin._create_vserver(self.config, nick, document_root, **kwargs)
        
    def create_source(self, nick, host, type, **kwargs):
        return Admin._create_source(self.config, nick, host,
                                    type, **kwargs)
        
    def create_rule(self, vserver_path, **kwargs):
        new_rule_path = self.config.get_next_entry_prefix(pre=vserver_path+"!rule")
        for k in kwargs.keys():
            self.config[new_rule_path + "!%s" %k] = kwargs[k]
        self.config.normalize(pre=vserver_path+"!rule", step=STEP_RULE)
        self.config.save()
            
        
    @classmethod     
    def _create_default_rules(cls, config, vserver_path):
        """
        Create the default rules that are defined by cherokee admin.
        """
        config[vserver_path]['rule!1!match'] = 'default'
        config[vserver_path]['rule!1!handler'] = 'common'
                             
        config[vserver_path]['rule!2!match'] = 'directory'
        config[vserver_path]['rule!2!match!directory'] = '/icons'
        config[vserver_path]['rule!2!handler'] = 'file'
        config[vserver_path]['rule!2!document_root'] = CHEROKEE_ICONSDIR
                             
        config[vserver_path]['rule!3!match'] = 'directory'
        config[vserver_path]['rule!3!match!directory'] = '/cherokee_themes'
        config[vserver_path]['rule!3!handler'] = 'file'
        config[vserver_path]['rule!3!document_root'] = CHEROKEE_THEMEDIR
     
    @classmethod    
    def _create_vserver(cls, config, nick, document_root, **kwargs):
        """
        Create a vserver
        """
        new_vserver_path = config.get_next_entry_prefix(pre="vserver")
        # mandatory information to create a vserver
        config[new_vserver_path + "!nick"] = nick
        config[new_vserver_path]["document_root"] = document_root
        Admin._create_default_rules(config, new_vserver_path)
        for k in kwargs.keys():
            config[new_vserver_path + "!%s" %k] = kwargs[k]  
        config.normalize(pre="vserver", step=STEP_VSERVER)
        config.save()
    
    @classmethod 
    def _create_source(cls, config, nick, host,
                       type, **kwargs):
        """
        Create a source
        """
        new_source_path = config.get_next_entry_prefix(pre="source")
        config[new_source_path + "!nick"] = nick
        config[new_source_path + "!host"] = host
        config[new_source_path + "!type"] = type
        for k in kwargs.keys():
            config[new_source_path + "!%s" %k] = kwargs[k]   
        config.normalize(pre="source", step=STEP_SOURCE)
        config.save()
        
    
    @classmethod 
    def _create_rule(cls, config, vserver_path, **kwargs):
        new_rule_path = config.get_next_entry_prefix(pre=vserver_path+"!rule")
        for k in kwargs.keys():
            config[new_rule_path + "!%s" %k] = kwargs[k]
        config.normalize(pre=vserver_path+"!rule", step=STEP_RULE)
        config.save()
    