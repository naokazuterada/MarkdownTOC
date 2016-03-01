from unittest import TestCase

class test_helloworld_command(TestCase):

    def test_hello_world(self):
        a = 3
        self.assertEqual(a*4, 12)
