use image::{GenericImageView, RgbImage};
use rand::distributions::{Distribution, WeightedIndex};
use rand::{self, Rng};
use std::collections::{HashMap, HashSet, VecDeque};
use std::fmt;
use std::hash::Hash;

const GRID_SIZE: (u32, u32) = (32, 32);
const TILE_SIZE: (u32, u32) = (1, 1);
const PATTERN_SIZE: (u8, u8) = {
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
impl Hash for Tile {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.image.hash(state);
    }
}
impl PartialEq for Tile {
    fn eq(&self, other: &Self) -> bool {
        return self.image == other.image;
    }
}
impl Eq for Tile {}
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

#[derive(Clone)]
struct Cell {
    x: u32,
    y: u32,
    patterns: Vec<Pattern>,
}
impl Cell {
    fn new(x: u32, y: u32) -> Cell {
        return Cell {
            x: x,
            y: y,
            patterns: Vec::new(),
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
        let pattern = self.patterns.swap_remove(index);
        self.patterns.clear();
        self.patterns.push(pattern);
    }

    fn is_collapsed(&self) -> bool {
        return self.patterns.len() == 1;
    }

    fn get_tile(&self) -> Option<&Tile> {
        if self.is_collapsed() {
            Some(&self.patterns[0].tile)
        } else {
            None
        }
    }

    fn entropy(&self) -> u32 {
        if self.is_collapsed() {
            u32::MAX
        } else {
            self.patterns.iter().map(|pattern| pattern.count).sum()
        }
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
    pattern_size: (u8, u8),
    wrap_around_edges: bool,
    allow_rotations: bool, // TODO
) -> Vec<Pattern> {
    let mut patterns: Vec<Pattern> = Vec::new();
    for x in 0..image.width() / tile_size.0 {
        for y in 0..image.height() / tile_size.1 {
            let tile = tiles[&(x, y)].clone();
            // O(pattern_size.0 ** 2 * pattern_size.1 ** 2) from here on out
            // size should be very small, its not as bad as it looks
            for dx in -(pattern_size.0 as i8) + 1..=0 {
                'new_pattern: for dy in -(pattern_size.1 as i8) + 1..=0 {
                    let mut offset_tiles = HashMap::new();
                    for ddx in 0..pattern_size.0 {
                        for ddy in 0..pattern_size.1 {
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
                        offset_tiles.len() == (pattern_size.0 * pattern_size.1 - 1) as usize
                    } else {
                        offset_tiles.len() <= (pattern_size.0 * pattern_size.1 - 1) as usize
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
    pattern_size: (u8, u8),
    collapsed_count: u32,
}
impl Grid {
    fn new(size: (u32, u32), tile_size: (u32, u32), pattern_size: (u8, u8)) -> Grid {
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
            pattern_size: pattern_size,
            collapsed_count: 0,
        };
    }

    fn lowest_entropy_cells(&mut self) -> Vec<&mut Cell> {
        assert!(!self.is_solved());
        let mut lowest_entropy = u32::MAX - 1;
        let mut cells = Vec::new();
        for cell in &mut self.cells {
            let entropy = cell.entropy();
            if entropy < lowest_entropy {
                lowest_entropy = entropy;
                cells.clear();
            }
            if entropy == lowest_entropy {
                cells.push(cell);
            }
        }
        cells
    }

    fn collapse_random_cell(&mut self) -> &mut Cell {
        let mut rng = rand::thread_rng();
        let mut cells = self.lowest_entropy_cells();
        cells.swap_remove(rng.gen_range(0..cells.len()))
    }

    fn is_solved(&self) -> bool {
        self.cells.iter().all(|cell| cell.is_collapsed())
    }

    fn iteration(&mut self) {
        let mut queue = VecDeque::new();
        let cell = self.collapse_random_cell();
        cell.collapse();
        queue.push_back(cell);
        while let Some(cell) = queue.pop_front() {
            let mut allowed_tiles = HashMap::new();
            for pattern in &cell.patterns {
                for ((dx, dy), tile) in &pattern.offset_tiles {
                    allowed_tiles
                        .entry((dx, dy))
                        .or_insert_with(HashSet::new)
                        .insert(tile);
                }
            }
        }
    }

    fn solve(&mut self) {
        while !self.is_solved() {
            self.iteration();
        }
    }

    fn create_image(&self) -> Result<RgbImage, String> {
        let mut image = RgbImage::new(
            self.size.0 * self.tile_size.0,
            self.size.1 * self.tile_size.1,
        );
        for cell in &self.cells {
            let tile = match cell.get_tile() {
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
        pattern_size: (u8, u8),
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
        if pattern_size.0 as u32 / tile_size.0 != pattern_size.1 as u32 / tile_size.1 {
            return Err(format!(
                "Pattern size ({}x{}) does not have the same aspect ratio as the tile size ({}x{}).",
                pattern_size.0, pattern_size.1, tile_size.0, tile_size.1
            ));
        }
        let tiles = create_tiles(image, tile_size);
        let patterns = create_patterns(
            image,
            &tiles,
            tile_size,
            pattern_size,
            wrap_around_edges,
            allow_rotations,
        );
        println!("{} patterns", patterns.len());
        let mut grid = Grid::new(grid_size, tile_size, pattern_size);
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
        PATTERN_SIZE,
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
