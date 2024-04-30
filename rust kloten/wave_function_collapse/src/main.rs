use image::{GenericImageView, RgbImage};
use rand;
use rand::distributions::{Distribution, WeightedIndex};
use std::collections::{HashMap, VecDeque};
use std::fmt;

const GRID_SIZE: (u32, u32) = (64, 64);
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
impl fmt::Debug for Tile {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Tile({}x{})", self.image.width(), self.image.height())
    }
}

#[derive(Clone, Debug)]
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

#[derive(Clone, Debug)]
struct Cell {
    x: u32,
    y: u32,
    patterns: Vec<Pattern>,
    tile: Option<Tile>,
}
impl Cell {
    fn new(x: u32, y: u32) -> Cell {
        return Cell {
            x: x,
            y: y,
            patterns: Vec::new(),
            tile: None,
        };
    }

    fn pattern_in_bounds(&self, pattern: &Pattern, wrap_around_edges: bool) -> bool {
        if wrap_around_edges {
            return true;
        }
        for (dx, dy) in pattern.offset_tiles.keys() {
            let (x, y) = (self.x as i32 + *dx as i32, self.y as i32 + *dy as i32);
            if x < 0 || y < 0 || x >= GRID_SIZE.0 as i32 || y >= GRID_SIZE.1 as i32 {
                return false;
            }
        }
        return true;
    }

    fn initiate_patterns(&mut self, patterns: &Vec<Pattern>, wrap_around_edges: bool) {
        assert!(self.patterns.is_empty());
        for pattern in patterns {
            if self.pattern_in_bounds(pattern, wrap_around_edges) {
                self.patterns.push(pattern.clone());
            }
        }
        assert!(!self.patterns.is_empty());
        if self.patterns.len() == 1 {
            self.collapse();
        }
    }

    fn collapse(&mut self) {
        assert!(!self.is_collapsed());
        assert!(self.patterns.len() > 0);
        let weights = self
            .patterns
            .iter()
            .map(|pattern| pattern.count)
            .collect::<Vec<u32>>();
        let mut rng = rand::thread_rng();
        let index = WeightedIndex::new(&weights).unwrap().sample(&mut rng);
        let pattern = &self.patterns[index];
        self.tile = Some(pattern.tile.clone());
    }

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
    let mut patterns: Vec<Pattern> = Vec::new();
    for x in 0..image.width() / tile_size.0 {
        for y in 0..image.height() / tile_size.1 {
            let tile = tiles[&(x, y)].clone();
            for dx in -(option_size.0 as i8) + 1..=0 {
                'new_pattern: for dy in -(option_size.1 as i8) + 1..=0 {
                    let mut offset_tiles = HashMap::new();
                    for ddx in 0..option_size.0 {
                        for ddy in 0..option_size.1 {
                            if ddx == 0 && ddy == 0 {
                                continue;
                            }
                            let (tx, ty) = (
                                (x as i32 + dx as i32 + ddx as i32),
                                (y as i32 + dy as i32 + ddy as i32),
                            );
                            if !wrap_around_edges
                                && (tx < 0
                                    || ty < 0
                                    || tx >= image.width() as i32
                                    || ty >= image.height() as i32)
                            {
                                continue 'new_pattern;
                            }
                            let (tx, ty) = (
                                tx.rem_euclid((image.width() / tile_size.0) as i32) as u32,
                                ty.rem_euclid((image.height() / tile_size.1) as i32) as u32,
                            );
                            offset_tiles
                                .insert((dx + ddx as i8, dy + ddy as i8), tiles[&(tx, ty)].clone());
                        }
                    }
                    assert!(if wrap_around_edges {
                        offset_tiles.len() == (option_size.0 * option_size.1 - 1) as usize
                    } else {
                        offset_tiles.len() <= (option_size.0 * option_size.1 - 1) as usize
                    });
                    let pattern = Pattern::new(tile.clone(), offset_tiles);
                    for existing_pattern in &mut patterns {
                        if *existing_pattern == pattern {
                            existing_pattern.increment();
                            continue 'new_pattern;
                        }
                    }
                    patterns.push(pattern);
                }
            }
        }
    }
    patterns
}

struct Grid {
    size: (u32, u32),
    cells: Vec<Cell>,
    tile_size: (u32, u32),
    option_size: (u8, u8),
}
impl Grid {
    fn new(
        size: (u32, u32),
        tile_size: (u32, u32),
        option_size: (u8, u8),
    ) -> Grid {
        let mut cells = Vec::new();
        for x in 0..size.0 {
            for y in 0..size.1 {
                cells.push(Cell::new(x, y));
            }
        }
        return Grid {
            size: size,
            cells: cells,
            tile_size: tile_size,
            option_size: option_size,
        };
    }

    fn solve(&mut self) {
        self.cells.iter_mut().for_each(|cell| {
            if !cell.is_collapsed() {
                cell.collapse();
            }
        });
    }

    fn create_image(&self) -> Result<RgbImage, String> {
        let mut image = RgbImage::new(
            self.size.0 * self.tile_size.0,
            self.size.1 * self.tile_size.1,
        );
        for cell in &self.cells {
            let tile = match &cell.tile {
                Some(tile) => tile,
                None => return Err("Not all cells have been collapsed.".to_string()),
            };
            let (x, y) = (cell.x * self.tile_size.0, cell.y * self.tile_size.1);
            for dx in 0..self.tile_size.0 {
                for dy in 0..self.tile_size.1 {
                    image.put_pixel(
                        (x + dx) as u32,
                        (y + dy) as u32,
                        tile.image.get_pixel(dx, dy).clone(),
                    );
                }
            }
        }
        Ok(image)
    }

    fn from_image(
        image: &RgbImage,
        grid_size: (u32, u32),
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
        println!("{} patterns", patterns.len());
        let mut grid = Grid::new(
            grid_size,
            tile_size,
            option_size,
        );
        grid.cells.iter_mut().for_each(|cell| {
            cell.initiate_patterns(&patterns, wrap_around_edges);
        });
        Ok(grid)
    }
}

fn main() {
    let img = image::open("input.png").unwrap().to_rgb8();
    let mut grid = match Grid::from_image(
        &img,
        GRID_SIZE,
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
    grid.solve();
    let img = match grid.create_image() {
        Ok(img) => img,
        Err(err) => {
            eprintln!("{}", err);
            return;
        }
    };
    img.save("output.png").unwrap();
    println!("woo done");
}
