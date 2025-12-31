from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from ..models import *

class PostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='sweetdevil'
        )

        self.post = Post.objects.create(
            title = 'Manchester is Red',
            subtitle = 'We might win this season',
            author = self.user,
            body = 'We are the biggest club in the world and we will continue to be that.'
        )

    def test_string_representation(self):
        post = Post(title="A sample title")
        self.assertEqual(str(post), post.title)

