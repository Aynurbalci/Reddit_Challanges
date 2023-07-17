import unittest
import asyncio
from reddit.app import fetch_posts
import json
from reddit.app import write_to_json

class TestFetchPosts(unittest.TestCase):

    def test_write_to_json(self):

        with open('temp.json', 'w+') as f:

            data = {'key': 'value'}
            write_to_json(data, f.name)
            f.flush()

            f.seek(0)
            result = json.load(f)
            assert result == data, 'JSON verisi yanlış'


    def test_fetch_posts(self):
        posts = asyncio.run(fetch_posts('phishing'))


        self.assertIsInstance(posts, list)


        for post in posts:
            self.assertIsInstance(post, dict)
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('author', post)
            self.assertIn('score', post)
            self.assertIn('comment_count', post)
            self.assertIn('timestamp', post)
            self.assertIn('url', post)
            self.assertIn('content', post)


if __name__ == '__main__':
    unittest.main()