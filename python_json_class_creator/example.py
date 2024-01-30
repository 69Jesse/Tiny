from create import create
import json


def main() -> None:
    with open('example.json', 'r') as file:
        data = json.load(file)
    create(name='Person', data=data)


if __name__ == '__main__':
    main()
