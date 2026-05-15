from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import TEXT

from .forms import ArticleForm
from .decorators import moderator_required

from cattlestock.mongodb import (
    article_collection,
    bookmarks_collection,
    likes_collection,
    comments_collection,
)

article_collection.create_index([
    ('title', TEXT),
    ('content', TEXT),
    ('category', TEXT),
])

def article_list(request):
    query = request.GET.get('q')
    if query:
        article = list(
            article_collection.find({
                '$text': {'$search': query},
                'status': 'approved'
            }).sort('created_at', -1)
        )
    else:
        article = list(
            article_collection.find({'status': 'approved'}).sort('created_at', -1)
        )
    return render(request, 'article/article_list.html', {
        'article': article,
        'current_page': 'article',
    })

def article_detail(request, article_id):
    article = article_collection.find_one({
        '_id': ObjectId(article_id),
        'status': 'approved'
    })
    likes_count = likes_collection.count_documents({'article_id': article_id})
    comments = list(
        comments_collection.find({'article_id': article_id}).sort('created_at', -1)
    )
    return render(request, 'article/article_detail.html', {
        'article': article,
        'likes_count': likes_count,
        'comments': comments,
    })

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_data = {
                'title': form.cleaned_data['title'],
                'category': form.cleaned_data['category'],
                'article_tags': form.cleaned_data['tags'].split(','),
                'image': form.cleaned_data['image'],
                'content': form.cleaned_data['content'],
                'author': request.user.username,
                'status': 'pending',
                'approved_by': None,
                'approver_post': None,
                'meta_title': form.cleaned_data['title'],
                'meta_description': form.cleaned_data['content'][:160],
                'created_at': datetime.now(),
            }
            article_collection.insert_one(article_data)
            return redirect('article')
    else:
        form = ArticleForm()
    return render(request, 'article/create_article.html', {'form': form})

@login_required
def edit_article(request, article_id):
    article = article_collection.find_one({'_id': ObjectId(article_id)})
    if article['author'] != request.user.username:
        return redirect('article')
    if request.method == 'POST':
        updated_data = {
            'title': request.POST.get('title'),
            'category': request.POST.get('category'),
            'content': request.POST.get('content'),
            'image': request.POST.get('image'),
            'article_tags': request.POST.get('tags').split(','),
            'status': 'pending',
        }
        article_collection.update_one(
            {'_id': ObjectId(article_id)},
            {'$set': updated_data}
        )
        return redirect('article_detail', article_id)
    return render(request, 'article/edit_article.html', {'article': article})

@login_required
def user_delete_article(request, article_id):
    article = article_collection.find_one({'_id': ObjectId(article_id)})
    if article['author'] == request.user.username:
        article_collection.delete_one({'_id': ObjectId(article_id)})
    return redirect('article')

@moderator_required
def moderation_dashboard(request):
    pending_article = list(
        article_collection.find({'status': 'pending'}).sort('created_at', -1)
    )
    return render(request, 'article/moderation_dashboard.html', {'pending_article': pending_article})

@moderator_required
def approve_article(request, article_id):
    article_collection.update_one(
        {'_id': ObjectId(article_id)},
        {
            '$set': {
                'status': 'approved',
                'approved_by': request.user.username,
                'approver_post': request.user.approver_post,
            }
        }
    )
    return redirect('moderation_dashboard')

@moderator_required
def reject_article(request, article_id):
    article_collection.update_one(
        {'_id': ObjectId(article_id)},
        {
            '$set': {
                'status': 'rejected'
            }
        }
    )
    return redirect('moderation_dashboard')

@login_required
def toggle_bookmark(request, article_id):
    existing = bookmarks_collection.find_one({
        'article_id': article_id,
        'username': request.user.username
    })
    if existing:
        bookmarks_collection.delete_one({'_id': existing['_id']})
    else:
        bookmarks_collection.insert_one({
            'article_id': article_id,
            'username': request.user.username
        })
    return redirect('article_detail', article_id=article_id)

@login_required
def toggle_like(request, article_id):
    existing = likes_collection.find_one({
        'article_id': article_id,
        'username': request.user.username
    })
    if existing:
        likes_collection.delete_one({'_id': existing['_id']})
    else:
        likes_collection.insert_one({
            'article_id': article_id,
            'username': request.user.username
        })
    return redirect('article_detail', article_id=article_id)

@login_required
def add_comment(request, article_id):
    if request.method == 'POST':
        content = request.POST.get('comment')
        comments_collection.insert_one({
            'article_id': article_id,
            'username': request.user.username,
            'comment': content,
            'created_at': datetime.now(),
        })
    return redirect('article_detail', article_id=article_id)
