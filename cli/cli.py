import click

@click.group()
def cli():
    """DevSec Scanner CLI - Scan for exploitable vulnerabilities."""
    pass

@cli.command()
def scan():
    """Scan the project for vulnerabilities (stub)."""
    click.echo("[stub] Scanning for vulnerabilities...")

@cli.command()
def list_modules():
    """List available scanning modules (stub)."""
    click.echo("[stub] Available modules: firebase, s3, git, api, docker, mongodb")

if __name__ == "__main__":
    cli()
