from flask import Blueprint
from flask import render_template
from flask import request

from mdblog.models import Article

blog = Blueprint("blog", __name__)

@blog.route("/blogs/", methods=["GET"])
def view_blogs():
    page = request.args.get("page", 1, type=int)
    paginate = Article.query.order_by(Article.id.desc()).paginate(page, 5, False)
    return render_template('mod_blog/view_blogs.html', articles=paginate.items, paginate=paginate)

@blog.route("/blog/<int:art_id>")
def view_blog(art_id):
    article = Article.query.filter_by(id=art_id).first()
    if article:
        return render_template("mod_blog/view_blog.html", article=article)
    return render_template('mod_blog/article_not_found.html', art_id=art_id)