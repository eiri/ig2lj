#!/usr/bin/env python

"""
Instagram to LiveJournal cross-poster
"""

import sys
import os
import time
import cgi
import pickle
import argparse
import logging
import ConfigParser
from instagram import client, subscriptions
from jinja2 import PackageLoader, Environment
from lj import lj

def load_config(configFile):
  Config = ConfigParser.ConfigParser()
  Config.read(configFile)
  return Config

def pull_instagram(cfg, day_ago):
  user_name = cfg.get("instagram", "user")
  client_id = cfg.get("instagram", "client_id")
  client_secret = cfg.get("instagram", "client_secret")
  after = int(round(time.time())) - day_ago * 86400
  api = client.InstagramAPI(client_id=client_id, client_secret=client_secret)
  [user] = api.user_search(q=user_name, count=1)
  feed, next_ = api.user_recent_media(user_id=user.id, min_timestamp=after)
  media = []
  for post in feed:
    if post.type == 'image':
      caption = post.caption.text if post.caption else "No title"
      tags = [t.name for t in post.tags] if hasattr(post, 'tags') else []
      media.append({
        "title" : cgi.escape(caption, True),
        "image" : post.get_standard_resolution_url(),
        "preview" : post.get_low_resolution_url(),
        "thumb" : post.get_thumbnail_url(),
        "tags"  : tags
      })
  return media

def build_post(cfg, media):
  pic = "pictures" if len(media) != 1 else "picture"
  subject = "%d %s from instagram" % (len(media), pic)
  preview_number = int(cfg.get("livejournal", "preview_number"))
  env = Environment(loader=PackageLoader('ig2lj', 'tpl'))
  tpl = env.get_template('post.html')
  # # post lj
  post = tpl.render(preview=media[:preview_number],
    rest=media[preview_number:], preview_number=preview_number)
  tags = cfg.get("livejournal", "tags")
  tagline = tags if isinstance(tags, basestring) else ", ".join(tags)
  return (subject, post, tagline)

def post_lj(cfg, subject, post, tags):
  user = cfg.get("livejournal", "user")
  password = cfg.get("livejournal", "password")
  client = lj.LJServer("ig2lj/0.1.0", "ig2lj.py; %s@livejournal.com" % user)
  try:
    login = client.login(user, password)
  except lj.LJException, e:
    sys.exit(e)
  result = client.postevent(post, subject, props={"taglist": tags})
  return result

def main():
  #
  log_file = "/tmp.ig2lj.log"
  cache_file = "cache.pickle"
  config_file = "ig2lj.ini"
  #
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--debug', action='store_true')
  parser.add_argument('-f', '--force', action='store_true')
  parser.add_argument('--ago', type=int, default=1)
  args = parser.parse_args()
  if args.debug:
    logging.basicConfig(
      format='%(asctime)s %(message)s',
      level=logging.DEBUG)
  else:
    logging.basicConfig(
      format='%(asctime)s %(message)s',
      filename=log_file,
      level=logging.INFO)
  logging.info('Reading config')
  cfg = load_config(config_file)
  logging.info('Quering Instagram')
  media = pull_instagram(cfg, args.ago)
  logging.debug("Got %s images total" % len(media))
  if args.force:
    logging.debug("Running with --force, removing cache")
    os.remove(cache_file)
  if os.path.isfile(cache_file):
    logging.info("Checking cache")
    prev_images = pickle.load(open(cache_file, "rb"))
    post_media = [m for m in media if m["image"] not in prev_images]
  else:
    post_media = media
  logging.info('Got %d new images since %s day ago'
    % (len(post_media), args.ago))
  if len(post_media) > 0:
    logging.info("Storing cache")
    images_to_cache = set((m['image'] for m in post_media))
    pickle.dump(images_to_cache, open("cache.p", "wb"))
    logging.info('Building post')
    (subject, post, tags) = build_post(cfg, post_media)
    logging.info('Posting to LJ')
    if args.debug:
      logging.debug('%s\nSubject: %s\nPost:\n%s\nTags: %s\n%s'
        % ('-'*80, subject, post, tags, '-'*80))
    else:
      post_lj(cfg, subject, post, tags)
  else:
    logging.info('Nothing to post into LJ')
  logging.info('Done')
  sys.exit(0)

if __name__ == "__main__":
  main()