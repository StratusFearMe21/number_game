use const_colors::{bold, end, green, red, yellow};
use rand::Rng;
use serde::{Deserialize, Serialize};

#[derive(Default, Deserialize, Serialize)]
struct SaveFile {
    total_guesses: u32,
    rounds_won: u32,
    rounds_lost: u32,
    total_rounds: u32,
}

impl SaveFile {
    fn save(&self, file: &mut std::fs::File) {
        bincode::serialize_into(file, self).unwrap();
    }
    fn load(file: &mut std::fs::File) -> Self {
        bincode::deserialize_from(file).unwrap_or_default()
    }
}

fn main() {
    let console = console::Term::stdout();
    let mut guess: u32;
    let mut rng = rand::thread_rng();
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .read(true)
        .create(true)
        .open("savefile.bc")
        .unwrap();
    let mut savefile = SaveFile::load(&mut file);
    loop {
        let number = rng.gen_range(
            0..=10_u32.pow(
                dialoguer::Select::new()
                    .items(&[
                        concat!(green!(), "1: Very Easy (100 possibilities)", end!()),
                        concat!(green!(), "2: Easy (1,000 possibilities)", end!()),
                        concat!(yellow!(), "3: Default (10,000 possibilities)", end!()),
                        concat!(red!(), "4: Hard (100,000 possibilites)", end!()),
                        concat!(red!(), "5: Very Hard (1,000,000 possibilities)", end!()),
                    ])
                    .with_prompt(concat!(bold!(), "Which difficulty would you like?", end!()))
                    .default(2)
                    .interact_on(&console)
                    .unwrap() as u32
                    + 2,
            ),
        );
        'a: loop {
            guess = dialoguer::Input::new()
                .with_prompt("Try to guess what number I'm thinking of (in less than 100 guesses)!")
                .interact_on(&console)
                .unwrap();
            for _ in 0..100 {
                savefile.total_guesses += 1;
                if guess < number {
                    guess = dialoguer::Input::new()
                        .with_prompt("Your guess is too low")
                        .interact_on(&console)
                        .unwrap();
                } else if guess > number {
                    guess = dialoguer::Input::new()
                        .with_prompt("Your guess is too high")
                        .interact_on(&console)
                        .unwrap();
                } else {
                    savefile.rounds_won += 1;
                    console.write_line("You guessed correct!").unwrap();
                    break 'a;
                }
            }
            savefile.rounds_lost += 1;
            break;
        }
        savefile.total_rounds += 1;
        console.write_line(&format!("Current standings:\n    Total guesses: {}\n    Rounds lost: {}\n    Rounds won: {}", savefile.total_guesses, savefile.rounds_lost, savefile.rounds_won)).unwrap();
        savefile.save(&mut file);
        if !dialoguer::Confirm::new()
            .with_prompt("Would you like to play another round?")
            .interact_on(&console)
            .unwrap()
        {
            break;
        }
    }
}
