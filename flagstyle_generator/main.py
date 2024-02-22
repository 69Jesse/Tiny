from generator import Generator


for raw_proposition in (
    '(P ⇒ (Q ∧ R)) ⇒ ((P ⇒ Q) ∧ (Q ⇒ (P ⇒ R)))',
    'a|b|c|d|e|f|g',
    'a=>b=>c',
    'a=>b=>c=>d',
):
    generator = Generator.from_proposition(raw_proposition)
    generator.check(display=True)
