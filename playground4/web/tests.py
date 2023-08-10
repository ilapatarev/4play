from django.test import TestCase
from django.contrib.auth import get_user_model

from playground4.web.forms import FieldForm, EventForm, ReviewForm, LoginForm
from playground4.web.models import Field, Reservation

User = get_user_model()


class UserModelTests(TestCase):

	def test_create_user(self):
		user = User.objects.create_user(username='marko', email='marko@marko.com', password='dadadada')
		self.assertEqual(user.username, 'marko')
		self.assertEqual(user.email, 'marko@marko.com')
		self.assertTrue(user.check_password('dadadada'))

	def test_create_user_no_username(self):
		with self.assertRaises(ValueError):
			User.objects.create_user(username='', email='marko@marko.com', password='dadadada')

	def test_create_superuser(self):
		admin_user = User.objects.create_superuser(username='aleks', email='aleks@some.com', password='aleks123')
		self.assertTrue(admin_user.is_staff)
		self.assertTrue(admin_user.is_superuser)


class FieldModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='aleks',
			email='aleks@test.com',
			password='aleks123'
		)

	def test_get_start_working_day(self):
		field = Field.objects.create(
			field_owner=self.user,
			name='Arena',
			location='Plovdiv',
			sport='Basketball',
			description='Brand new facilities',
			price_per_hour=20,
			start_working_day=2,
			start_working_hour=16,
			end_working_day=4,
			end_working_hour=20
		)
		self.assertEqual(field.get_start_working_day(), 'Tuesday')

	def test_get_end_working_day(self):
		field = Field.objects.create(
			field_owner=self.user,
			name='Arena',
			location='Plovdiv',
			sport='Basketball',
			description='Brand new facilities',
			price_per_hour=20,
			start_working_day=2,
			start_working_hour=16,
			end_working_day=4,
			end_working_hour=20
		)
		self.assertEqual(field.get_end_working_day(), 'Thursday')


class ReservationModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='aleks',
			email='aleks@some.com',
			password='dadadada'
		)

		self.field = Field.objects.create(
			field_owner=self.user,
			name='Arena',
			location='Plovdiv',
			sport='Basketball',
			description='Brand new facilities',
			price_per_hour=20,
			start_working_day=2,
			start_working_hour=16,
			end_working_day=4,
			end_working_hour=20
		)

	def test_reservation_str(self):
		reservation = Reservation.objects.create(
			user=self.user,
			field=self.field,
			reservation_date='2023-07-25',
			reservation_hour=18
		)
		expected_str = f"Reservation for {self.field.name} by {self.user.username}"
		self.assertEqual(str(reservation), expected_str)


class FieldFormTest(TestCase):
	def test_valid_form(self):
		form_data = {
			'name': 'Arena',
			'location': 'Plovdivn',
			'sport': 'Basketball',
			'description': 'Brand new facilities',
			'image_url': 'https://example.com/image.jpg',
			'start_working_day': 2,  # Tuesday
			'start_working_hour': 16,
			'end_working_day': 4,  # Thursday
			'end_working_hour': 20
		}

		form = FieldForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		form_data = {
			'name': '',
			'location': 'Plovdivn',
			'sport': 'Basketball',
			'description': 'Brand new facilities',
			'image_url': 'https://example.com/image.jpg',
			'start_working_day': 2,  # Tuesday
			'start_working_hour': 16,
			'end_working_day': 4,  # Thursday
			'end_working_hour': 20
		}

		form = FieldForm(data=form_data)
		self.assertFalse(form.is_valid())


class EventFormTest(TestCase):
	def test_valid_form(self):
		form_data = {
			'title': 'Cup race',
			'sport': 'Basketball',
			'content': 'Knock out competition',
			'image': 'https://example.com/image.jpg',
			'event_date': '2023-08-31 18:00:00'
		}

		form = EventForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		form_data = {
			'title': '',
			'sport': 'Basketball',
			'content': 'Knock out competition',
			'image': 'https://example.com/image.jpg',
			'event_date': '2023-08-31 18:00:00'
		}

		form = EventForm(data=form_data)
		self.assertFalse(form.is_valid())


class ReviewFormTest(TestCase):
	def test_valid_form(self):
		form_data = {
			'rating': 4,
			'comment': 'Average field'
		}
		form = ReviewForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		form_data = {
			'rating': 6,  # Rating should be between 1 and 5
			'comment': ''
		}
		form = ReviewForm(data=form_data)
		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 2)
		self.assertEqual(form.errors['rating'][0], 'Ensure this value is less than or equal to 5.')
		self.assertEqual(form.errors['comment'][0], 'This field is required.')


