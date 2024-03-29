from typing import Optional


def add_newlines(
	text: str,
	*,
	max_line_length: Optional[int] = None,
	max_length_ratio: float = 4 / 1,
	min_line_length: int = 20,
	max_length_margin: int = 4,
	ignore_newlines: bool = True,
) -> str:
	if ignore_newlines:
		text = text.replace('\n', ' ')
	if max_line_length is not None:
		line_length = max_line_length
	else:
		line_length = round((
			(len(text) / max_length_ratio) ** 0.5
		) * max_length_ratio)
	line_length = max(line_length, min_line_length)

	lines: list[str] = []
	for left in text.split('\n'):
		line: str = ''
		words: list[str] = left.split(' ')
		while len(words) > 0:
			before = len(line)
			word = words.pop(0).strip(' ')
			new_line = (line + ' ' + word).removeprefix(' ')
			after = len(new_line)
			before_diff, after_diff = line_length - before, line_length - after
			if after_diff > 0:
				line = new_line
				continue
			abs_after_diff = abs(after_diff)
			if abs_after_diff <= max_length_margin:
				if abs(before_diff) < abs_after_diff:
					lines.append(line)
					line = word
					continue
				lines.append(new_line)
				line = ''
				continue
			if len(line) == 0:
				left, right = word[:line_length], word[line_length:]
				lines.append(left)
				words.insert(0, right)
				line = ''
				continue
			lines.append(line)
			line = word
		if len(line) > 0:
			lines.append(line)
	return '\n'.join(lines)
