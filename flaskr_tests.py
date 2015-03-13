import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        # In python3 rv.data comes back as buffer
        # Need to add decode to convert to string
        assert 'No entries here so far' in rv.data.decode("utf-8")

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data.decode("utf-8")
        rv = self.logout()
        assert 'You were logged out' in rv.data.decode("utf-8")
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data.decode("utf-8")
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data.decode("utf-8")

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data.decode("utf-8")
        assert '&lt;Hello&gt;' in rv.data.decode("utf-8")
        assert '<strong>HTML</strong> allowed here' in rv.data.decode("utf-8")

if __name__ == '__main__':
    unittest.main()