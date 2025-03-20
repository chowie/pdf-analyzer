# AI Prompts Documentation

This document contains all the prompts and configurations used in the PDF analyzer application with the OpenAI API.

## OpenAI API Configuration

```bash
# Replace with your actual API key - NEVER commit real keys
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

## Text Analysis Prompts

### Document Content Analysis
- **Model**: gpt-4o
- **System Prompt**: 
```
Analyze the following document text and provide a structured analysis including main topics, key points, and a summary. Return the analysis in JSON format.
```
- **Expected Response Format**:
```json
{
    "main_topics": ["Topic 1", "Topic 2"],
    "key_points": ["Key point 1", "Key point 2"],
    "summary": "Comprehensive summary"
}
```

### Image Content Analysis
- **Model**: gpt-4o
- **System Prompt**:
```
Analyze this image and describe its content, context, and any relevant information it contains.
```
- **Input**: Base64 encoded image
- **Response Format**: Natural language description

### Document Querying
- **Model**: gpt-4o
- **System Prompt**:
```
You are a document analysis assistant. Use the provided document context to answer queries accurately and concisely.
```
- **Context Format**:
```
Document: [filename]
Text Analysis:
[JSON analysis data]
Image Analyses:
[Image descriptions]

Query: [User's question]
```

## Development Guidelines

### Testing New Prompts
1. Use the OpenAI playground (platform.openai.com/playground)
2. Configure appropriate settings:
   - Model selection
   - Temperature
   - Response format (JSON/text)
3. Test with sample inputs
4. Verify output structure and quality

### Security Best Practices
- Never include actual API keys in prompts
- Use placeholders for sensitive information:
  - `<YOUR_OPENAI_API_KEY>`
  - `<YOUR_AUTH_TOKEN>`
  - `<USER_EMAIL>`

### Rate Limiting
The system includes automatic rate limit handling:
- Base delay: 2 seconds
- Max retries: 5
- Jitter: 0.5 seconds random addition

## Configuration Example

```python
# Environment Variables (.env)
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
LOG_LEVEL=INFO
MAX_PDF_SIZE_MB=10
ALLOW_IMAGES=true
```

## Future Improvements
1. Add support for more document formats
2. Implement concurrent processing
3. Add export functionality for analysis results

## Model Information

Note: The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
Do not change this unless explicitly requested by the user.