from PIL import Image, ImageDraw, ImageFont

from typing import Optional


def resize_font_to_fit(
    text: str,
    *,
    font: ImageFont.FreeTypeFont,
    box: tuple[int, int],
    draw: Optional[ImageDraw.ImageDraw] = None,
    image: Optional[Image.Image] = None,
) -> tuple[ImageFont.FreeTypeFont, tuple[int, int], ImageDraw.ImageDraw]:
    if (draw is None and image is None) or (draw is not None and image is not None):
        raise ValueError('Must give either `draw` or `image` (and not both).')
    draw = draw if draw is not None else ImageDraw.Draw(image)  # type: ignore
    left, right = 1, font.size + 1
    while left < right:
        middle = (left + right) // 2
        font = font.font_variant(size=middle)
        width, height = draw.textbbox(
            xy=(0, 0),
            text=text,
            font=font,
        )[2:]
        if width <= box[0] and height <= box[1]:
            left = middle + 1
        else:
            right = middle
    return (font, (width, height), draw)
