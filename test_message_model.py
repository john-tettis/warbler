"""Message model tests."""

import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class MessageModelTestCase(TestCase):
    """Test the message model"""

    def setUp(self):
        """Clear data and give test info"""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

    def test_message_model(self):
        """Does the basic model work?"""

        user = User.signup(username='test',password='test_password',email="test@test.com",image_url=None)
        db.session.add(user)
        db.session.commit()

        message = Message(text='this is a test message',user_id=user.id)
        db.session.add(message)
        db.session.commit()
        self.assertEqual(message.user,user)
        self.assertEqual(message.text,'this is a test message')