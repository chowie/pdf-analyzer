import io
import base64
from PIL import Image
from PyPDF2 import PdfReader
import logging

def extract_text_from_page(page):
    """Extract text content from a PDF page."""
    try:
        return page.extract_text()
    except Exception as e:
        logging.error(f"Error extracting text: {str(e)}")
        return ""

def extract_images_from_page(page):
    """Extract images from a PDF page and convert them to base64."""
    images = []
    try:
        for image_file_object in page.images:
            try:
                image_bytes = image_file_object.data
                image = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if necessary
                if image.mode in ('RGBA', 'P'):
                    image = image.convert('RGB')
                
                # Convert to base64
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                images.append(img_str)
            except Exception as e:
                logging.error(f"Error processing image: {str(e)}")
                continue
    except Exception as e:
        logging.error(f"Error extracting images: {str(e)}")
    return images

def extract_pdf_content(file_path):
    """Extract both text and images from a PDF file."""
    content = {
        'text': [],
        'images': [],
        'metadata': {}
    }

    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)

            # Extract metadata - handle None case
            metadata = pdf.metadata or {}
            content['metadata'] = {
                'pages': len(pdf.pages),
                'title': metadata.get('/Title', ''),
                'author': metadata.get('/Author', ''),
                'subject': metadata.get('/Subject', '')
            }

            # Process each page
            for page in pdf.pages:
                # Extract text
                text = extract_text_from_page(page)
                content['text'].append(text)

                # Extract images
                images = extract_images_from_page(page)
                content['images'].extend(images)

        return content
    except Exception as e:
        raise Exception(f"Failed to process PDF: {str(e)}")