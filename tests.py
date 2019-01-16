from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='chenqq')
        u.set_password('123456')
        self.assertFalse(u.check_password('12345'))
        self.assertTrue(u.check_password('123456'))

    def test_avatar(self):
        u = User(username='chen', email='TauCrus@163.com')
        self.assertEqual(u.avatar(128),'')

    def test_follow(self):
        u1 = User(username='chenqq', email='974613056@qq.com')
        u2 = User(username='chen', email='TauCrus@163,com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'chen')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'chenqq')

if __name__ == '__main__':
    unittest.main(verbosity=2)