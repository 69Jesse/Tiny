use image::{DynamicImage, GenericImage, GenericImageView, Pixel};
use std::{cmp, error::Error, fs, path::PathBuf};

const CELL_SIZE: (u32, u32) = {
    let n = 16;
    (n, n)
};
const MAX_GRID_SIZE: (u32, u32) = {
    let n = 128;
    (n, n)
};

#[allow(dead_code)]
enum ComparisonMethod {
    Average,
    Manhattan,
    Euclidean,
}

trait Average {
    fn get_pixels(&self) -> Vec<image::Rgb<u8>>;
    fn set_average(&mut self, average: (f64, f64, f64));

    fn calculate_average(&mut self) {
        let mut r = 0;
        let mut g = 0;
        let mut b = 0;
        for pixel in self.get_pixels().iter() {
            r += pixel[0] as u32;
            g += pixel[1] as u32;
            b += pixel[2] as u32;
        }
        let n = self.get_pixels().len() as u32;
        let average = (
            r as f64 / n as f64,
            g as f64 / n as f64,
            b as f64 / n as f64,
        );
        self.set_average(average);
    }
}

#[derive(Debug)]
struct Mosaic {
    path: PathBuf,
    pixels: Vec<image::Rgb<u8>>,
    average: (f64, f64, f64),
}
impl Mosaic {
    fn new(path: PathBuf) -> Self {
        Mosaic {
            path: path,
            pixels: Vec::new(),
            average: (0.0, 0.0, 0.0),
        }
    }

    fn create_pixels(&mut self) -> Result<(), Box<dyn Error>> {
        let img = image::open(&self.path)?.resize_exact(
            CELL_SIZE.0,
            CELL_SIZE.1,
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
impl Average for Mosaic {
    fn get_pixels(&self) -> Vec<image::Rgb<u8>> {
        self.pixels.clone()
    }

    fn set_average(&mut self, average: (f64, f64, f64)) {
        self.average = average;
    }
}

#[derive(Debug)]
struct Cell {
    pixels: Vec<image::Rgb<u8>>,
    average: (f64, f64, f64),
}
impl Cell {
    fn new() -> Self {
        Cell {
            pixels: Vec::new(),
            average: (0.0, 0.0, 0.0),
        }
    }

    fn distance(&self, mosaic: &Mosaic, method: &ComparisonMethod) -> f64 {
        assert!(self.pixels.len() == mosaic.pixels.len());
        match method {
            ComparisonMethod::Average => {
                let mut distance = 0.0;
                distance += (self.average.0 - mosaic.average.0).powi(2)
                    + (self.average.1 - mosaic.average.1).powi(2)
                    + (self.average.2 - mosaic.average.2).powi(2);
                distance
            }
            ComparisonMethod::Euclidean => {
                let mut distance = 0.0;
                for (p1, p2) in self.pixels.iter().zip(mosaic.pixels.iter()) {
                    distance += (p1[0] as f64 - p2[0] as f64).powi(2)
                        + (p1[1] as f64 - p2[1] as f64).powi(2)
                        + (p1[2] as f64 - p2[2] as f64).powi(2);
                }
                distance
            }
            ComparisonMethod::Manhattan => {
                let mut distance = 0.0;
                for (p1, p2) in self.pixels.iter().zip(mosaic.pixels.iter()) {
                    distance += (p1[0] as f64 - p2[0] as f64).abs()
                        + (p1[1] as f64 - p2[1] as f64).abs()
                        + (p1[2] as f64 - p2[2] as f64).abs();
                }
                distance
            }
        }
    }

    fn best_match<'a>(&'a self, others: &Vec<&'a Mosaic>, method: &ComparisonMethod) -> &'a Mosaic {
        let mut best = others[0];
        let mut best_distance = self.distance(best, method);
        for other in others.iter().skip(1) {
            let distance = self.distance(*other, method);
            if distance < best_distance {
                best = *other;
                best_distance = distance;
            }
        }
        best
    }
}
impl Average for Cell {
    fn get_pixels(&self) -> Vec<image::Rgb<u8>> {
        self.pixels.clone()
    }

    fn set_average(&mut self, average: (f64, f64, f64)) {
        self.average = average;
    }
}

#[derive(Debug)]
struct Grid {
    size: (u32, u32),
    cells: Vec<Cell>,
}
impl Grid {
    fn new(size: (u32, u32)) -> Self {
        Grid {
            size: size,
            cells: Vec::new(),
        }
    }

    fn from_image(path: PathBuf, method: &ComparisonMethod) -> Result<Self, Box<dyn Error>> {
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
        let mut grid = Grid::new(grid_size);
        for y in 0..grid.size.1 {
            for x in 0..grid.size.0 {
                let mut cell = Cell::new();
                for dy in 0..CELL_SIZE.1 {
                    for dx in 0..CELL_SIZE.0 {
                        let pixel = img.get_pixel(x * CELL_SIZE.0 + dx, y * CELL_SIZE.1 + dy);
                        cell.pixels.push(pixel.to_rgb());
                    }
                }
                assert!(cell.pixels.len() == (CELL_SIZE.0 * CELL_SIZE.1) as usize);
                match method {
                    ComparisonMethod::Average => {
                        cell.calculate_average();
                    }
                    _ => {}
                }
                grid.cells.push(cell);
            }
        }
        Ok(grid)
    }

    fn create_mosaic_image(
        &self,
        mosaics: &Vec<&Mosaic>,
        method: &ComparisonMethod,
    ) -> Result<DynamicImage, Box<dyn Error>> {
        let mut img =
            image::DynamicImage::new_rgb8(self.size.0 * CELL_SIZE.0, self.size.1 * CELL_SIZE.1);
        for y in 0..self.size.1 {
            for x in 0..self.size.0 {
                let cell = &self.cells[(y * self.size.0 + x) as usize];
                let best_mosaic = cell.best_match(&mosaics, &method);
                for dy in 0..CELL_SIZE.1 {
                    for dx in 0..CELL_SIZE.0 {
                        let pixel = best_mosaic.pixels[(dy * CELL_SIZE.0 + dx) as usize];
                        img.put_pixel(
                            x * CELL_SIZE.0 + dx,
                            y * CELL_SIZE.1 + dy,
                            image::Rgba([pixel[0], pixel[1], pixel[2], 255]),
                        );
                    }
                }
            }
            println!("Row {}/{}", y + 1, self.size.1)
        }
        Ok(img)
    }
}

fn fetch_mosaics(method: &ComparisonMethod) -> Result<Vec<Mosaic>, Box<dyn Error>> {
    let paths = fs::read_dir("./mosaics/")?;
    let mut mosaics = Vec::new();
    for path in paths {
        let path = path.unwrap().path();
        let mut mosaic = Mosaic::new(path);
        mosaic.create_pixels()?;
        match method {
            ComparisonMethod::Average => {
                mosaic.calculate_average();
            }
            _ => {}
        }
        mosaics.push(mosaic);
    }
    Ok(mosaics)
}

fn main() {
    let method = ComparisonMethod::Average;
    let mosaics = match fetch_mosaics(&method) {
        Ok(mosaics) => mosaics,
        Err(e) => {
            eprintln!("Could not get fetch: {}", e);
            return;
        }
    };
    let mosaic_references: Vec<&Mosaic> = mosaics.iter().collect();

    let grid = match Grid::from_image(PathBuf::from("./bogdan.png"), &method) {
        Ok(grid) => grid,
        Err(e) => {
            eprintln!("Could not create grid: {}", e);
            return;
        }
    };

    let img = match grid.create_mosaic_image(&mosaic_references, &method) {
        Ok(img) => img,
        Err(e) => {
            eprintln!("Could not create mosaic image: {}", e);
            return;
        }
    };
    img.save("output.png").unwrap();
}
