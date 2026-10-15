from django.contrib import admin
from django.test import Client, TestCase
from django.urls import reverse
from .models import Todo


class TodoTests(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(title="공부", content="Django 학습")

    def test_model_defaults_and_admin(self):
        self.assertFalse(self.todo.is_completed)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIn(Todo, admin.site._registry)

    def test_list_and_empty_state(self):
        self.assertContains(self.client.get(reverse("todos:list")), "공부")
        Todo.objects.all().delete()
        self.assertContains(self.client.get(reverse("todos:list")), "아직 등록된 할 일이 없어요.")

    def test_create_with_optional_content(self):
        response = self.client.post(reverse("todos:create"), {"title": "운동"})
        self.assertRedirects(response, reverse("todos:list"))
        self.assertEqual(Todo.objects.get(title="운동").content, "")

    def test_invalid_create(self):
        for title in ("", "   ", "가" * 201):
            response = self.client.post(reverse("todos:create"), {"title": title})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
        self.assertEqual(Todo.objects.count(), 1)

    def test_update_and_invalid_update(self):
        url = reverse("todos:update", args=[self.todo.pk])
        self.client.post(url, {"title": " ", "content": "변경"})
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "공부")
        response = self.client.post(url, {"title": "복습", "is_completed": "on"})
        self.assertRedirects(response, reverse("todos:list"))
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "복습")
        self.assertTrue(self.todo.is_completed)

    def test_toggle_post_only_and_completed_style(self):
        url = reverse("todos:toggle", args=[self.todo.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        for expected in (True, False):
            self.client.post(url)
            self.todo.refresh_from_db()
            self.assertEqual(self.todo.is_completed, expected)
            if expected:
                self.assertContains(self.client.get(reverse("todos:list")), 'class="todo completed"')

    def test_delete_confirmation_then_post(self):
        url = reverse("todos:delete", args=[self.todo.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Todo.objects.filter(pk=self.todo.pk).exists())
        self.assertRedirects(self.client.post(url), reverse("todos:list"))
        self.assertFalse(Todo.objects.exists())

    def test_missing_objects(self):
        for name in ("update", "delete", "toggle"):
            self.assertEqual(self.client.post(reverse(f"todos:{name}", args=[999])).status_code, 404)

    def test_csrf_and_escape(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse("todos:create"), {"title": "test"}).status_code, 403)
        Todo.objects.create(title="<script>alert(1)</script>")
        response = self.client.get(reverse("todos:list"))
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_form_pages_and_admin_login(self):
        for url in (reverse("todos:create"), reverse("todos:update", args=[self.todo.pk]), "/admin/login/"):
            self.assertEqual(self.client.get(url).status_code, 200)
