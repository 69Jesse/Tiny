from generator import Generator


def main() -> None:
    for raw_proposition in (
        'P -> P',
        # '(P ⇒ (Q ∧ R)) ⇒ ((P ⇒ Q) ∧ (Q ⇒ (P ⇒ R)))',
        # 'a|b|c|d|e|f|g',
        # 'a=>b=>c',
        # 'a=>b=>c=>d',
    ):
        generator = Generator.from_proposition(raw_proposition)
        generator.prove()
        print(f'\n\n{generator.flag}\n\n')


if __name__ == '__main__':
    main()
