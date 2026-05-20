# ConfigValidator CLI

A Python CLI tool to validate configuration files against JSON schemas.

## Goal
Validate YAML/JSON config files against a provided JSON schema and report findings.

## Acceptance Criteria
1. Scan specified directory recursively.
2. Parse YAML and JSON configuration files.
3. Validate configurations against a JSON schema.
4. Output a formatted rich terminal table with findings.
5. Support dry-run mode.
6. Export findings to JSON.

## Installation
pip install click rich pyyaml jsonschema

## Usage
config-validator /path/to/configs /path/to/schema.json --dry-run

## Project Status
- Status: Active
- Meetings Held: 2
- Meeting Budget: 5
- All acceptance criteria met. Tests passed.
