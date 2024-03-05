from pathlib import Path
from import_sorter import sort_imports


def main() -> None:
    # with Path(r'example/parse_me.py').open('r', encoding='utf-8') as f:
    #     raw = f.read()
    # raw = sort_imports(raw)
    # with Path('example/parsed.py').open('w', encoding='utf-8') as f:
    #     f.write(raw)

    ignoring_folders: list[str] = [
        'legacy',
    ]

    p = r'C:\Aliases\scripts'
    for path in Path(p).rglob('*.py'):
        if any(
            path.parts[i] == folder
            for i in range(len(path.parts))
            for folder in ignoring_folders
        ):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            raw = f.read()
        raw = sort_imports(raw)
        if not raw.endswith('\n'):
            raw += '\n'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(raw)


if __name__ == '__main__':
    main()
