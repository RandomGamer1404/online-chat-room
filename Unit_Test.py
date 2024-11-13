import unittest
from main import app, generate_unique_code, rooms

class TestChatRoom(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test for generate_unique_code
    def test_generate_unique_code(self):
        code1 = generate_unique_code(4)
        code2 = generate_unique_code(4)
        self.assertNotEqual(code1, code2)  # Unique check
        self.assertEqual(len(code1), 4)   # Length check

    # Test for home route
    def test_home_route_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pick a name!', response.data)  # Check error message

    def test_home_route_post(self):
        response = self.app.post('/', data=dict(name="TestUser", create="true"))
        self.assertEqual(response.status_code, 302)  # Redirect to /room

    # Test for room route
    def test_room_route_valid(self):
        with self.app.session_transaction() as session:
            session['room'] = "TEST"
            session['name'] = "TestUser"
            rooms["TEST"] = {"members": 1, "messages": []}

        response = self.app.get('/room')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TEST', response.data)  # Check room code in response

    def test_room_route_invalid(self):
        response = self.app.get('/room')
        self.assertEqual(response.status_code, 302)  # Redirect to home

if __name__ == '__main__':
    unittest.main()
