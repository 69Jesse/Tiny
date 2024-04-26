use image::GenericImageView;
use image::Pixel;
use std::fs;
use std::path::PathBuf;

const MOSAIC_SIZE: (u32, u32) = (8, 8);

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

    fn create_pixels(&mut self) {
        let img = match image::open(&self.path) {
            Ok(img) => img.resize_exact(
                MOSAIC_SIZE.0,
                MOSAIC_SIZE.1,
                image::imageops::FilterType::Nearest,
            ),
            Err(e) => {
                eprintln!("Could not open image: {}", e);
                return;
            }
        };
        for y in 0..img.height() {
            for x in 0..img.width() {
                let pixel = img.get_pixel(x, y).to_rgb();
                self.pixels.push(pixel);
                println!("{:?}", pixel);
            }
        }
    }
}

fn get_mosaics() -> Option<Vec<Mosaic>> {
    let paths = match fs::read_dir("./mosaics/") {
        Ok(paths) => paths,
        Err(e) => {
            eprintln!("Error: {}", e);
            return None;
        }
    };
    let mut mosaics = Vec::new();
    for path in paths {
        let path = path.unwrap().path();
        let mut mosaic = Mosaic::new(path);
        mosaic.create_pixels();
        mosaics.push(mosaic);
    }
    Some(mosaics)
}

fn main() {
    let mosaics = match get_mosaics() {
        Some(mosaics) => mosaics,
        None => return,
    };
    for mosaic in mosaics {
        println!("{:?}", mosaic.path);
    }
}
