from generator import Generator


def main() -> None:
    for raw_proposition in (
        '(P ⇒ P)',
        # 'a|b|c|d|e|f|g',
        # 'a=>b=>c',
        # 'a=>b=>c=>d',
    ):
        generator = Generator.from_proposition(raw_proposition)
        generator.prove()


if __name__ == '__main__':
    main()
