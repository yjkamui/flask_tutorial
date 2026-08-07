from datetime import datetime

import pytz

from . import db

JST = pytz.timezone('Asia/Tokyo')


def now_jst():
    """Current JST time as a naive datetime.

    Every datetime in this app is stored naive-but-JST, so values read back
    from SQLite can be compared with each other without tzinfo mismatches.
    """
    return datetime.now(JST).replace(tzinfo=None)


class Feed(db.Model):
    """An RSS/Atom feed we collect articles from."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    url = db.Column(db.String(500), nullable=False, unique=True)
    site_url = db.Column(db.String(500))
    last_fetched_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=now_jst)

    articles = db.relationship(
        'Article',
        backref='feed',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )

    @property
    def display_name(self):
        return self.title or self.url


class Article(db.Model):
    """A single entry pulled out of a feed."""

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    # Entry id from the feed, falling back to the link. Used to skip duplicates.
    guid = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.Text)
    published_at = db.Column(db.DateTime)
    fetched_at = db.Column(db.DateTime, default=now_jst)

    __table_args__ = (
        db.UniqueConstraint('feed_id', 'guid', name='uq_article_feed_guid'),
    )

    @property
    def shown_at(self):
        """Date to show in the list: the feed's date, or when we picked it up."""
        return self.published_at or self.fetched_at
