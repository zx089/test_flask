from flask import Blueprint, render_template, jsonify, g
from flask_login import login_required, current_user
from flask_expects_json import expects_json
from .models import Post
from . import db


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    created_on = current_user.created_on.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('profile.html',
                           name=current_user.name,
                           created=created_on)


@main.route('/library')
@login_required
def library():
    return render_template('library.html')


schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'text': {'type': 'string'}
    },
    'required': ['name', 'text']
}


@main.route('/posts/<int:post_id>', methods=['PUT'])
@expects_json(schema)
@login_required
def edit(post_id):
    Post.query.filter_by(user_id=current_user.id).filter_by(id=post_id).update({
        'name': g.data.get('name'),
        'text': g.data.get('text')})
    db.session.commit()
    return render_template('library.html'), 204


@main.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete(post_id):
    Post.query.filter_by(user_id=current_user.id).filter_by(id=post_id).update({'is_deleted': True})
    db.session.commit()
    return render_template('library.html'), 204


@main.route('/posts', methods=['POST'])
@expects_json(schema)
@login_required
def add():
    g.data['user_id'] = current_user.id
    new_post = Post(**g.data)
    db.session.add(new_post)
    db.session.commit()
    return render_template('library.html'), 204


@main.route('/posts', methods=['GET'])
@login_required
def get():
    users_posts = Post.query.filter_by(user_id=current_user.id).filter_by(is_deleted=False).order_by(Post.id.desc())
    results = [post.as_dict() for post in users_posts]
    return jsonify({'count': len(results), 'results': results})

