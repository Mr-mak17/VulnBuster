# secuscan.py
import os
import re
import argparse
import json
from rich import print
from rich.table import Table

# Vulnerability detection rules
def detect_sql_injection(line):
    pattern = re.compile(r"(SELECT|INSERT|UPDATE|DELETE).*['\"]\s*\+\s*.*input", re.IGNORECASE)
    return bool(pattern.search(line))

def detect_xss(line):
    pattern = re.compile(r"(<[^>]+>).*input\(", re.IGNORECASE)
    return bool(pattern.search(line))

def analyze_file(filepath):
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            for i, line in enumerate(file, start=1):
                if detect_sql_injection(line):
                    issues.append({
                        "line": i,
                        "issue": "Potential SQL Injection",
                        "severity": "High",
                        "code": line.strip()
                    })
                if detect_xss(line):
                    issues.append({
                        "line": i,
                        "issue": "Potential XSS",
                        "severity": "Medium",
                        "code": line.strip()
                    })
    except Exception as e:
        print(f"[red]Error reading file {filepath}: {e}[/red]")
    return issues

def scan_directory(path):
    results = {}
    for root, _, files in os.walk(path):
        for name in files:
            if name.endswith(".py"):
                full_path = os.path.join(root, name)
                issues = analyze_file(full_path)
                if issues:
                    results[full_path] = issues
    return results

def scan_files(files):
    results = {}
    for filepath in files:
        if os.path.isfile(filepath) and filepath.endswith(".py"):
            issues = analyze_file(filepath)
            if issues:
                results[filepath] = issues
        else:
            print(f"[yellow]Skipping invalid file: {filepath}[/yellow]")
    return results

def print_report(results):
    table = Table(title="Scan Results")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Line", style="magenta")
    table.add_column("Issue", style="red")
    table.add_column("Severity", style="yellow")
    table.add_column("Code", style="white")

    for file, issues in results.items():
        for issue in issues:
            table.add_row(
                file, str(issue['line']), issue['issue'], issue['severity'], issue['code']
            )
    print(table)

def save_json_report(results, output_file):
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"[green]Report saved to {output_file}[/green]")

def main():
    parser = argparse.ArgumentParser(description="Secure Code Review Tool")
    parser.add_argument('--path', type=str, help="Path to code directory")
    parser.add_argument('--files', nargs='+', help="List of file paths to scan")
    parser.add_argument('--output', type=str, help="Path to save JSON report")
    args = parser.parse_args()

    results = {}

    if args.files:
        print("[blue]Scanning individual files...[/blue]")
        results = scan_files(args.files)
    elif args.path:
        print(f"[blue]Scanning directory:[/blue] {args.path}")
        results = scan_directory(args.path)
    else:
        print("[red]Error: You must provide --path or --files to scan.[/red]")
        return

    if results:
        print_report(results)
        if args.output:
            save_json_report(results, args.output)
    else:
        print("[green]No vulnerabilities found.[/green]")

if __name__ == '__main__':
    main()

