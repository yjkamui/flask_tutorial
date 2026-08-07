from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .feeds import fetch_all, fetch_feed
from .forms import FeedForm
from .models import Article, Feed

article_bp = Blueprint('article', __name__, url_prefix='/')
feed_bp = Blueprint('feed', __name__, url_prefix='/feeds')

PER_PAGE = 20


def _report(added, errors):
    """Turn a fetch result into flash messages."""
    if added:
        flash(f'{added}件の新しい記事を取得しました。', 'success')
    elif not errors:
        flash('新しい記事はありませんでした。', 'success')
    for error in errors:
        flash(f'取得に失敗しました - {error}', 'error')


@article_bp.route('/')
@article_bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    feed_id = request.args.get('feed_id', type=int)

    query = Article.query
    selected = None
    if feed_id:
        selected = db.get_or_404(Feed, feed_id)
        query = query.filter(Article.feed_id == feed_id)

    # published_at is missing on some feeds, so fall back to when we fetched it.
    newest_first = db.func.coalesce(Article.published_at, Article.fetched_at).desc()
    query = query.order_by(newest_first, Article.id.desc())

    articles = db.paginate(query, page=page, per_page=PER_PAGE, error_out=False)
    feeds = Feed.query.order_by(Feed.id).all()
    return render_template('index.html', articles=articles, feeds=feeds, selected=selected)


@article_bp.route('/refresh', methods=['POST'])
def refresh():
    added, errors = fetch_all(Feed.query.all())
    _report(added, errors)
    return redirect(request.referrer or url_for('article.index'))


@feed_bp.route('/', methods=['GET', 'POST'])
def list_feeds():
    form = FeedForm()
    if form.validate_on_submit():
        url = form.url.data.strip()
        if Feed.query.filter_by(url=url).first():
            flash('そのフィードはすでに登録されています。', 'error')
        else:
            feed = Feed(url=url, title=form.title.data.strip() or None)
            db.session.add(feed)
            db.session.commit()

            added, error = fetch_feed(feed)
            if error:
                # Keep the feed registered so the user can fix or retry it.
                flash(f'フィードを追加しましたが、取得に失敗しました - {error}', 'error')
            else:
                flash(f'{feed.display_name} を追加し、{added}件の記事を取得しました。', 'success')
            return redirect(url_for('feed.list_feeds'))

    feeds = Feed.query.order_by(Feed.id).all()
    counts = dict(
        db.session.query(Article.feed_id, db.func.count(Article.id))
        .group_by(Article.feed_id)
        .all()
    )
    return render_template('feeds.html', form=form, feeds=feeds, counts=counts)


@feed_bp.route('/<int:id>/refresh', methods=['POST'])
def refresh_feed(id):
    feed = db.get_or_404(Feed, id)
    added, error = fetch_feed(feed)
    _report(added, [f'{feed.display_name}: {error}'] if error else [])
    return redirect(request.referrer or url_for('feed.list_feeds'))


@feed_bp.route('/<int:id>/delete', methods=['POST'])
def delete_feed(id):
    feed = db.get_or_404(Feed, id)
    name = feed.display_name
    # Article rows go with it via the cascade on Feed.articles.
    db.session.delete(feed)
    db.session.commit()
    flash(f'{name} を削除しました。', 'success')
    return redirect(url_for('feed.list_feeds'))
