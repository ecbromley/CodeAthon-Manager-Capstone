from flask import render_template, request, Blueprint
from codeathon.models import Post

challenges = Blueprint('challenges', __name__)

@challenges.route("/challenges")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('challenges.html', posts=posts)