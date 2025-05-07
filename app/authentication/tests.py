from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User

class AutenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('token_obtain_pair')
        self.register_url = reverse('register')  # Asegúrate de que esta URL existe

        self.user_data = {
            'username': "testuser",
            'email': "test@example.com",
            'password': "securepassword123"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        print("Respuesta del login:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_fallido(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': 'cotrasena',  # Contraseña incorrecta
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)

    def test_registro(self):
        response = self.client.post(self.register_url, {
            'username': 'nuevoUsuario',
            'password': 'contrasena1234',
            'email': 'nuevoUsuario@gmail.com',
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], 'nuevoUsuario')

    def test_registro_fallido(self):
        response = self.client.post(self.register_url, {
            'username': self.user_data['username'],  # Usuario ya registrado
            'password': '12',  # Contraseña demasiado corta
            'email': 'email',  # Email inválido
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
    print(User.objects.all())  # Esto debe mostrar el usuario creado
