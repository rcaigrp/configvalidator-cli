# ConfigValidator CLI

A Python CLI tool to validate configuration files against schemas.

## Goal
Validate JSON/YAML config files against a provided schema, outputting errors and suggestions.

## Acceptance Criteria
1. Recursively scan directories for .json and .yaml files.
2. Load a provided JSON schema file.
3. Validate each config file against the schema.
4. Output a formatted `rich` terminal table of validation results.
5. Support dry-run mode.
6. Export results to JSON.

## Installation
pip install rich click pyyaml

## Usage
configvalidator /path/to/configs --schema schema.json

## Project Status
- Status: Active
- Meetings Held: 0
- Meeting Budget: 5