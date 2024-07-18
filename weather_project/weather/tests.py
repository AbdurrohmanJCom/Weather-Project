from django.test import TestCase
from django.contrib.auth.models import User
from .models import SearchHistory

class WeatherTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_search_history_creation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/api/weather/', {'city': 'London'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SearchHistory.objects.filter(user=self.user, city='London').exists())
