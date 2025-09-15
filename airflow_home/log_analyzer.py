import sys
from pathlib import Path

def analyze_file(filepath):
    """
    Parses a single log file and returns:
    - count of ERROR lines
    - list of error message lines
    """
    error_count = 0
    error_lines = []

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if 'ERROR' in line:
                    error_count += 1
                    error_lines.append(line.strip())
    except Exception as e:
        print(f"Failed to read {filepath}: {e}")

    return error_count, error_lines

def analyze_logs(log_root_dir):
    """
    Recursively analyzes all .log files under a given directory.
    Prints total number of errors and their details.
    """
    total_errors = 0
    all_error_messages = []

    log_files = Path(log_root_dir).rglob('*.log')

    for file in log_files:
        count, errors = analyze_file(file)
        total_errors += count
        all_error_messages.extend(errors)

    print(f"\nTotal number of errors: {total_errors}")
    print("Here are all the errors:")
    for msg in all_error_messages:
        print(msg)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 log_analyzer.py /path/to/logs")
        sys.exit(1)

    log_dir = sys.argv[1]
    analyze_logs(log_dir)
