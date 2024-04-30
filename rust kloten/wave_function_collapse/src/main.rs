use image::DynamicImage;
use image_hasher::HasherConfig;
use std::collections::{HashMap, HashSet};

const TILE_SIZE: (u32, u32) = (1, 1);
const OPTION_SIZE: (u8, u8) = (2, 2);  // in amount of tiles, not pixels
const ALLOW_ROTATIONS: bool = true;
const WRAP_AROUND_EDGES: bool = true;

struct Tile {
    image: DynamicImage,
}
impl Tile {
    fn new(image: DynamicImage) -> Tile {
        return Tile { image: image };
    }
}
impl std::hash::Hash for Tile {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        let hasher = HasherConfig::new().to_hasher();
        let hash = hasher.hash_image(&self.image);
        hash.hash(state);
    }
}
impl PartialEq for Tile {
    fn eq(&self, other: &Self) -> bool {
        return self.image == other.image;
    }
}
impl Eq for Tile {}

struct Pattern {
    tile: &'static Tile,
    offset_tiles: HashMap<(i8, i8), &'static Tile>,
    count: u32,
}
impl Pattern {
    fn new(tile: &'static Tile, offset_tiles: HashMap<(i8, i8), &'static Tile>) -> Pattern {
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
    patterns: HashSet<Pattern>,
    tile: Option<Tile>,
}
impl Cell {
    fn is_collapsed(&self) -> bool {
        return self.tile.is_some();
    }
}

fn create_patterns(
    image: DynamicImage,
    tile_size: (u32, u32),
    option_size: (u8, u8),
    allow_rotations: bool,
    wrap_around_edges: bool,
) -> Result<HashSet<Pattern>, String> {
    return Ok(HashSet::new());
}

struct Grid {}
impl Grid {
    fn from_image(
        image: DynamicImage,
        tile_size: (u32, u32),
        option_size: (u8, u8),
        allow_rotations: bool,
        wrap_around_edges: bool,
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
        let patterns = create_patterns(
            image,
            tile_size,
            option_size,
            allow_rotations,
            wrap_around_edges,
        )?;
    
        return Ok(Grid {});
    }
}

fn main() {
    let hasher = HasherConfig::new().to_hasher();
    let img = image::open("input.png").unwrap();
    let grid = match Grid::from_image(
        img,
        TILE_SIZE,
        OPTION_SIZE,
        ALLOW_ROTATIONS,
        WRAP_AROUND_EDGES,
    ) {
        Ok(patterns) => patterns,
        Err(err) => {
            eprintln!("{}", err);
            return;
        }
    };
    println!("woo done");
}
