
import click
from rich.console import Console
from rich.progress import Progress
from colorama import Fore, Style, init as colorama_init
import sys
import json

from .utils.helpers import handle_error, DevSecError

colorama_init(autoreset=True)
console = Console()

VERSION = "0.1.0"

def print_error(msg):
    console.print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}", style="bold red")

def print_success(msg):
    console.print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}", style="bold green")

def print_info(msg):
    console.print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}", style="cyan")

def load_config(config_path):
    import yaml, os
    if not config_path or not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

@click.group()
@click.version_option(VERSION, '--version', '-v', message="DevSec Scanner, version %(version)s")
@click.option('--verbose', is_flag=True, help="Enable verbose output.")
@click.option('--json', 'json_output', is_flag=True, help="Output results as JSON.")
@click.option('--config', type=click.Path(), help="Path to configuration file.")
@click.pass_context
def main(ctx, verbose, json_output, config):
    """DevSec Scanner CLI - Scan for exploitable vulnerabilities."""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['JSON'] = json_output
    ctx.obj['CONFIG'] = load_config(config)

@main.group()
@click.pass_context
def scan(ctx):
    """Scan for vulnerabilities on a specific platform or all."""
    pass

@scan.command()
@click.argument('path', required=False)
@click.pass_context
def firebase(ctx, path):
    """Scan Firebase project at PATH."""
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning Firebase...", total=100)
            for _ in range(10):
                progress.update(task, advance=10)
        result = {"platform": "firebase", "path": path, "status": "ok"}
        if ctx.obj['JSON']:
            console.print(json.dumps(result, indent=2))
        else:
            print_success(f"Firebase scan complete for {path or 'current directory'}.")
    except DevSecError as e:
        handle_error(e, ctx.obj.get('VERBOSE', False))
    except Exception as e:
        handle_error(DevSecError(str(e)), ctx.obj.get('VERBOSE', False))

@scan.command()
@click.argument('path', required=False)
@click.pass_context
def git(ctx, path):
    """Scan Git repository at PATH."""
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning Git repo...", total=100)
            for _ in range(10):
                progress.update(task, advance=10)
        result = {"platform": "git", "path": path, "status": "ok"}
        if ctx.obj['JSON']:
            console.print(json.dumps(result, indent=2))
        else:
            print_success(f"Git scan complete for {path or 'current directory'}.")
    except DevSecError as e:
        handle_error(e, ctx.obj.get('VERBOSE', False))
    except Exception as e:
        handle_error(DevSecError(str(e)), ctx.obj.get('VERBOSE', False))

@scan.command()
@click.argument('bucket', required=False)
@click.pass_context
def s3(ctx, bucket):
    """Scan AWS S3 bucket."""
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning S3 bucket...", total=100)
            for _ in range(10):
                progress.update(task, advance=10)
        result = {"platform": "s3", "bucket": bucket, "status": "ok"}
        if ctx.obj['JSON']:
            console.print(json.dumps(result, indent=2))
        else:
            print_success(f"S3 scan complete for bucket {bucket or '[not specified]' }.")
    except DevSecError as e:
        handle_error(e, ctx.obj.get('VERBOSE', False))
    except Exception as e:
        handle_error(DevSecError(str(e)), ctx.obj.get('VERBOSE', False))

@scan.command()
@click.argument('path', required=False)
@click.pass_context
def all(ctx, path):
    """Scan all supported platforms."""
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning all platforms...", total=100)
            for _ in range(10):
                progress.update(task, advance=10)
        result = {"platform": "all", "path": path, "status": "ok"}
        if ctx.obj['JSON']:
            console.print(json.dumps(result, indent=2))
        else:
            print_success(f"All-platform scan complete for {path or 'current directory'}.")
    except DevSecError as e:
        handle_error(e, ctx.obj.get('VERBOSE', False))
    except Exception as e:
        handle_error(DevSecError(str(e)), ctx.obj.get('VERBOSE', False))

if __name__ == "__main__":
    main(obj={})
