omniconfig
==========

> a small utility to gather several config files in one interface, python of course!

Why?
----
Now that microservices are trending (because it's an awesome way to think of complex system), it happens to replicate some configuration of a common service (ie. `redis` host/port ) across different processes or access from your python microservice the config file of a another service.   
What if you could *include* other config files, whatever the format (`.ini`, `.yml`, ...) and access from a unique "config" object?   
Enters `omniconfig`

Usage
-----
omniconfig need a main config file in `json` format, in it you can with the special key `_include` include other files. 
**NOTE THAT includes are always relative to main json file**   
The extension of the file included dictates the way it is parsed.  
Given this files:

**config.json**

	{
	  "database": {   
	    "host": "10.10.10.10",
	    "port": 2323
	  },
	  "yaml": {
	    "_include": "example.yml"
	  }
	}

**example.yml**

	mysql:
    	host: localhost
    	user: root
    	
`omniconfig` can know about the main json file in 3 ways:

1. by **convention**: if you put it in the same directory and name it `conf.json`
2. with an **environment variable** that is `CONFIG`
3. explicitly in code when you init the object

```python
myconf = OmniConfig()

# 1. or 2.
myconf.load_config()

# 3.
myconf.load_config("conf/myconf.json")
```

or if you are in case 1 or 2 you can just this handler import

```python
from omniconfig import c as myconf
```

After you have your omniconfig object you can directly access the config structure as a python object, given the previous files you can:

```python
>>> print(myconf.database.host)
$ 10.10.10.10
>>> print(myconf.yaml.mysql.host)
$ localhost
```
That easy!!

### Supported formats to include
- json
- yaml
- ini, cfg (aka`ConfigParser`)
- python 
- plist

Install
-------
you can use good 'ol pip   
`pip install omniconfig`

Or if you prefer, you can just drop the single file inside your project   
`wget http://asdasd`   
it depends only on pyaml and only if you intend to include yaml files

Contribute
----------
Usual way: fork /  pull request happiness !   
Will be happy to add strange config file formats :)
