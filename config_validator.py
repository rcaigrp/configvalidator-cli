import os
import json
import yaml
import click
from rich.console import Console
from rich.table import Table

console = Console()

def scan_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith('.json') or f.endswith('.yaml') or f.endswith('.yml'):
                files.append(os.path.join(root, f))
    return files

def validate_schema(config, schema):
    if 'required' in schema:
        for req in schema['required']:
            if req not in config:
                return False, f"Missing required key: {req}"
    return True, "Valid"

def process_configs(path, schema):
    files = scan_files(path)
    results = []
    for fpath in files:
        try:
            with open(fpath, 'r') as f:
                if fpath.endswith('.json'):
                    config = json.load(f)
                else:
                    config = yaml.safe_load(f)
            valid, msg = validate_schema(config, schema)
            results.append({'file': fpath, 'valid': valid, 'message': msg})
        except Exception as e:
            results.append({'file': fpath, 'valid': False, 'message': str(e)})
    return results

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--schema', type=click.Path(exists=True), required=True)
@click.option('--output', type=click.Path(exists=False))
@click.option('--dry-run', is_flag=True, help='Do not export results, just show table.')
def main(path, schema, output, dry_run):
    results = process_configs(path, schema)
    table = Table()
    table.add_column("File")
    table.add_column("Valid")
    table.add_column("Message")
    for r in results:
        table.add_row(r['file'], str(r['valid']), r['message'])
    console.print(table)
    
    if not dry_run and output:
        with open(output, 'w') as f:
            json.dump(results, f)

if __name__ == '__main__':
    main()