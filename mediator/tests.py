from django.utils import unittest
from mediator import MediaMapping


class MediaMappingTest(unittest.TestCase):
    def setUp(self):
        self.root_dir = '/home/foo/public_html'
        self.root_url = '/media/'
        self.mm = MediaMapping(self.root_dir, self.root_url)
        
    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_init(self):
        self.assertEqual(self.mm.root_dir, self.root_dir)
        self.assertEqual(self.mm.root_url, self.root_url)

    def test_to_url(self):
        pass
