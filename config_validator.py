import os
import json
import yaml
import jsonschema
import click
from rich.console import Console
from rich.table import Table

console = Console()

def scan_directory(path):
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(('.yaml', '.yml', '.json')):
                files.append(os.path.join(root, f))
    return files

def load_config(path):
    ext = os.path.splitext(path)[1]
    with open(path, 'r') as f:
        if ext in ('.yaml', '.yml'):
            return yaml.safe_load(f)
        else:
            return json.load(f)

@click.command()
@click.argument('path')
@click.argument('schema')
@click.option('--dry-run', is_flag=True, help='Skip writing output files.')
@click.option('--export', type=click.Path(extensions=['.json']), help='Export findings to JSON.')
def main(path, schema, dry_run, export):
    schema_data = load_config(schema)
    config_files = scan_directory(path)
    findings = []
    
    for f in config_files:
        try:
            data = load_config(f)
            jsonschema.validate(data, schema_data)
            findings.append({'file': f, 'status': 'valid', 'message': 'OK'})
        except jsonschema.exceptions.ValidationError as e:
            findings.append({'file': f, 'status': 'invalid', 'message': str(e.message)})
        except Exception as e:
            findings.append({'file': f, 'status': 'error', 'message': str(e)})
            
    table = Table()
    table.add_column("File")
    table.add_column("Status")
    table.add_column("Message")
    for f in findings:
        table.add_row(f['file'], f['status'], f['message'])
    console.print(table)
    
    if export and not dry_run:
        with open(export, 'w') as ef:
            json.dump(findings, ef)
    elif export and dry_run:
        click.echo("Cannot use --export with --dry-run")

if __name__ == '__main__':
    main()
