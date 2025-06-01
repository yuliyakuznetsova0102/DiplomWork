from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Ad, Comment


class AdTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123',
            role='admin'
        )
        self.ad = Ad.objects.create(
            title='Test Ad',
            price=100,
            description='Test description',
            author=self.user
        )
        self.comment = Comment.objects.create(
            text='Test comment',
            author=self.user,
            ad=self.ad
        )

    def test_create_ad(self):
        url = reverse('ad-list')
        data = {
            'title': 'New Ad',
            'price': 200,
            'description': 'New description'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)
        self.assertEqual(Ad.objects.last().title, 'New Ad')

    def test_update_ad_by_owner(self):
        url = reverse('ad-detail', args=[self.ad.id])
        data = {'title': 'Updated Ad', 'price': 150, 'description': 'Updated description'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Ad')

    def test_update_ad_by_admin(self):
        url = reverse('ad-detail', args=[self.ad.id])
        data = {'title': 'Admin Updated', 'price': 150, 'description': 'Admin updated description'}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Admin Updated')

    def test_delete_ad_by_non_owner(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            first_name='Other',
            last_name='User',
            password='otherpass123'
        )
        url = reverse('ad-detail', args=[self.ad.id])
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_ads(self):
        Ad.objects.create(
            title='Another Ad',
            price=300,
            description='Another description',
            author=self.user
        )
        url = reverse('ad-list') + '?title=Another'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Another Ad')


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123',
            role='admin'
        )
        self.ad = Ad.objects.create(
            title='Test Ad',
            price=100,
            description='Test description',
            author=self.user
        )
        self.comment = Comment.objects.create(
            text='Test comment',
            author=self.user,
            ad=self.ad
        )

    def test_create_comment(self):
        url = reverse('comment-list', args=[self.ad.id])
        data = {'text': 'New comment'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.last().text, 'New comment')

    def test_update_comment_by_owner(self):
        url = reverse('comment-detail', args=[self.ad.id, self.comment.id])
        data = {'text': 'Updated comment'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Updated comment')

    def test_delete_comment_by_admin(self):
        url = reverse('comment-detail', args=[self.ad.id, self.comment.id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)