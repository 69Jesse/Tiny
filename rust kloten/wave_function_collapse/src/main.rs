use image::{GenericImageView, Rgb, RgbImage};
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
        for x in 0..self.image.width() {
            for y in 0..self.image.height() {
                self.image.get_pixel(x, y).hash(state);
            }
        }
    }
}
impl PartialEq for Tile {
    fn eq(&self, other: &Self) -> bool {
        // TODO
        if self.image.width() != other.image.width() || self.image.height() != other.image.height()
        {
            return false;
        }
        for x in 0..self.image.width() {
            for y in 0..self.image.height() {
                if self.image.get_pixel(x, y) != other.image.get_pixel(x, y) {
                    return false;
                }
            }
        }
        return true;
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
    offset_tiles: HashMap<(u8, u8), Tile>,
    count: u32,
}
impl Pattern {
    fn new(tile: Tile, offset_tiles: HashMap<(u8, u8), Tile>) -> Pattern {
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
impl Hash for Pattern {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.tile.hash(state);
        let mut keys = self.offset_tiles.keys().collect::<Vec<_>>();
        keys.sort();
        for key in keys {
            key.hash(state);
            self.offset_tiles[key].hash(state);
        }
    }
}
impl PartialEq for Pattern {
    fn eq(&self, other: &Self) -> bool {
        return self.tile == other.tile && {
            let mut self_keys = self.offset_tiles.keys().collect::<Vec<_>>();
            let mut other_keys = other.offset_tiles.keys().collect::<Vec<_>>();
            self_keys.sort();
            other_keys.sort();
            self_keys == other_keys
                && self_keys
                    .iter()
                    .all(|key| self.offset_tiles[key] == other.offset_tiles[key])
        };
    }
}
impl Eq for Pattern {}

#[derive(Clone)]
struct Cell {
    x: u32,
    y: u32,
    patterns: HashSet<Pattern>,
    initial_pattern_count: u32,
}
impl Cell {
    fn new(x: u32, y: u32) -> Cell {
        return Cell {
            x: x,
            y: y,
            patterns: HashSet::new(),
            initial_pattern_count: 0,
        };
    }

    fn pattern_in_bounds(&self, pattern: &Pattern, wrap_around_edges: bool) -> bool {
        if wrap_around_edges {
            return true;
        }
        for (dx, dy) in pattern.offset_tiles.keys() {
            let (x, y) = (self.x as i64 + *dx as i64, self.y as i64 + *dy as i64);
            if x < 0 || y < 0 || x >= GRID_SIZE.0 as i64 || y >= GRID_SIZE.1 as i64 {
                return false;
            }
        }
        return true;
    }

    fn initiate_patterns(&mut self, patterns: &HashSet<Pattern>, wrap_around_edges: bool) {
        assert!(self.patterns.is_empty());
        for pattern in patterns {
            if self.pattern_in_bounds(pattern, wrap_around_edges) {
                self.patterns.insert(pattern.clone());
            }
        }
        self.initial_pattern_count = self.patterns.len() as u32;
        assert!(!self.patterns.is_empty());
    }

    fn collapse(
        &mut self,
        tried_patterns: &HashSet<Pattern>,
    ) -> Result<HashSet<Pattern>, ()> {
        assert!(!self.is_collapsed());
        if self.patterns.is_empty() {
            return Err(());
        }
        let mut patterns: Vec<Pattern> = self.patterns.iter().cloned().collect();
        patterns.retain(|pattern| !tried_patterns.contains(pattern));
        if patterns.is_empty() {
            return Err(());
        }
        let weights = patterns
            .iter()
            .map(|pattern| pattern.count)
            .collect::<Vec<u32>>();
        let mut rng = rand::thread_rng();
        let index = WeightedIndex::new(&weights).unwrap().sample(&mut rng);
        let pattern = patterns.swap_remove(index);
        let old_patterns = self.patterns.clone();
        self.patterns.clear();
        self.patterns.insert(pattern);
        Ok(old_patterns)
    }

    fn is_collapsed(&self) -> bool {
        return self.patterns.len() == 1;
    }

    fn get_tile(&self) -> Option<&Tile> {
        if self.is_collapsed() {
            Some(&self.patterns.iter().next().unwrap().tile)
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
) -> HashSet<Pattern> {
    let mut patterns_map = HashMap::new();
    for x in 0..image.width() / tile_size.0 {
        for y in 0..image.height() / tile_size.1 {
            let tile = tiles[&(x, y)].clone();
            let mut offset_tiles = HashMap::new();
            for dx in 0..pattern_size.0 {
                for dy in 0..pattern_size.1 {
                    if dx == 0 && dy == 0 {
                        continue;
                    }
                    let (tx, ty) = ((x as i64 + dx as i64), (y as i64 + dy as i64));
                    if !wrap_around_edges
                        && (tx < 0
                            || ty < 0
                            || tx >= image.width() as i64
                            || ty >= image.height() as i64)
                    {
                        continue;
                    }
                    let (tx, ty) = (
                        tx.rem_euclid((image.width() / tile_size.0) as i64) as u32,
                        ty.rem_euclid((image.height() / tile_size.1) as i64) as u32,
                    );
                    offset_tiles.insert((dx, dy), tiles[&(tx, ty)].clone());
                }
            }
            assert!(if wrap_around_edges {
                offset_tiles.len() == (pattern_size.0 * pattern_size.1 - 1) as usize
            } else {
                offset_tiles.len() <= (pattern_size.0 * pattern_size.1 - 1) as usize
            });
            let pattern = Pattern::new(tile.clone(), offset_tiles);
            if !patterns_map.contains_key(&pattern) {
                patterns_map.insert(pattern.clone(), pattern);
                continue;
            }
            patterns_map.get_mut(&pattern).unwrap().increment();
        }
    }
    patterns_map.values().cloned().collect()
}

struct Grid {
    size: (u32, u32),
    cells: Vec<Cell>,
    tile_size: (u32, u32),
    pattern_size: (u8, u8),
    history: Vec<(
        (u32, u32),                            // collapsed cell position
        HashSet<Pattern>,                      // tried patterns so far
        HashSet<(u32, u32)>,                   // cells tried to collapse next iteration
        HashMap<(u32, u32), HashSet<Pattern>>, // removed patterns from cells
    )>,
}
impl Grid {
    fn new(size: (u32, u32), tile_size: (u32, u32), pattern_size: (u8, u8)) -> Grid {
        let mut cells = Vec::new();
        for y in 0..size.1 {
            for x in 0..size.0 {
                cells.push(Cell::new(x, y));
            }
        }
        return Grid {
            size: size,
            cells: cells,
            tile_size: tile_size,
            pattern_size: pattern_size,
            history: Vec::new(),
        };
    }

    fn lowest_entropy_cell_positions(&self) -> Vec<(u32, u32)> {
        assert!(!self.is_solved());
        let mut lowest_entropy = u32::MAX - 1;
        let mut cell_positions = Vec::new();
        for cell in &self.cells {
            let entropy = cell.entropy();
            if entropy < lowest_entropy {
                lowest_entropy = entropy;
                cell_positions.clear();
            }
            if entropy == lowest_entropy {
                cell_positions.push((cell.x, cell.y));
            }
        }
        cell_positions
    }

    fn fetch_next_cell_position(&mut self) -> Result<(u32, u32), ()> {
        let last_history_entry = self.history.last();
        let mut rng = rand::thread_rng();
        let mut cell_positions = self.lowest_entropy_cell_positions();
        if let Some(last_history_entry) = last_history_entry {
            let already_tried = &last_history_entry.2;
            cell_positions.retain(|(x, y)| !already_tried.contains(&(*x, *y)));
        }
        if cell_positions.is_empty() {
            return Err(());
        }
        Ok(cell_positions.swap_remove(rng.gen_range(0..cell_positions.len())))
    }

    fn is_solved(&self) -> bool {
        self.cells.iter().all(|cell| cell.is_collapsed())
    }

    fn get_index_at(&self, x: u32, y: u32) -> usize {
        (x + y * self.size.0) as usize
    }

    fn get_cell_at(&self, x: u32, y: u32) -> &Cell {
        let index = self.get_index_at(x, y);
        &self.cells[index]
    }

    fn get_mut_cell_at(&mut self, x: u32, y: u32) -> &mut Cell {
        let index = self.get_index_at(x, y);
        &mut self.cells[index]
    }

    fn insert_into_queue(
        queue: &mut VecDeque<(u32, u32)>,
        queue_set: &mut HashSet<(u32, u32)>,
        x: u32,
        y: u32,
    ) {
        if queue_set.contains(&(x, y)) {
            return;
        }
        queue_set.insert((x, y));
        queue.push_back((x, y));
    }

    fn backtrack(&mut self) {
        println!("Backtracking, {}", self.history.len());
        let mut history_entry = match self.history.pop() {
            Some(history_entry) => history_entry,
            None => panic!("No solution found."),
        };
        for ((x, y), removed_patterns) in history_entry.3.clone() {
            println!("Adding {} patterns back to ({}, {})", removed_patterns.len(), x, y);
            let cell = self.get_mut_cell_at(x, y);
            cell.patterns.extend(removed_patterns);
        }
        history_entry.3.clear();

        let cell = self.get_cell_at(history_entry.0.0, history_entry.0.1);
        if history_entry.1.len() < cell.patterns.len() {
            self.history.push(history_entry);
        } else {
            println!("fuck");
        }
    }

    fn iteration(&mut self) {
        let (x, y) = match self.fetch_next_cell_position() {
            Ok(cell_position) => cell_position,
            Err(_) => return self.backtrack(),
        };

        let mut history_entry = {
            // TODO: make this less disgusting
            match match self.history.last() {
                Some(entry) => {
                    if entry.0 == (x, y) {
                        Some(self.history.pop().unwrap())
                    } else {
                        None
                    }
                }
                None => None,
            } {
                Some(entry) => entry,
                None => ((x, y), HashSet::new(), HashSet::new(), HashMap::new()),
            }
        };
        history_entry.2.insert((x, y));

        let cell = self.get_mut_cell_at(x, y);
        let removed = match cell.collapse(&history_entry.1) {
            Ok(removed) => removed,
            Err(_) => return self.backtrack(),
        };
        history_entry
            .1
            .insert(cell.patterns.iter().next().unwrap().clone());
        history_entry
            .3
            .entry((x, y))
            .or_insert_with(HashSet::new)
            .extend(removed);

        let mut queue = VecDeque::new();
        let mut queue_set = HashSet::new();
        queue_set.insert((x, y));
        queue.push_back((x, y));

        while let Some((x, y)) = queue.pop_front() {
            let cell = self.get_cell_at(x, y).clone();
            queue_set.remove(&(cell.x, cell.y));
            let mut all_allowed_tiles = HashMap::new();
            for pattern in &cell.patterns {
                all_allowed_tiles
                    .entry((&0, &0))
                    .or_insert_with(HashSet::new)
                    .insert(&pattern.tile);
                for ((dx, dy), tile) in &pattern.offset_tiles {
                    all_allowed_tiles
                        .entry((dx, dy))
                        .or_insert_with(HashSet::new)
                        .insert(tile);
                }
            }

            for dx in 0..self.pattern_size.0 {
                for dy in 0..self.pattern_size.1 {
                    let (x, y) = (
                        (cell.x as i64 + dx as i64).rem_euclid(self.size.0 as i64) as u32,
                        (cell.y as i64 + dy as i64).rem_euclid(self.size.1 as i64) as u32,
                    );
                    let neighbour = self.get_mut_cell_at(x, y);
                    let allowed_tiles = match all_allowed_tiles.get(&(&dx, &dy)) {
                        Some(allowed_tiles) => allowed_tiles,
                        None => return self.backtrack(),
                    };
                    for neighbour_pattern in neighbour.patterns.clone() {
                        if allowed_tiles.contains(&neighbour_pattern.tile) {
                            continue;
                        }
                        neighbour.patterns.remove(&neighbour_pattern);
                        Self::insert_into_queue(&mut queue, &mut queue_set, x, y);
                        history_entry
                            .3
                            .entry((x, y))
                            .or_insert_with(HashSet::new)
                            .insert(neighbour_pattern);
                    }
                }
            }

            for dx in -(self.pattern_size.0 as i16 - 1)..=0 {
                for dy in -(self.pattern_size.1 as i16 - 1)..=0 {
                    if dx == 0 && dy == 0 {
                        continue;
                    }
                    let (x, y) = (
                        (cell.x as i64 + dx as i64).rem_euclid(self.size.0 as i64) as u32,
                        (cell.y as i64 + dy as i64).rem_euclid(self.size.1 as i64) as u32,
                    );
                    let neighbour = self.get_mut_cell_at(x, y);
                    let allowed_tiles = &all_allowed_tiles[&(&0, &0)];
                    for neighbour_pattern in neighbour.patterns.clone() {
                        let (neighbour_dx, neighbour_dy) = (-dx as u8, -dy as u8);
                        let tile = neighbour_pattern
                            .offset_tiles
                            .get(&(neighbour_dx, neighbour_dy))
                            .unwrap();
                        if allowed_tiles.contains(tile) {
                            continue;
                        }
                        neighbour.patterns.remove(&neighbour_pattern);
                        Self::insert_into_queue(&mut queue, &mut queue_set, x, y);
                        history_entry
                            .3
                            .entry((x, y))
                            .or_insert_with(HashSet::new)
                            .insert(neighbour_pattern);
                    }
                }
            }
        }
        self.history.push(history_entry);
    }

    fn solve(&mut self) {
        while !self.is_solved() {
            self.visualize();
            self.iteration();
        }
        self.visualize();
    }

    fn visualize(&self) {
        self.create_image().unwrap().save("output.png").unwrap();
        // println!("\nVisualisation:");
        // for y in 0..self.size.1 {
        //     for x in 0..self.size.0 {
        //         let cell = self.get_cell_at(x, y);
        //         let symbol = if cell.is_collapsed() {
        //             String::from(".X.")
        //         } else {
        //             format!("{:03}", cell.patterns.len())
        //         };
        //         print!("{} ", symbol);
        //     }
        //     println!();
        // }
    }

    fn create_image(&self) -> Result<RgbImage, String> {
        let mut image = RgbImage::new(
            self.size.0 * self.tile_size.0,
            self.size.1 * self.tile_size.1,
        );
        for cell in &self.cells {
            if cell.is_collapsed() {
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
            } else {
                for x in 0..self.tile_size.0 {
                    for y in 0..self.tile_size.1 {
                        image.put_pixel(x, y, Rgb([0, 0, 0]));
                    }
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
    let mut grid = Grid::from_image(
        &img,
        GRID_SIZE,
        TILE_SIZE,
        PATTERN_SIZE,
        WRAP_AROUND_EDGES,
        ALLOW_ROTATIONS,
    )
    .unwrap_or_else(|err| {
        eprintln!("{}", err);
        std::process::exit(1);
    });
    grid.solve();
    let img = grid.create_image().unwrap_or_else(|err| {
        eprintln!("{}", err);
        std::process::exit(1);
    });
    img.save("output.png").unwrap();
    println!("woo done");
}
