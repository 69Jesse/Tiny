use rand::Rng;

const EMPTY: usize = 0;
const PLAYER_1: usize = 1;
const PLAYER_2: usize = 2;

const BOARD_HEIGHT: usize = 6;
const BOARD_WIDTH: usize = 7;

fn create_board() -> [[usize; BOARD_WIDTH]; BOARD_HEIGHT] {
    [[EMPTY; BOARD_WIDTH]; BOARD_HEIGHT]
}

fn random_player() -> usize {
    let mut rng = rand::thread_rng();
    let index = rng.gen_range(0..2);
    [PLAYER_1, PLAYER_2][index]
}

fn other_player(player: usize) -> usize {
    if player == PLAYER_1 {
        PLAYER_2
    } else {
        PLAYER_1
    }
}

fn cell_symbol(cell: usize) -> String {
    match cell {
        EMPTY => " ".to_string(),
        PLAYER_1 => "\x1b[91mX\x1b[39m".to_string(),
        PLAYER_2 => "\x1b[33mO\x1b[39m".to_string(),
        _ => panic!("Invalid cell value"),
    }
}

fn print_board(board: &[[usize; BOARD_WIDTH]; BOARD_HEIGHT]) {
    let mut text: String = String::new();
    text.push_str("╔");
    for _ in 0..BOARD_WIDTH {
        text.push_str("═══╦");
    }
    text.pop();
    text.push_str("╗\n");
    for row in board.iter() {
        text.push_str("║");
        for cell in row.iter() {
            text.push_str(&format!(" {} ", cell_symbol(*cell)));
            text.push_str("║");
        }
        text.push_str("\n");
        text.push_str("╠");
        for _ in 0..BOARD_WIDTH {
            text.push_str("═══╬");
        }
        text.pop();
        text.push_str("╣\n");
    }
    text.push_str("║");
    for i in 0..BOARD_WIDTH {
        text.push_str(&format!(" {} ║", i + 1));
    }
    text.push_str("\n");
    println!("{}", text);
}

fn main() {
    let mut board = create_board();
    let player = random_player();
    let computer = other_player(player);
    let mut turn = random_player();
    print_board(&board);
}
