from django.test import TestCase
from .models import User  # User 모델을 임포트

class UserModelTestCase(TestCase):
    def setUp(self):
        # Given: 아래와 같은 유저 데이터를 입력 받았을 때
        self.user_data = {
            'name': 'testuser',
            'email': 'test@example.com',
            'nickname': 'testnickname',
            'password': 'testpassword1234'
        }

    def test_create_user(self):
        # When: 입력 받은 데이터를 바탕으로 유저 모델을 생성하면
        user = User.objects.create_user(**self.user_data)

        # Then: 성공적으로 생성된 유저모델은 이메일, 닉네임, 비밀번호가 입력받은 데이터와 일치해야 한다.
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.nickname, self.user_data['nickname'])
        self.assertTrue(user.check_password(self.user_data['password']))