"""Allocate private company/role records, revisions, and reviewed PDF deliveries."""

import argparse
import json
import re
from pathlib import Path, PureWindowsPath


def label(value: str) -> str:
    if not value.strip() or PureWindowsPath(value).drive or '..' in re.split(r'[/\\]', value):
        raise ValueError('Supply a company or role label, not a path')
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', value).strip().rstrip('. ')[:80].rstrip('. ')
    if not name or name == '.':
        raise ValueError('A nonempty company or role label is required')
    if re.fullmatch(r'CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³]', name.split('.')[0], re.I):
        name = '_' + name
    return name


def contained(path: Path, root: Path) -> Path:
    path = path.absolute()
    if path.resolve() != path or not path.is_relative_to(root.resolve()):
        raise ValueError(f'Redirected path or destination outside output directory: {path}')
    return path


def fresh(parent: Path, name: str, separator: str = '-') -> Path:
    index = 1
    while True:
        target = contained(parent / (name if index == 1 else f'{name}{separator}{index}'), parent)
        try:
            target.mkdir()
            return target
        except FileExistsError:
            index += 1


def allocate(output: Path, company: str, role: str) -> Path:
    company_name, role_name = label(company), label(role)
    output = output.absolute()
    contained(output, output)
    output.mkdir(parents=True, exist_ok=True)
    index = 1
    while True:
        folder = contained(output / (company_name if index == 1 else f'{company_name}-{index}'), output)
        try:
            folder.mkdir()
            break
        except FileExistsError:
            if folder.is_dir():
                records = [contained(p, output) for p in folder.glob('*/supporting/application.json')]
                if any(json.loads(p.read_text(encoding='utf-8')).get('company') == company.strip() for p in records):
                    break
            index += 1
    root = fresh(folder, role_name)
    supporting = root / 'supporting'
    supporting.mkdir()
    record = {'root': str(root), 'company': company.strip(), 'role': role.strip()}
    (supporting / 'application.json').write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
    return root


def resume(root: Path) -> Path:
    root = root.absolute()
    contained(root, root)
    if (root / 'supporting').exists():
        contained(root / 'supporting', root)
        record_path = contained(root / 'supporting/application.json', root)
        if not record_path.is_file():
            raise ValueError('Missing supporting application record; recover the saved inputs before resuming')
        record = json.loads(record_path.read_text(encoding='utf-8'))
        if record.get('root') != str(root):
            raise ValueError('Application root differs from the recorded root')
    elif not (root / 'job.md').is_file():
        raise ValueError('Missing supporting state; recover the saved inputs before resuming')
    return root


def revision(root: Path, language: str) -> Path:
    if language not in {'en', 'fr'}:
        raise ValueError('Language must be en or fr')
    root = resume(root)
    if not (root / 'supporting').is_dir():
        raise ValueError('Legacy application: retain its existing revision layout')
    parent = contained(root / 'supporting/revisions', root)
    parent.mkdir(exist_ok=True)
    index = 1
    while True:
        target = contained(parent / f'{language}-v{index}', root)
        try:
            target.mkdir()
            return target
        except FileExistsError:
            index += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    new = commands.add_parser('allocate')
    new.add_argument('output', type=Path)
    new.add_argument('company')
    new.add_argument('role')
    continuing = commands.add_parser('resume')
    continuing.add_argument('root', type=Path)
    rev = commands.add_parser('revision')
    rev.add_argument('root', type=Path)
    rev.add_argument('language', choices=('en', 'fr'))
    args = parser.parse_args()
    try:
        if args.command == 'allocate':
            print(allocate(args.output, args.company, args.role))
        elif args.command == 'resume':
            print(resume(args.root))
        else:
            print(revision(args.root, args.language))
    except (OSError, ValueError) as error:
        parser.exit(1, f'Artifact storage failed: {error}\n')


if __name__ == '__main__':
    main()
