# AI Prompts Documentation

This document contains all the prompts and configurations used in the PDF analyzer application with the OpenAI API.

## OpenAI Playground Configurations

### Text Analysis
- **Model**: gpt-4o
- **System Prompt**: 
```
Analyze the following document text and provide a structured analysis including main topics, key points, and a summary.
```
- **Response Format**: JSON
- **Example Input**: PDF document text content
- **Expected Output Format**:
```json
{
    "main_topics": ["Topic 1", "Topic 2"],
    "key_points": ["Key point 1", "Key point 2"],
    "summary": "Summary of the document"
}
```

### Image Analysis
- **Model**: gpt-4o
- **System Prompt**:
```
Analyze this image and describe its content, context, and any relevant information it contains.
```
- **Input Type**: text + image
- **Response Format**: Natural language
- **Example Input**: Base64 encoded image data
- **Expected Output**: Descriptive text analyzing the image content

### Document Queries
- **Model**: gpt-4o
- **System Prompt**:
```
You are a document analysis assistant. Use the provided document context to answer queries accurately and concisely.
```
- **Input Format**:
```
Context:
[Document content and analysis]

Query: [User's question]
```
- **Response Format**: Natural language
- **Example Query**: "What are the main topics covered in this document?"

## Development Guidelines

When testing or modifying prompts:

1. Always test new prompts in the OpenAI playground first
2. Verify response formats match the expected structure
3. Test with representative sample data
4. Monitor token usage and response times
5. Consider edge cases and potential errors

## Security Notes

- Never include actual API keys in prompts
- Use placeholders for sensitive information:
  - API Keys: `<YOUR_OPENAI_API_KEY>`
  - Auth Tokens: `<YOUR_AUTH_TOKEN>`
  - Personal Information: `<USER_NAME>`, `<USER_EMAIL>`

## Rate Limiting

The system includes automatic rate limit handling with exponential backoff:
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

## Future Prompt Improvements

Consider these areas for future prompt enhancement:
1. Add support for more document formats
2. Implement concurrent processing
3. Add export functionality for analysis results

## Model Information

Note: The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
Do not change this unless explicitly requested by the user.