
import sys
from rich.console import Console

class DevSecError(Exception):
    """Base exception for DevSec Scanner"""
    exit_code = 1
    def __init__(self, message, suggestion=None):
        super().__init__(message)
        self.suggestion = suggestion

class ConfigurationError(DevSecError):
    """Configuration-related errors"""
    exit_code = 2

class ScannerError(DevSecError):
    """Scanner-related errors"""
    exit_code = 3

class AIServiceError(DevSecError):
    """AI service-related errors"""
    exit_code = 4

def handle_error(e, verbose=False):
    console = Console()
    if isinstance(e, DevSecError):
        console.print(f"[bold red]Error:[/bold red] {e}")
        if getattr(e, 'suggestion', None):
            console.print(f"[yellow]Suggestion:[/yellow] {e.suggestion}")
        if verbose:
            import traceback
            console.print(traceback.format_exc(), style="dim")
        sys.exit(getattr(e, 'exit_code', 1))
    else:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc(), style="dim")
        sys.exit(99)
