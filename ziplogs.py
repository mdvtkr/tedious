import re
import zipfile
import argparse
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import platform

def is_valid_date(date_str):
    if platform.system() == 'Windows':
        modifier = '#'
    else:
        modifier = '-'

    available_formats = (
        '%Y%m%d',                               # yyyymmdd
        '%Y-%m-%d',                             # yyyy-mm-dd
        '%Y.%m.%d',                             # yyyy.mm.dd
        '%Y.%{0}m.%{0}d'.format(modifier),      # yyyy.m.d
        '%Y-%{0}m-%{0}d'.format(modifier),      # yyyy-m-d
        '%y%m%d',                               # yymmdd
        '%y.%{0}m.%{0}.%{0}d'.format(modifier), # yy.m.d
        '%y-%{0}m-%{0}-%{0}d'.format(modifier)  # yy.m.d
    )

    for date_format in available_formats:
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            continue
    return False

def is_in_interval(dt, interval):
    today = datetime.today()
    if interval == 'm':
        return dt.date() == today.date()
    elif interval == 'm':
        return dt.year == today.year and dt.month == today.month

def extract_date_and_name(file_name):
    patterns = [
        r'(.+)_(\d{8}|\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2})\.(.+)',
        r'(\d{8}|\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2})_(.+)\.(.+)'
    ]

    for pattern in patterns:
        match = re.match(pattern, file_name)
        if match:
            groups = match.groups()
            if is_valid_date(groups[1]):
                return groups
    return None

def group_files(input_path, interval):
    grouped_files = defaultdict(list)
    input_path = Path(input_path)

    for file in input_path.glob('**/*.*'):
        extracted = extract_date_and_name(file.name)
        if extracted:
            if is_valid_date(extracted[0]):
                date, name, extension = extracted[0], extracted[1], extracted[2]
            else:
                date, name, extension = extracted[1], extracted[0], extracted[2]
            dt = datetime.strptime(date, '%Y%m%d' if len(date) == 8 else '%Y-%m-%d' if '-' in date else '%Y.%m.%d')
            if not is_in_interval(dt, interval):
                if interval == 'm':
                    key = f"{name}_{dt.strftime('%Y%m')}"
                else:
                    key = f"{name}_{dt.strftime('%Y%m%d')}"
                grouped_files[key].append(file)

    return grouped_files

def compress_grouped_files(grouped_files, output_directory, delete_files=False, dry_run=False):
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    for group_name, files in grouped_files.items():
        output_file = output_directory / f"{group_name}.zip"
        if not dry_run:
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files:
                    zipf.write(file_path, file_path.name)
                    if delete_files:
                        try:
                            file_path.unlink()
                        except Exception as e:
                            print(f"Failed to delete {file_path.name}: {str(e)}")
        else:
            print(f"{output_file}:")
            for file_path in files:
                print(f"  {file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compress files in the given directory')
    parser.add_argument('input_directory', help='Path to the directory containing files to compress')
    parser.add_argument('-o', '--output', default='.', help='Path to the output directory')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete files after successful compression')
    parser.add_argument('-i', '--interval', choices=['d', 'm'], help='Compression interval (daily or monthly)')
    parser.add_argument('--dry-run', action='store_true', help='Dry-run mode: display files to be compressed without actually compressing them')

    args = parser.parse_args()

    grouped_files = group_files(args.input_directory, args.interval)
    compress_grouped_files(grouped_files, args.output, delete_files=args.delete, dry_run=args.dry_run)
