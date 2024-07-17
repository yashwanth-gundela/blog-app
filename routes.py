from flask import Blueprint, request, jsonify
from app import db
from models import BlogPost, UserTable
from auth import auth

api_bp = Blueprint('api', __name__)

@api_bp.route('/posts', methods=['POST'])
@auth.login_required
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    if title is None or content is None:
        return jsonify({'message': 'Missing arguments'}), 400
    post = BlogPost(title=title, content=content, user_id=auth.current_user().id)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

@api_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id} for post in posts])

@api_bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = BlogPost.query.get_or_404(id)
    return jsonify({'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id})

@api_bp.route('/posts/<int:id>', methods=['PUT'])
@auth.login_required
def update_post(id):
    post = BlogPost.query.get_or_404(id)
    if post.user_id != auth.current_user().id:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})

@api_bp.route('/posts/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    if post.user_id != auth.current_user().id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})
