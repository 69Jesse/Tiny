use image::{GenericImageView, Pixel};
use std::{error::Error, fs, path::PathBuf};

const CELL_SIZE: (u32, u32) = (16, 16);
const MAX_GRID_SIZE: (u32, u32) = {
    let n = 16;
    (n * CELL_SIZE.0, n * CELL_SIZE.1)
};

struct Mosaic {
    path: PathBuf,
    pixels: Vec<image::Rgb<u8>>,
}
impl Mosaic {
    fn new(path: PathBuf) -> Self {
        Mosaic {
            path: path,
            pixels: Vec::new(),
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
            eprintln!("Could not get mosaics: {}", e);
            return;
        }
    };
    for mosaic in mosaics {
        println!("{:?}", mosaic.path);
    }
}
