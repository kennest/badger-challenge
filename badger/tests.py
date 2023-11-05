# Create your tests here.
from django.utils import timezone
import datetime

from django.test import TestCase, Client
from .models import User, Badge, UserBadge, Model3d


class BadgeTestCase(TestCase):
    def setUp(self):
        # Create some users, badges and models
        self.user1 = User.objects.create(username='user1', email='user1@example.com', password='@Ziwa80Ti@')

        self.user2 = User.objects.create(username='user2', email='user2@example.com', password='@Ziwa80Ti@')
        self.user3 = User.objects.create_user(username="test", password="@Ziwa80Ti@")
        self.user3.date_joined = datetime.datetime(2022, 11, 3, tzinfo=timezone.utc)
        self.user3.save()
        self.star_badge = Badge.objects.create(name='Star', description='Your model has more than 1k views',
                                               image='star.png')
        self.collector_badge = Badge.objects.create(name='Collector',
                                                    description='You have uploaded more than 5 models',
                                                    image='collector.png')
        self.model1 = Model3d.objects.create(name='model1', description='model1', image='model1.png', views=500,
                                             user=self.user1)
        self.model2 = Model3d.objects.create(name='model2', description='model2', image='model2.png', views=2000,
                                             user=self.user2)
        self.user_star_badge = UserBadge.objects.create(user=self.user2, badge=self.star_badge, date=timezone.now())
        self.user_collector_badge = UserBadge.objects.create(user=self.user1, badge=self.collector_badge,
                                                             date=timezone.now())

    def test_badge_awarding(self):
        # Test that user2 has the Star badge
        self.assertTrue(UserBadge.objects.filter(user=self.user2, badge=self.star_badge).exists())
        # Test that user1 does not have the Star badge
        self.assertFalse(UserBadge.objects.filter(user=self.user1, badge=self.star_badge).exists())
        # Test that user1 has the Collector badge after uploading 5 more models
        for i in range(3, 8):
            Model3d.objects.create(name=f'model{i}', description=f'model{i}', image=f'model{i}.png', views=0,
                                   user=self.user1)
        self.assertTrue(UserBadge.objects.filter(user=self.user1, badge=self.collector_badge).exists())
        # Test that user2 does not have the Collector badge
        self.assertFalse(UserBadge.objects.filter(user=self.user2, badge=self.collector_badge).exists())

    def test_api_access(self):
        # Test that the API returns the list of badges for each user
        client = Client()
        response1 = client.get(f'/badger/api/users/{self.user1.id}/')
        response2 = client.get(f'/badger/api/users/{self.user2.id}/')
        print(f"Response 1: {response1.data['badges']}")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.data['badges'], [{'badge': {'name': 'Collector',
                                                               'description': 'You have uploaded more than 5 models',
                                                               'image': 'http://testserver/collector.png'},
                                                     'date': '2023-11-03T07:41:46Z'}])
        self.assertEqual(response2.data['badges'], [
            {'badge': {'name': 'Star', 'description': 'Your model has more than 1k views', 'image': 'star.png'},
             'date': '2023-11-03T07:41:46Z'}])

        # Définir une méthode de test qui vérifie si un an s'est écoulé depuis la date_joined

    def test_one_year_passed_since_joined(self):
        # Obtenir la date actuelle
        today = timezone.now()
        # Calculer la différence entre la date actuelle et la date_joined
        delta = today - self.user3.date_joined
        # Vérifier si la différence est supérieure ou égale à un an (365 jours)
        self.assertGreaterEqual(delta.days, 365)
