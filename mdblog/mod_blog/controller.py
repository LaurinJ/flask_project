from flask import Blueprint
from flask import render_template


from mdblog.models import Article

blog = Blueprint("blog", __name__)

@blog.route("/blogs/", methods=["GET"])
def view_blogs():
    articles = Article.query.order_by(Article.id.desc())
    return render_template('mod_blog/view_blogs.html', articles=articles)

@blog.route("/blog/<int:art_id>")
def view_blog(art_id):
    article = Article.query.filter_by(id=art_id).first()
    if article:
        return render_template("mod_blog/view_blog.html", article=article)
    return render_template('mod_blog/article_not_found.html', art_id=art_id)