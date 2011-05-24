from django.conf.urls.defaults import patterns
from django.db import models
from django.http import HttpResponse
from django.test import TestCase
from django.contrib.auth.models import User
from echelon.fields import CurrentUserField
from echelon.middleware import EchelonMiddleware


class TestModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creator = CurrentUserField(add_only=True,
                               blank=True,
                               null=True,
                               related_name="tests_created")


def test_view(request):
    user = EchelonMiddleware.get_user()
    return HttpResponse(user and user.username or u"")


class EchelonTestCase(TestCase):
    urls = patterns('',
        (r"^test-view/", test_view, {}, "test-view"),
    )

    def setUp(self):
        User.objects.create_user("test", "test@example.com", "test")

    def test_echelon_middleware(self):
        response = self.client.get("/test-view/")
        self.assertEqual(response.content, u"")
        self.client.login(username="test", password="test")
        response = self.client.get("/test-view/")
        self.assertEqual(response.content, u"test")

    def test_current_user_field(self):
        user = User.objects.get(username="test")
        EchelonMiddleware.set_user(user)
        TestModel.objects.create(name="TEST")
        EchelonMiddleware.del_user()
        test_instance = TestModel.objects.get(name="TEST")
        self.assertEqual(test_instance.creator, user)

    def test_current_user_field_with_no_active_user(self):
        EchelonMiddleware.del_user()
        TestModel.objects.create(name="TEST")
        test_instance = TestModel.objects.get(name="TEST")
        self.assertEqual(test_instance.creator, None)
