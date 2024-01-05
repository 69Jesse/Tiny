
def add_newlines(
    message: str,
    *,
    max_line_size: int,
) -> str:
    lines: list[str] = []
    line: str = ''
    for word in message.split(' '):
        if not line:
            new = word
        else:
            new = line + ' ' + word
        if len(new) > max_line_size:
            if line:
                lines.append(line)
            if len(word) > max_line_size:
                div, mod = divmod(len(word), max_line_size)
                for _ in range(div + (mod != 0)):
                    part = word[:max_line_size]
                    lines.append(part)
                    word = word[max_line_size:]
            line = word
            continue
        line = new
    if line:
        lines.append(line)
    return '\n'.join(lines)
