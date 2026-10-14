"""Allocate private company/role records, revisions, and reviewed PDF deliveries."""

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path, PureWindowsPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.check_evidence import check


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


def publish(root: Path, rev: Path, language: str) -> Path:
    root = resume(root)
    rev = contained(rev, root / 'supporting/revisions')
    if language not in {'en', 'fr'} or not re.fullmatch(f'{language}-v[1-9][0-9]*', rev.name):
        raise ValueError('Choose the matching en or fr revision')
    pdf = contained(rev / 'render/cv.pdf', root)
    source = contained(rev / 'render/cv.yaml', root)
    review_path = contained(rev / 'review/review.json', root)
    record = json.loads(review_path.read_text(encoding='utf-8'))
    if not isinstance(record, dict) or any(record.get(key) != 'passed' for key in ('visual_review', 'factual_review', 'text_review')):
        raise ValueError('Factual, visual, and extracted-text review must all pass')
    if record.get('text_extracted') is not True or type(record.get('pages')) is not int or record['pages'] < 1 or not isinstance(record.get('review_notes'), str) or not record['review_notes'].strip():
        raise ValueError('Record page count, extracted text, and actual review notes')
    pdf_bytes = pdf.read_bytes()
    if not pdf_bytes.startswith(b'%PDF-') or record.get('pdf') != str(pdf) or record.get('pdf_sha256') != hashlib.sha256(pdf_bytes).hexdigest() or record.get('yaml_sha256') != hashlib.sha256(source.read_bytes()).hexdigest():
        raise ValueError('Reviewed PDF or YAML is missing, mismatched, or changed; review again')
    for index in range(1, record['pages'] + 1):
        if not contained(rev / f'review/page-{index}.png', root).is_file():
            raise ValueError('Missing reviewed page image')
    if not contained(rev / 'review/extracted.txt', root).read_text(encoding='utf-8').strip():
        raise ValueError('Missing extracted text')
    errors = check(source, contained(rev / 'evidence.json', root))
    if errors:
        raise ValueError('Evidence check failed: ' + '; '.join(errors))
    index = 1
    while True:
        name = f'resume-{language}' + ('' if index == 1 else f'-v{index}') + '.pdf'
        target = contained(root / name, root)
        try:
            destination = target.open('xb')
        except FileExistsError:
            index += 1
            continue
        try:
            with destination, pdf.open('rb') as original:
                shutil.copyfileobj(original, destination)
            if target.read_bytes() != pdf_bytes:
                raise ValueError('PDF changed during delivery; review again')
        except BaseException:
            target.unlink()
            raise
        return target


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
    final = commands.add_parser('publish')
    final.add_argument('root', type=Path)
    final.add_argument('revision', type=Path)
    final.add_argument('language', choices=('en', 'fr'))
    args = parser.parse_args()
    try:
        if args.command == 'allocate':
            print(allocate(args.output, args.company, args.role))
        elif args.command == 'resume':
            print(resume(args.root))
        elif args.command == 'revision':
            print(revision(args.root, args.language))
        else:
            print(publish(args.root, args.revision, args.language))
    except (OSError, ValueError) as error:
        parser.exit(1, f'Artifact storage failed: {error}\n')


if __name__ == '__main__':
    main()
