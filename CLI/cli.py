#!/usr/bin/env python3
import click
import requests
import json
import os
from getpass import getpass

class ITSDCopilotCLI:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.token = None
        self.config_file = os.path.expanduser("~/.itsd_copilot_config")
        self.load_config()

    def load_config(self):
        """Load configuration and token from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.token = config.get('token')
                self.base_url = config.get('base_url', self.base_url)

    def save_config(self):
        """Save configuration to file"""
        config = {
            'token': self.token,
            'base_url': self.base_url
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def authenticate(self, username, password):
        """Authenticate user and get token"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data['access_token']
                self.save_config()
                return True
            else:
                click.echo(f"Authentication failed: {response.json().get('error', 'Unknown error')}")
                return False
        except Exception as e:
            click.echo(f"Error during authentication: {e}")
            return False

    def query_copilot(self, query):
        """Send query to copilot API"""
        if not self.token:
            click.echo("Not authenticated. Please login first.")
            return

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.base_url}/chat/query",
                json={"query": query},
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                click.echo(f"Error: {response.json().get('error', 'Unknown error')}")
                return None
        except Exception as e:
            click.echo(f"Error sending query: {e}")
            return None

@click.group()
@click.pass_context
def cli(ctx):
    """ITSD Admin Copilot CLI - Your AI assistant for Unix administration"""
    ctx.obj = ITSDCopilotCLI()

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
@click.pass_obj
def login(copilot, username, password):
    """Login to ITSD Copilot"""
    if copilot.authenticate(username, password):
        click.echo("✅ Login successful!")
    else:
        click.echo("❌ Login failed!")

@cli.command()
@click.argument('query')
@click.pass_obj
def ask(copilot, query):
    """Ask a question to the copilot"""
    result = copilot.query_copilot(query)
    if result:
        click.echo("\n🤖 Copilot Response:")
        click.echo("─" * 50)
        click.echo(result.get('response', 'No response'))
        
        if result.get('automation_suggestions'):
            click.echo("\n🔧 Automation Suggestions:")
            for suggestion in result['automation_suggestions']:
                click.echo(f"  • {suggestion['description']}")
                click.echo(f"    Command: {suggestion['command']}")
        
        click.echo("─" * 50)

@cli.command()
@click.pass_obj
def status(copilot):
    """Check system status"""
    result = copilot.query_copilot("Check system status")
    if result:
        click.echo(result.get('response', 'No response'))

@cli.command()
@click.pass_obj
def disk(copilot):
    """Check disk space"""
    result = copilot.query_copilot("How to check disk space")
    if result:
        click.echo(result.get('response', 'No response'))

if __name__ == '__main__':
    cli()