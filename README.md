# Instagram to LiveJournal cross-poster

## Update June 1, 2016

Since Instagram is now playing Apple's app store with sandboxing, approving and rest of the dance, this could take more twiggling around to get setup. I haven't tried the new process myself, so no idea how much hustle is it. 

## Synopsis

This is a simple python script that automatically translates images posted on [Instagram](http://instagram.com) to [LiveJournal](http://www.livejournal.com)

## Installation

```bash
$ git clone https://github.com/eiri/ig2lj.git
$ virtualenv venv
$ source venv/bin/activate
$ pip install git+https://github.com/eiri/ig2lj.git@master
```

## Usage

Register at Instagram and get client_id. Edit ig2lj.ini accordingly. Edit livejournal's post template `tpl/post.html` to your liking. THen run the script:

```
usage: ig2lj.py [-h] [-d] [-f] [--ago AGO]

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug
  -f, --force
  --ago AGO
```

## Crontab

Edit `croned.sh` to `cd` in the installation directory. Set to run every night with something like

`12 1 * * * /Installation/Dir/croned.sh > /tmp/ig2lj.cron.log 2>&1`

## TODO

  - Store date of the last update and pull all the instagram images since then
  - Move log and cache location in config file under `[main]` section 

## Changelog

  - 0.1.0 - Initial release

## Licence

[MIT](https://github.com/eiri/ig2lj/blob/master/LICENSE)
