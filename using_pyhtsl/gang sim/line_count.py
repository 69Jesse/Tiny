from pathlib import Path


def main() -> None:
    count = 0
    for path in Path('.').rglob('*.py'):
        with open(path, 'r', encoding='utf-8') as file:
            count += len(file.readlines())
    print(f'.py line count: {count}')


if __name__ == '__main__':
    main()
