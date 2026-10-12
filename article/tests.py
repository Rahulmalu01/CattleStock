from unittest.mock import patch

from bson import ObjectId
from django.http import Http404
from django.test import RequestFactory, SimpleTestCase

from .views import _ensure_article_text_index, article_detail


class ArticleLookupTests(SimpleTestCase):
    def setUp(self):
        self.request = RequestFactory().get('/article/')
        _ensure_article_text_index.cache_clear()

    def tearDown(self):
        _ensure_article_text_index.cache_clear()

    def test_invalid_article_id_returns_not_found(self):
        with self.assertRaises(Http404):
            article_detail(self.request, 'not-an-object-id')

    @patch('article.views.article_collection.find_one', return_value=None)
    def test_missing_article_returns_not_found(self, find_one):
        with self.assertRaises(Http404):
            article_detail(self.request, str(ObjectId()))

        find_one.assert_called_once()

    @patch('article.views.article_collection.create_index')
    def test_text_index_is_created_once_when_search_is_used(self, create_index):
        _ensure_article_text_index()
        _ensure_article_text_index()

        create_index.assert_called_once()
