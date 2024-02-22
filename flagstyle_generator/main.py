from generator import Generator


def main() -> None:
    for raw_proposition in (
        '(P ⇒ (Q ∧ R)) ⇒ ((P ⇒ Q) ∧ (Q ⇒ (P ⇒ R)))',
        # 'a|b|c|d|e|f|g',
        # 'a=>b=>c',
        # 'a=>b=>c=>d',
    ):
        generator = Generator.from_proposition(raw_proposition)
        print(generator.parser.proposition)
        generator.check(display=True)


if __name__ == '__main__':
    main()
