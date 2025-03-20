"""Mock OpenAI client for testing purposes."""
import json

class MockMessage:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, message_content):
        self.message = MockMessage(message_content)

class MockCompletion:
    def __init__(self, choices):
        self.choices = [MockChoice(choice) for choice in choices]

class MockChatCompletion:
    def __init__(self):
        self.completions = {}

    def create(self, model=None, messages=None, response_format=None, **kwargs):
        """Mock create completion."""
        # Default test responses
        response_map = {
            'analyze_text': json.dumps({
                'main_topics': ['Test Document'],
                'key_points': ['Sample PDF for testing', 'Contains text and graphics'],
                'summary': 'A test document demonstrating PDF analysis capabilities'
            }),
            'analyze_image': 'A test image containing simple geometric shapes',
            'query': 'This is a test document used for analyzing PDF processing capabilities.'
        }

        # Determine which type of response to return based on the messages
        if any('analyze this image' in str(msg.get('content', '')) 
               for msg in (messages or [])):
            content = response_map['analyze_image']
        elif response_format and response_format.get('type') == 'json_object':
            content = response_map['analyze_text']
        else:
            content = response_map['query']

        return MockCompletion([content])

class MockOpenAI:
    """Mock OpenAI client for testing."""
    def __init__(self, api_key=None):
        self.chat = MockChatCompletion()