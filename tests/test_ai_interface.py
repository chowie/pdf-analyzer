import unittest
from unittest.mock import patch
import os
import json
from tests.mock_openai import MockOpenAI
import ai_interface

class TestAIInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up test environment variables
        os.environ.update({
            'OPENAI_API_KEY': 'test-key',
            'LOG_LEVEL': 'DEBUG',
            'MAX_PDF_SIZE_MB': '20',
            'ALLOW_IMAGES': 'true'
        })

    def setUp(self):
        # Set up mock OpenAI client before each test
        self.patcher = patch('ai_interface.get_openai_client', return_value=MockOpenAI())
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_analyze_text_content(self):
        text = "Test Document\nThis is a sample PDF document."
        result = ai_interface.analyze_text_content(text)
        self.assertIsInstance(result, dict)
        self.assertIn('main_topics', result)
        self.assertIn('key_points', result)
        self.assertIn('summary', result)

    def test_analyze_image(self):
        image_data = "base64_encoded_image_data"
        result = ai_interface.analyze_image(image_data)
        self.assertIsInstance(result, str)
        self.assertIn('test image', result.lower())

    def test_query_documents(self):
        docs = [{
            'path': type('MockPath', (), {'name': 'test.pdf'})(),
            'analysis': {
                'text_analysis': {'summary': 'Test document'},
                'image_analyses': []
            }
        }]
        result = ai_interface.query_documents("What is this document about?", docs)
        self.assertIsInstance(result, str)
        self.assertIn('test document', result.lower())

if __name__ == '__main__':
    unittest.main()