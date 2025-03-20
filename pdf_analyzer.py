#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
import document_processor as dp
import ai_interface as ai
from utils import setup_logging, log_error
import logging

console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="AI-powered PDF document analysis tool"
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=str,
        help="PDF files to analyze"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()

def validate_files(file_paths):
    valid_files = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            log_error(f"File not found: {file_path}")
            continue
        if not path.suffix.lower() == '.pdf':
            log_error(f"Not a PDF file: {file_path}")
            continue
        valid_files.append(path)
    return valid_files

def process_files(files):
    processed_docs = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for file_path in files:
            task = progress.add_task(
                f"Processing {file_path.name}...",
                total=None
            )
            try:
                content = dp.extract_pdf_content(file_path)
                analysis = ai.analyze_document(content)
                processed_docs.append({
                    'path': file_path,
                    'content': content,
                    'analysis': analysis
                })
                progress.update(task, completed=True)
            except Exception as e:
                progress.update(task, completed=True)
                log_error(f"Error processing {file_path}: {str(e)}")
    return processed_docs

def interactive_query(docs):
    while True:
        console.print("\n[bold green]Query the documents (or 'exit' to quit)[/bold green]")
        query = Prompt.ask("Enter your query")
        
        if query.lower() == 'exit':
            break
            
        with console.status("[bold blue]Processing query..."):
            try:
                response = ai.query_documents(query, docs)
                console.print(f"\n[bold cyan]Answer:[/bold cyan] {response}")
            except Exception as e:
                log_error(f"Error processing query: {str(e)}")

def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    
    console.print("[bold]PDF Document Analyzer[/bold]")
    
    valid_files = validate_files(args.files)
    if not valid_files:
        console.print("[bold red]No valid PDF files provided[/bold red]")
        sys.exit(1)
    
    console.print(f"\nProcessing {len(valid_files)} file(s)...")
    processed_docs = process_files(valid_files)
    
    if processed_docs:
        console.print("\n[bold green]Documents processed successfully![/bold green]")
        interactive_query(processed_docs)
    else:
        console.print("[bold red]No documents were successfully processed[/bold red]")

if __name__ == "__main__":
    main()
