import logging
from rich.console import Console

console = Console()

def setup_logging(verbose):
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_error(message):
    """Log error message and display it to the console."""
    logging.error(message)
    console.print(f"[bold red]Error:[/bold red] {message}")
