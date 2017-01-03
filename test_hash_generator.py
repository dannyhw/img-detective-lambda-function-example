import unittest
import aws_lambda_function
import json


class TestHashGenerator(unittest.TestCase):
    EVENT = {}
    CONTEXT = None

    def setUp(self):
        # fix up json file with bucket name valid for you
        with open('test-s3-event.json') as data_file:
            self.EVENT = json.load(data_file)

    def tearDown(self):
        None

    def test_lambda_s3_event(self):
        aws_lambda_function.lambda_handler(self.EVENT, self.CONTEXT)


if __name__ == '__main__':
    unittest.main()
