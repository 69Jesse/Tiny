from classes import Person
import json


def main() -> None:
    with open('example.json', 'r') as file:
        data = json.load(file)

    people: list[Person] = [Person(**item) for item in data]
    for person in people:
        print(person.name, person.age, [b.name for b in person.belongings])


if __name__ == '__main__':
    main()
