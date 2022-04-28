import unittest
import hashlib
import datetime
from utils import cases
from store import Store
import api


class MockStore(Store):
    def get(self, key):
        raise Exception('Не удалось получить данные из хранилища')


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store = Store()

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    @cases([])
    def test_empty_request(self):
        _, code = self.get_response({})
        self.assertEqual(api.INVALID_REQUEST, code)

    def set_valid_auth(self, request):
        if request.get("login") == api.ADMIN_LOGIN:
            msg = (datetime.datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT).encode()
            request["token"] = hashlib.sha512(msg).hexdigest()
        else:
            msg = request.get("account", "") + request.get("login", "") + api.SALT
            request["token"] = hashlib.sha512(msg.encode()).hexdigest()

    @cases([
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000",
         "first_name": "a", "last_name": "b"},
    ])
    def test_score_ok_storage(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}

        test_store = Store()
        score = 5.0
        test_store.cache_set('uid:dceedd618e2a233dfdaf80d99d6c3452', score, 60 * 60)

        self.set_valid_auth(request)
        response, code = self.get_response(request)
        score_ = response.get("score")
        self.assertEqual(float(score_), score)

    @cases([
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000",
         "first_name": "a", "last_name": "b"},
    ])
    def test_score_invalid_storage(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.store = MockStore()
        score = 5.0

        self.set_valid_auth(request)
        response, code = self.get_response(request)
        score_ = response.get("score")
        self.assertEqual(float(score_), score)

    @cases([
        {"client_ids": [1, 2], "date": "19.07.2017"},
    ])
    def test_interests_invalid_storage(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}

        self.store = MockStore()

        self.set_valid_auth(request)
        with self.assertRaises(Exception):
            self.get_response(request)


if __name__ == "__main__":
    unittest.main()
