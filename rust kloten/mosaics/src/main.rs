use image::{GenericImageView, Pixel};
use std::{cmp, error::Error, fs, path::PathBuf};

const CELL_SIZE: (u32, u32) = {
    let n = 16;
    (n, n)
};
const MAX_GRID_SIZE: (u32, u32) = {
    let n = 64;
    (n, n)
};

#[derive(Debug)]
struct Mosaic {
    path: PathBuf,
    size: (u32, u32),
    pixels: Vec<image::Rgb<u8>>,
}
impl Mosaic {
    fn new(path: PathBuf) -> Self {
        Mosaic {
            path: path,
            size: CELL_SIZE,
            pixels: Vec::new(),
        }
    }

    fn create_pixels(&mut self) -> Result<(), Box<dyn Error>> {
        let img = image::open(&self.path)?.resize_exact(
            self.size.0,
            self.size.1,
            image::imageops::FilterType::Nearest,
        );
        for y in 0..img.height() {
            for x in 0..img.width() {
                let pixel = img.get_pixel(x, y).to_rgb();
                self.pixels.push(pixel);
            }
        }
        assert!(self.pixels.len() == (CELL_SIZE.0 * CELL_SIZE.1) as usize);
        Ok(())
    }
}

#[derive(Debug)]
struct Cell {
    size: (u32, u32),
    pixels: Vec<image::Rgb<u8>>,
}
impl Cell {
    fn new(size: (u32, u32)) -> Self {
        Cell {
            size: size,
            pixels: Vec::new(),
        }
    }
}

#[derive(Debug)]
struct Grid {
    path: PathBuf,
    size: (u32, u32),
    cells: Vec<Cell>,
}
impl Grid {
    fn new(path: PathBuf, size: (u32, u32)) -> Self {
        Grid {
            path: path,
            size: size,
            cells: Vec::new(),
        }
    }

    fn from_image(path: PathBuf) -> Result<Self, Box<dyn Error>> {
        let img = image::open(&path)?;
        let old_size = img.dimensions();
        let grid_size = {
            // TODO round to nearest integer instead of flooring
            if (old_size.0 as f64 / MAX_GRID_SIZE.0 as f64)
                > (old_size.1 as f64 / MAX_GRID_SIZE.1 as f64)
            {
                (
                    MAX_GRID_SIZE.0,
                    cmp::max(
                        ((MAX_GRID_SIZE.0 * old_size.1) as f64 / old_size.0 as f64) as u32,
                        1,
                    ),
                )
            } else {
                (
                    cmp::max(
                        ((MAX_GRID_SIZE.1 * old_size.0) as f64 / old_size.1 as f64) as u32,
                        1,
                    ),
                    MAX_GRID_SIZE.1,
                )
            }
        };
        assert!(grid_size.0 <= MAX_GRID_SIZE.0 && grid_size.1 <= MAX_GRID_SIZE.1);
        let img = img.resize_exact(
            grid_size.0 * CELL_SIZE.0,
            grid_size.1 * CELL_SIZE.1,
            image::imageops::FilterType::Nearest,
        );
        let mut grid = Grid::new(path, grid_size);
        for y in 0..grid.size.1 {
            for x in 0..grid.size.0 {
                let mut cell = Cell::new(CELL_SIZE);
                for dy in 0..cell.size.1 {
                    for dx in 0..cell.size.0 {
                        let pixel = img.get_pixel(x * cell.size.0 + dx, y * cell.size.1 + dy);
                        cell.pixels.push(pixel.to_rgb());
                    }
                }
                assert!(cell.pixels.len() == (CELL_SIZE.0 * CELL_SIZE.1) as usize);
                grid.cells.push(cell);
            }
        }
        Ok(grid)
    }
}

fn get_mosaics() -> Result<Vec<Mosaic>, Box<dyn Error>> {
    let paths = fs::read_dir("./mosaics/")?;
    let mut mosaics = Vec::new();
    for path in paths {
        let path = path.unwrap().path();
        let mut mosaic = Mosaic::new(path);
        mosaic.create_pixels()?;
        mosaics.push(mosaic);
    }
    Ok(mosaics)
}

fn main() {
    let mosaics = match get_mosaics() {
        Ok(mosaics) => mosaics,
        Err(e) => {
            eprintln!("Could not get fetch: {}", e);
            return;
        }
    };
    let grid = match Grid::from_image(PathBuf::from("./input.png")) {
        Ok(grid) => grid,
        Err(e) => {
            eprintln!("Could not create grid: {}", e);
            return;
        }
    };
    print!("{:?}", grid.size);
}
