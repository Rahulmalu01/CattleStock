# Read the views.py file
with open('article/views.py', 'r') as f:
    content = f.read()

# Replace the article_list function
old_code = """def article_list(request):
    query = request.GET.get('q')
    if query:
        article = list(
            article_collection.find({
                '\': {'\': query},
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
    })"""

new_code = """def article_list(request):
    query = request.GET.get('q')
    if query:
        articles = list(
            article_collection.find({
                '\': {'\': query},
                'status': 'approved'
            }).sort('created_at', -1)
        )
    else:
        articles = list(
            article_collection.find({'status': 'approved'}).sort('created_at', -1)
        )
    
    # Convert MongoDB _id to id for template access
    for article in articles:
        article['id'] = str(article['_id'])
    
    return render(request, 'article/article_list.html', {
        'articles': articles,
        'current_page': 'article',
    })"""

content = content.replace(old_code, new_code)

# Write back
with open('article/views.py', 'w') as f:
    f.write(content)

print('Fixed article_list view')
