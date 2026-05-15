# Fix the template
with open('article/templates/article/article_list.html', 'r') as f:
    content = f.read()

# Replace article._id with article.id
content = content.replace('article._id', 'article.id')

# Write back
with open('article/templates/article/article_list.html', 'w') as f:
    f.write(content)

print('Fixed template to use article.id')
