"""
AI Interface for PDF document analysis.

For development and testing:
1. Use the OpenAI playground (platform.openai.com/playground) to test and refine prompts
2. In test environments, this module uses a mock OpenAI client to avoid API costs
3. The mock client provides predictable responses for testing purposes

Production usage:
- Requires a valid OpenAI API key with sufficient quota
- Uses rate limiting and exponential backoff for API calls
"""

import os
import json
import time
import logging
import random
from openai import OpenAI, RateLimitError

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client
openai = OpenAI(api_key=OPENAI_API_KEY)

def handle_rate_limit(func):
    """Decorator to handle rate limiting with exponential backoff."""
    def wrapper(*args, **kwargs):
        max_retries = 5
        base_delay = 2  # Increased from 1 to 2 seconds
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                if attempt == max_retries - 1:
                    raise Exception(
                        "Rate limit exceeded. Please ensure your OpenAI API key "
                        "has sufficient quota and billing enabled."
                    ) from e
                delay = base_delay * (2 ** attempt) + (random.random() * 0.5)
                logging.warning(f"Rate limit hit. Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            except Exception as e:
                raise Exception(f"API Error: {str(e)}")
    return wrapper

@handle_rate_limit
def analyze_document(content):
    """Analyze document content using OpenAI API."""
    try:
        # Prepare the document content for analysis
        text_content = "\n".join(content['text'])

        # Initial text analysis
        text_analysis = analyze_text_content(text_content)

        # Process images if present
        image_analyses = []
        for image in content['images']:
            try:
                image_analysis = analyze_image(image)
                image_analyses.append(image_analysis)
            except Exception as e:
                logging.error(f"Error analyzing image: {str(e)}")
                continue

        return {
            'text_analysis': text_analysis,
            'image_analyses': image_analyses,
            'metadata_analysis': analyze_metadata(content['metadata'])
        }
    except Exception as e:
        raise Exception(f"Failed to analyze document: {str(e)}")

@handle_rate_limit
def analyze_text_content(text):
    """Analyze text content using OpenAI API."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the following document text and provide a "
                              "structured analysis including main topics, key points, "
                              "and a summary. Return the analysis in JSON format."
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Failed to analyze text content: {str(e)}")

@handle_rate_limit
def analyze_image(base64_image):
    """Analyze image content using OpenAI API."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this image and describe its content, "
                                  "context, and any relevant information it contains."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Failed to analyze image: {str(e)}")

def analyze_metadata(metadata):
    """Analyze document metadata."""
    return {
        'summary': f"Document with {metadata['pages']} pages",
        'title': metadata['title'],
        'author': metadata['author'],
        'subject': metadata['subject']
    }

@handle_rate_limit
def query_documents(query, documents):
    """Query the analyzed documents using OpenAI API."""
    try:
        # Prepare context from documents
        context = prepare_query_context(documents)

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a document analysis assistant. Use the "
                              "provided document context to answer the user's query "
                              "accurately and concisely."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuery: {query}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Failed to process query: {str(e)}")

def prepare_query_context(documents):
    """Prepare context from analyzed documents for querying."""
    context = []
    for doc in documents:
        context.append(f"Document: {doc['path'].name}")
        context.append("Text Analysis:")
        context.append(json.dumps(doc['analysis']['text_analysis'], indent=2))
        if doc['analysis']['image_analyses']:
            context.append("Image Analyses:")
            for img_analysis in doc['analysis']['image_analyses']:
                context.append(img_analysis)
    return "\n".join(context)