from __future__ import print_function
import os
import sys
import json
import io
import imp
import ConfigParser
import types
import os.path

try:
    import yaml
    OMNICONFIG_YAML = True
except ImportError:
    OMNICONFIG_YAML = False

class OmniConfig():
    def __init__(self, d=None, conf_dir=None):
        self._conf_dir = conf_dir
        if d:
            self._parse(d)


    def load_config(self, config_file=None):
        _main_json = 'conf.json'

        if config_file:
            _main_json = config_file
        elif os.environ.get('CONFIG', False):
            _main_json = os.environ['CONFIG']

        self._conf_dir = os.path.dirname(os.path.abspath(_main_json))

        with open(_main_json) as f:
            d = json.load(f)

        self._parse(d)


    def _parse(self, d):
        for k, v in d.items():
            if k == '_include':
              self._include(v)
            elif isinstance(d, (list, tuple)):
               setattr(self, k, [OmniConfig(x, self._conf_dir) if isinstance(x, dict) else x for x in v])
            else:
               setattr(self, k, OmniConfig(v, self._conf_dir) if isinstance(v, dict) else v)


    def _include(self, filename):

        # include is relative to the main config loaded
        if not os.path.isabs(filename):
            filename = os.path.join(self._conf_dir, filename)

        extension = filename.split('.')[-1]
        cfg = dict()

        if extension in ('yml', 'yaml'):
            # parse yml
            if not OMNICONFIG_YAML:
                raise OmniConfigException('To include yml file you must install pyaml first')
            with open(filename) as f:
                cfg = yaml.load(f)

        elif extension in ('ini', 'cfg', 'conf'):
            # use config parser
            with open(filename) as f:
                cfgf = f.read()
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(io.BytesIO(cfgf))

            for section in config.sections():
                tmp_section= dict()
                for options in config.options(section):
                    tmp_section[options] = config.get(section, options)

                cfg[section] = tmp_section

        elif extension == 'json':
            with open(filename) as f:
                cfg = json.load(f)

        elif extension == 'py':
            module = filename.split("/")[-1].replace('.py', '')
            mod = imp.load_source(module, filename)
            cfg = {k: v for k,v in mod.__dict__.iteritems() if not (k.startswith('_') or isinstance(v, types.FunctionType ))}

        elif extension == 'plist':
            raise Exception('Not yet implemented') # TODO: impl this

        else:
            raise OmniConfigException('Unsupported extension %s OmniConfig doesn\'t know hoe to parse it')


        self._parse(cfg)

class OmniConfigException(Exception):
    pass

try:
    c = OmniConfig()
    c.load_config()
except:
    c = None
