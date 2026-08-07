"""Default feeds inserted the first time the app starts."""

from . import db
from .models import Feed

DEFAULT_FEEDS = [
    ('NHK 主要ニュース', 'https://www.nhk.or.jp/rss/news/cat0.xml'),
    ('ITmedia NEWS', 'https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml'),
    ('はてなブックマーク テクノロジー', 'https://b.hatena.ne.jp/hotentry/it.rss'),
    ('Publickey', 'https://www.publickey1.jp/atom.xml'),
    ('GIGAZINE', 'https://gigazine.net/news/rss_2.0/'),
]


def seed_default_feeds():
    """Register the starter feeds, but only on a brand new database."""
    if db.session.query(Feed.id).first():
        return
    for title, url in DEFAULT_FEEDS:
        db.session.add(Feed(title=title, url=url))
    db.session.commit()
