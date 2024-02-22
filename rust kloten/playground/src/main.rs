use rand::Rng;

const EMPTY: usize = 0;
const PLAYERS: [usize; 2] = [1, 2];

const BOARD_HEIGHT: usize = 6;
const BOARD_WIDTH: usize = 7;

fn create_board() -> [[usize; BOARD_WIDTH]; BOARD_HEIGHT] {
    [[EMPTY; BOARD_WIDTH]; BOARD_HEIGHT]
}

fn random_player() -> usize {
    let mut rng = rand::thread_rng();
    PLAYERS[rng.gen_range(0..2)]
}

fn other_player(player: usize) -> usize {
    if player == PLAYERS[0] {
        PLAYERS[1]
    } else {
        PLAYERS[0]
    }
}

fn main() {
    let mut board = create_board();
    let player = random_player();
    let computer = other_player(player);
    let mut turn = random_player();
}
