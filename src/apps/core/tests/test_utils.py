from django.contrib.auth.models import User
from django.test import TestCase

from friendship.models import Friend, FriendshipRequest

from apps.core.utils import get_friendship


credentials = [
    {
        "username": "testuser1",
        "email": "testuser1@free.fr",
        "password": "1X<ISRUkw+tuK"
    },
    {
        "username": "testuser2",
        "email": "testuser2@free.fr",
        "password": "adadfgfdsgfd"
    },
    {
        "username": "testuser3",
        "email": "testuser3@free.fr",
        "password": "jpoqjepwq"
    }
]


class GetFriendshipTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        self.test_user3 = User.objects.create_user(**credentials[2])
        # Create users.
        for user in [self.test_user1, self.test_user2, self.test_user3]:
            user.save()
        # Create friendship.
        self.client.post(
            "/login/",
            {
                "email": credentials[0]["email"],
                "password": credentials[0]["password"]
            }
        )

    def test_friendship_request_sent_presents(self):
        # Create friendships.
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        Friend.objects.add_friend(self.test_user1, self.test_user3)
        friendship = get_friendship(self.test_user1)
        self.assertEqual(len(friendship["friendship_request_sent"]), 2)

    def test_friendship_friends(self):
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        Friend.objects.add_friend(self.test_user1, self.test_user3)
        FriendshipRequest.objects.get(
            from_user=self.test_user1, to_user=self.test_user2
        ).accept()
        FriendshipRequest.objects.get(
            from_user=self.test_user1, to_user=self.test_user3
        ).accept()
        friendship = get_friendship(self.test_user1)
        self.assertEqual(len(friendship["friends"]), 2)

    def test_friendship_asked(self):
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        Friend.objects.add_friend(self.test_user1, self.test_user3)
        friendship_user2 = get_friendship(self.test_user2)
        friendship_user3 = get_friendship(self.test_user3)
        self.assertEqual(len(friendship_user2["friendship"]), 1)
        self.assertEqual(len(friendship_user3["friendship"]), 1)

    def test_friendship_refused(self):
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        Friend.objects.add_friend(self.test_user1, self.test_user3)
        FriendshipRequest.objects.get(to_user=self.test_user3).delete()
        friendship_user2 = get_friendship(self.test_user2)
        friendship_user3 = get_friendship(self.test_user3)
        self.assertEqual(len(friendship_user2["friendship"]), 1)
        self.assertEqual(len(friendship_user3["friendship"]), 0)

    def test_friendship_canceled(self):
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        FriendshipRequest.objects.get(
            from_user=self.test_user1, to_user=self.test_user2
        ).accept()
        Friend.objects.remove_friend(self.test_user1, self.test_user2)
        friendship = get_friendship(self.test_user1)
        self.assertEqual(len(friendship["friendship"]), 0)
