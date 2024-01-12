from pathlib import Path

from PIL import Image

from typing import (
    Optional,
    NamedTuple,
)


class Fade(NamedTuple):
    frames_duration: int
    fade_last_to_first: bool


def images_to_gif(
    image_paths: tuple[Path, ...],
    output_path: Path,
    *,
    size: tuple[int, int],
    frames_per_image: int,
    fade: Optional[Fade] = None,
    alpha_threshold: int = 128,
) -> None:
    images: list[Image.Image] = [
        Image.open(path).convert('RGBA').resize(size)
        for path in image_paths
    ]

    gif_images: list[Image.Image] = []
    for index in range(len(images)):
        current_image = images[index]
        gif_images.extend([current_image] * frames_per_image)
        if fade is None:
            continue

        next_index = (index + 1) % len(images)
        if next_index < index and not fade.fade_last_to_first:
            continue
        next_image = images[next_index]
        for i in range(fade.frames_duration):
            a = (i + 1) / (fade.frames_duration + 1)
            new_image = Image.blend(current_image, next_image, a)
            gif_images.append(new_image)

    if alpha_threshold < 255:
        for image in gif_images:
            pixels = image.load()
            for x in range(image.width):
                for y in range(image.height):
                    r, g, b, a = pixels[x, y]
                    if a < alpha_threshold:
                        pixels[x, y] = (r, g, b, 0)

    gif_images[0].save(
        output_path,
        save_all=True,
        append_images=gif_images[1:],
        duration=len(gif_images),
        loop=0,
        disposal=2,
    )
    print(f'GIF saved to {output_path}')
