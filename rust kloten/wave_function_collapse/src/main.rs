use image::DynamicImage;
use image_hasher::HasherConfig;
use std::collections::HashSet;

const OPTION_SIZE: (u32, u32) = (2, 2);
const OFFSET: (u32, u32) = (OPTION_SIZE.0 / 2, OPTION_SIZE.1 / 2);

struct Option<'a> {
    image: DynamicImage,
    count: u8,
    hasher: &'a image_hasher::Hasher,
}
impl<'a> Option<'a> {
    fn new(image: DynamicImage, hasher: &'a image_hasher::Hasher) -> Option {
        return Option {
            image: image,
            count: 1,
            hasher: hasher,
        };
    }

    fn increment(&mut self) {
        self.count += 1;
    }
}
impl std::hash::Hash for Option<'_> {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        let hash = self.hasher.hash_image(&self.image);
        hash.hash(state);
    }
}
impl PartialEq for Option<'_> {
    fn eq(&self, other: &Self) -> bool {
        let hash1 = self.hasher.hash_image(&self.image);
        let hash2 = self.hasher.hash_image(&other.image);
        return hash1 == hash2;
    }
}
impl Eq for Option<'_> {}

struct Cell<'a> {
    x: u32,
    y: u32,
    options: HashSet<Option<'a>>,
}
impl<'a> Cell<'a> {
    fn is_collapsed(&self) -> bool {
        return false;
    }
}

fn create_options(image: DynamicImage) -> HashSet<Option<'static>> {
    let hasher = HasherConfig::new().to_hasher();
    let mut set = HashSet::new();
    return set;
}

fn main() {
    let input = image::open("input.png").unwrap();
    let options = create_options(input);
    println!("{:?}", options.len());
}
