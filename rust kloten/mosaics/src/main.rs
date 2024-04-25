use std::fs;
use std::path::PathBuf;
use image::GenericImageView;


struct Mosaic {
    path: PathBuf,
    pixels: Vec<Vec<u8>>,
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
            Ok(img) => img,
            Err(e) => {
                eprintln!("Could not open image: {}", e);
                return;
            }
        };
        for y in 0..img.height() {
            for x in 0..img.width() {
                let pixel = img.get_pixel(x, y);
                self.pixels.push(vec![pixel[0], pixel[1], pixel[2]]);
                println!("{:?}", pixel);
                // TODO turn into RGB and convert into RGB
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
