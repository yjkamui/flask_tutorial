"""Fetching and parsing of RSS/Atom feeds."""

import re
import socket
from calendar import timegm
from datetime import datetime

import feedparser
import pytz

from . import db
from .models import JST, Article, now_jst

TAG_RE = re.compile(r'<[^>]+>')
SUMMARY_MAX = 200
FETCH_TIMEOUT = 15


def clean_summary(raw):
    """Strip the HTML out of a feed summary and shorten it for the list view."""
    if not raw:
        return ''
    text = TAG_RE.sub('', raw)
    text = ' '.join(text.split())
    if len(text) > SUMMARY_MAX:
        text = text[:SUMMARY_MAX] + '…'
    return text


def published_at(entry):
    """Convert a feedparser time tuple (always UTC) into a naive JST datetime."""
    parsed = entry.get('published_parsed') or entry.get('updated_parsed')
    if not parsed:
        return None
    utc = datetime.fromtimestamp(timegm(parsed), tz=pytz.utc)
    return utc.astimezone(JST).replace(tzinfo=None)


def parse_url(url):
    """Download and parse a feed. Network errors come back on the result."""
    socket.setdefaulttimeout(FETCH_TIMEOUT)
    return feedparser.parse(url)


def parse_error(parsed):
    """Return a human-readable reason the parse failed, or None if it worked."""
    status = parsed.get('status')
    if status and status >= 400:
        return f'HTTP {status}'
    if parsed.entries:
        return None
    if parsed.get('bozo'):
        return str(parsed.get('bozo_exception') or 'could not be parsed as a feed')
    return 'no entries found'


def fetch_feed(feed):
    """Save any entries of `feed` we don't have yet.

    Returns (added_count, error_message); error_message is None on success.
    """
    parsed = parse_url(feed.url)
    error = parse_error(parsed)
    if error:
        return 0, error

    # Fill in metadata the user didn't type in by hand.
    info = parsed.get('feed', {})
    if not feed.title:
        feed.title = (info.get('title') or '')[:120] or None
    if not feed.site_url:
        feed.site_url = (info.get('link') or '')[:500] or None

    known = {
        guid for (guid,) in
        db.session.query(Article.guid).filter(Article.feed_id == feed.id)
    }

    added = 0
    for entry in parsed.entries:
        url = entry.get('link')
        if not url:
            continue
        guid = entry.get('id') or url
        if guid in known:
            continue
        known.add(guid)

        db.session.add(Article(
            feed_id=feed.id,
            guid=guid[:500],
            title=(entry.get('title') or '(タイトルなし)')[:300],
            url=url[:500],
            summary=clean_summary(entry.get('summary')),
            published_at=published_at(entry),
        ))
        added += 1

    feed.last_fetched_at = now_jst()
    db.session.commit()
    return added, None


def fetch_all(feeds):
    """Refresh every feed. Returns (total_added, ['<feed>: <error>', ...])."""
    total = 0
    errors = []
    for feed in feeds:
        added, error = fetch_feed(feed)
        total += added
        if error:
            errors.append(f'{feed.display_name}: {error}')
    return total, errors
