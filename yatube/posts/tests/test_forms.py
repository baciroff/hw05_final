from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User, Comment


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="StasBasov")
        cls.post = Post.objects.create(author=cls.user, 
                                       text="Тестовый пост",)
        cls.comment = Comment.objects.create(
            author=cls.user,
            text="Тестовый комментарий",
        )
    def setUp(self):
        self.user = User.objects.create(username="NoName")
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {"text": "Тестовый текст"}
        response = self.authorized_client.post(reverse("posts:post_create"),
                                               data=form_data, follow=True)
        self.assertRedirects(response, reverse("posts:profile",
                             kwargs={"username": self.user.username}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
                        text=form_data.get('text')).exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        """Валидная форма изменяет запись в Post."""
        self.post = Post.objects.create(author=self.user,
                                        text="Тестовый текст",)
        self.group = Group.objects.create(title="Тестовая группа",
                                          slug="test-slug",
                                          description="Тестовое описание",)
        posts_count = Post.objects.count()
        form_data = {"text": "Изменяем текст", "group": self.group.id}
        response = self.authorized_client.post(reverse("posts:post_edit",
                                               args=({self.post.id})),
                                               data=form_data,
                                               follow=True,)
        self.assertRedirects(response, reverse("posts:post_detail",
                             kwargs={"post_id": self.post.id}))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(Post.objects.filter(text="Изменяем текст").exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_comment(self):
        """Валидная форма Комментария создает запись в Post."""
        comments_count = Comment.objects.count()
        form_data = {"text": "Тестовый коммент"}
        response = self.authorized_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("posts:post_detail",
                             kwargs={"post_id": self.post.id}))
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(Comment.objects.filter(
                        text=form_data["text"]).exists())
