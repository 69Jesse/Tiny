from pathlib import Path
from PIL import Image


MAIN_LAYER_COORDS: tuple[int, int, int, int] = (8, 8, 16, 16)
SUB_LAYER_COORDS: tuple[int, int, int, int] = (40, 8, 48, 16)


def main() -> None:
    for path in Path('./input').glob('*.png'):
        image = Image.open(path).convert('RGBA')
        head = Image.new('RGB', (8, 8), (0, 0, 0))
        head.paste(image.crop(MAIN_LAYER_COORDS), (0, 0))
        sublayer = image.crop(SUB_LAYER_COORDS)
        head.paste(sublayer, (0, 0), sublayer)
        head.save(f'../image_mosaics/input/{path.stem}.png', 'PNG')
        print(f'Converted {path}.')


if __name__ == '__main__':
    main()
