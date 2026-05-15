from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200)
    category = forms.CharField(max_length=100)
    tags = forms.CharField(required=False)
    image = forms.URLField(required=False)
    content = forms.CharField(widget=forms.Textarea)

