use image::{GenericImageView, RgbImage};
use image_hasher::HasherConfig;
use std::{
    collections::{HashMap, HashSet},
    hash::Hash,
};

const TILE_SIZE: (u32, u32) = (1, 1);
const OPTION_SIZE: (u8, u8) = {
    let n = 2;
    (n, n)
}; // in amount of tiles, not pixels
const WRAP_AROUND_EDGES: bool = true;
const ALLOW_ROTATIONS: bool = true;

#[derive(Clone)]
struct Tile {
    image: RgbImage,
}
impl Tile {
    fn new(image: RgbImage) -> Tile {
        return Tile { image: image };
    }
}
impl PartialEq for Tile {
    fn eq(&self, other: &Self) -> bool {
        return self.image == other.image;
    }
}

struct Pattern {
    tile: Tile,
    offset_tiles: HashMap<(i8, i8), Tile>,
    count: u32,
}
impl Pattern {
    fn new(tile: Tile, offset_tiles: HashMap<(i8, i8), Tile>) -> Pattern {
        return Pattern {
            tile: tile,
            offset_tiles: offset_tiles,
            count: 1,
        };
    }

    fn increment(&mut self) {
        self.count += 1;
    }
}
impl PartialEq for Pattern {
    fn eq(&self, other: &Self) -> bool {
        return self.tile == other.tile && self.offset_tiles == other.offset_tiles;
    }
}

struct Cell {
    x: u32,
    y: u32,
    patterns: Vec<Pattern>,
    tile: Option<Tile>,
}
impl Cell {
    fn is_collapsed(&self) -> bool {
        return self.tile.is_some();
    }
}

fn create_tiles(image: &RgbImage, tile_size: (u32, u32)) -> HashMap<(u32, u32), Tile> {
    let mut tiles = HashMap::new();
    for x in 0..image.width() / tile_size.0 {
        for y in 0..image.height() / tile_size.1 {
            let tile = Tile::new(
                image
                    .view(x * tile_size.0, y * tile_size.1, tile_size.0, tile_size.1)
                    .to_image(),
            );
            tiles.insert((x, y), tile);
        }
    }
    tiles
}

fn create_patterns(
    image: &RgbImage,
    tiles: &HashMap<(u32, u32), Tile>,
    tile_size: (u32, u32),
    option_size: (u8, u8),
    wrap_around_edges: bool,
    allow_rotations: bool, // TODO
) -> Vec<Pattern> {
    let mut patterns = Vec::new();
    for x in 0..image.width() / tile_size.0 {
        for y in 0..image.height() / tile_size.1 {
            let tile = tiles[&(x, y)].clone();
            for dx in -(option_size.0 as i8) + 1..=0 {
                for dy in -(option_size.1 as i8) + 1..=0 {
                    let mut offset_tiles = HashMap::new();
                    for ddx in 0..option_size.0 {
                        for ddy in 0..option_size.1 {
                            let (tx, ty) = (
                                (x as i32 + dx as i32 + ddx as i32),
                                (y as i32 + dy as i32 + ddy as i32),
                            );
                            if !wrap_around_edges
                                && (tx < 0 || ty < 0 || tx >= image.width() as i32 || ty >= image.height() as i32)
                            {
                                continue;
                            }
                            let (tx, ty) = (
                                tx.rem_euclid((image.width() / tile_size.0) as i32),
                                ty.rem_euclid((image.height() / tile_size.1) as i32),
                            );
                            let (tx, ty) = (
                                tx as u32,
                                ty as u32,
                            );
                            offset_tiles.insert(
                                (dx + ddx as i8, dy + ddy as i8),
                                tiles[&(tx, ty)]
                                    .clone(),
                            );
                        }
                    }
                    patterns.push(Pattern::new(tile.clone(), offset_tiles));
                }
            }
        }
    }
    patterns
}

struct Grid {}
impl Grid {
    fn from_image(
        image: &RgbImage,
        tile_size: (u32, u32),
        option_size: (u8, u8),
        wrap_around_edges: bool,
        allow_rotations: bool,
    ) -> Result<Grid, String> {
        if image.width() % tile_size.0 != 0 || image.height() % tile_size.1 != 0 {
            return Err(format!(
                "Image dimensions ({}x{}) are not divisible by the tile size ({}x{}).",
                image.width(),
                image.height(),
                tile_size.0,
                tile_size.1
            ));
        }
        if option_size.0 as u32 % tile_size.0 != 0 || option_size.1 as u32 % tile_size.1 != 0 {
            return Err(format!(
                "Option size ({}x{}) is not divisible by the tile size ({}x{}).",
                option_size.0, option_size.1, tile_size.0, tile_size.1
            ));
        }
        if option_size.0 as u32 / tile_size.0 != option_size.1 as u32 / tile_size.1 {
            return Err(format!(
                "Option size ({}x{}) does not have the same aspect ratio as the tile size ({}x{}).",
                option_size.0, option_size.1, tile_size.0, tile_size.1
            ));
        }
        let tiles = create_tiles(image, tile_size);
        let patterns = create_patterns(
            image,
            &tiles,
            tile_size,
            option_size,
            wrap_around_edges,
            allow_rotations,
        );

        return Ok(Grid {});
    }
}

fn main() {
    let hasher = HasherConfig::new().to_hasher();
    let img = image::open("input.png").unwrap().to_rgb8();
    let grid = match Grid::from_image(
        &img,
        TILE_SIZE,
        OPTION_SIZE,
        WRAP_AROUND_EDGES,
        ALLOW_ROTATIONS,
    ) {
        Ok(patterns) => patterns,
        Err(err) => {
            eprintln!("{}", err);
            return;
        }
    };
    println!("woo done");
}
