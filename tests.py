from unittest import TestCase
from test.test_support import EnvironmentVarGuard
from omniconfig import OmniConfig, OmniConfigException
import os
import json


class MainFileTests(TestCase):

    def setUp(self):
        self.example_conf = 'examples/example.json'
        self.tmp_dict = {'test': True}

    def test_passing_file(self):
        c = OmniConfig()
        c.load_config(self.example_conf)
        assert c.database.port == 2323

    def test_environment(self):
        e = EnvironmentVarGuard()
        e.set('CONFIG', 'env.json')
        with open('env.json','w') as f:
           json.dump(self.tmp_dict, f)
        with e:
            c = OmniConfig()
            c.load_config()
            os.unlink("env.json")
            assert c.test

    def test_default(self):
        with open('conf.json','w') as f:
            json.dump(self.tmp_dict, f)
        c = OmniConfig()
        c.load_config()
        os.unlink('conf.json')
        assert c.test

    def test_file_not_present_raises(self):
        with self.assertRaises(IOError):
            c = OmniConfig()
            c.load_config()

    def test_yml(self):
        c = OmniConfig()
        c.load_config(self.example_conf)

        assert c.yaml.mysql.host == 'localhost'

    def test_ini(self):
        c = OmniConfig()
        c.load_config(self.example_conf)

        assert c.ini.mysql.user == 'root'


    def test_json(self):
        c = OmniConfig()
        c.load_config(self.example_conf)

        assert c.node.test

    def test_py(self):
        c = OmniConfig()
        c.load_config(self.example_conf)

        assert c.python.HELP == 5
        with self.assertRaises(Exception):
            c.help_func

    def test_unknown_ext(self):
        with open('conf.json','w') as f:
            json.dump({"a":"b", "_include":"example.unk"}, f)

        with self.assertRaises(OmniConfigException):
            c = OmniConfig()
            c.load_config()
        os.unlink('conf.json')

