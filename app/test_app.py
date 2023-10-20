import unittest
from app import app, db
from models import Hero, Power, HeroPower

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to your API', response.data)

    def test_get_heroes(self):
        response = self.app.get('/heroes')
        self.assertEqual(response.status_code, 200)
        # Customize the assertions based on your expected response data.

    def test_get_hero_by_id(self):
        hero = Hero(name='Superman')
        db.session.add(hero)
        db.session.commit()

        response = self.app.get(f'/heroes/{hero.id}')
        self.assertEqual(response.status_code, 200)
        # Customize the assertions based on your expected response data.

    def test_get_powers(self):
        response = self.app.get('/powers')
        self.assertEqual(response.status_code, 200)
        # Customize the assertions based on your expected response data.

    def test_get_power_by_id(self):
        power = Power(description='Flight')
        db.session.add(power)
        db.session.commit()

        response = self.app.get(f'/powers/{power.id}')
        self.assertEqual(response.status_code, 200)
        # Customize the assertions based on your expected response data.

    def test_create_hero_power(self):
        hero = Hero(name='Batman')
        power = Power(description='Intelligence')
        db.session.add(hero)
        db.session.add(power)
        db.session.commit()

        data = {
            'strength': 80,
            'power_id': power.id,
            'hero_id': hero.id
        }

        response = self.app.post('/hero_powers', json=data)
        self.assertEqual(response.status_code, 200)
        # Customize the assertions based on your expected response data.

if __name__ == '__main__':
    unittest.main()
