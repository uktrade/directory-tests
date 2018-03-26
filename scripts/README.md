# URLs checker script

Is a simple script that will repeatedly fetch URLs in a configurable time 
interval.


## Requirements

* Python 3.5+
* [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
* [async-timeout](https://pypi.python.org/pypi/async_timeout/)


# VirtualEnv

```shell
mkvirtualenv -p python3.5 async-urls
pip install -r requirements_urls_checker.txt
```

# Usage

```shell
$ ./urls-checker.py -h
usage: urls-checker.py [-h] -u URLSFILE [-l LIMIT] [-i INTERVAL]
                       [-a USER_AGENT] [-t TIMEOUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -u URLSFILE, --urlsfile URLSFILE
                        Path to a file with URLs to monitor
  -l LIMIT, --limit LIMIT
                        Limit monitoring to N consequent requests
  -i INTERVAL, --interval INTERVAL
                        Number of seconds between requests
  -a USER_AGENT, --user-agent USER_AGENT
                        User-Agent header value
  -t TIMEOUT, --timeout TIMEOUT
                        Request timeout
  -v, --verbose         Print intermediate status codes
```


# Running the script

To run the script you'll need a text file with a list of URLs to check.
e.g.:
```text
https://google.com
http://cnn.com
```

Once you have such file then run the script:
```shell
./urls-checker.py -u urls.txt
```
