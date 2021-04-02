"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY, do_logout

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """test app view functions"""
    def setUp(self):
        """Clear data and give test info"""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        db.session.commit()

    def test_home_(self):
        """Does the home route return the home page with logged in user"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get('/')
            self.assertEqual(resp.status_code,200)
            
    def test_signup(self):
        """Can the user signup properly"""

        with self.client as c:
            data={
                'username':'test_signup',
                'password':'123456',
                'email':'test@email.com'
                }
            resp = c.post('/signup',data=data)
            self.assertEqual(resp.status_code,302)
            user = User.authenticate(username='test_signup', password='123456')
            self.assertTrue(user != False)
    
    def test_login(self):
        """Can the user login properly"""
        # do_logout()
        with self.client as c:
            data={
                'username':'test_user',
                'password':'testuser'
            }
            resp = c.post('/login',data=data)
            self.assertEqual(resp.status_code,200)
            self.assertIn(b'testuser',resp.data.lower())

    def test_logout(self):
        """CAn the user logout properly"""
        with self.client as c:
            resp = c.get('/logout', follow_redirects=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn(b'new to warbler?',resp.data.lower())
    
    def test_delete_user(self):
        """Can the user delete their account"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post('/users/delete')

            self.assertEqual(resp.status_code, 302)
            self.assertIsNone(User.query.get(self.testuser.id))


    

    

  
