# PDF Document Analyzer

A command-line tool for AI-powered PDF document analysis.

## Development with OpenAI Playground

Before implementing new features or modifying existing ones, use the OpenAI playground (platform.openai.com/playground) to test and refine your prompts:

### Text Analysis Testing
1. Visit the OpenAI playground
2. Select model: gpt-4o
3. Configure JSON mode if needed
4. Use the system prompt from `ai_interface.py`
5. Test with sample PDF text
6. Verify the response format and quality

### Image Analysis Testing
1. Use the playground's image upload feature
2. Select model: gpt-4o
3. Use the image analysis prompt
4. Test with various image types
5. Verify descriptive responses

### Query Testing
1. Prepare sample document context
2. Use the system prompt for querying
3. Test various query types
4. Verify response relevance and accuracy

## Configuration

Copy `.env.example` to `.env` and set your configuration:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here

# Logging Configuration
LOG_LEVEL=INFO

# PDF Processing Configuration
MAX_PDF_SIZE_MB=10
ALLOW_IMAGES=true
```

## Development

### Running Tests
```bash
python -m unittest discover tests -v
```

Tests use a mock OpenAI client to avoid API costs during development.

### Adding New Features
1. Test prompts in the OpenAI playground
2. Update mock responses in `tests/mock_openai.py`
3. Implement the feature
4. Add tests
5. Verify with real API (optional)
