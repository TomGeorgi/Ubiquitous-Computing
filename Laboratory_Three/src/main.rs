extern crate philipshue;

use philipshue::bridge::Bridge;
use philipshue::errors::{BridgeError, HueError, HueErrorKind};
use philipshue::hue::LightCommand;

use std::fs::File;
use std::path::Path;
use std::io;
use std::io::prelude::*;
use std::thread;
use std::time::Duration;

use cpu_monitor::CpuInstant;

fn main() -> Result<(), io::Error> {

    let ip = "141.37.168.50";
    let mut user = String::new();

    if Path::new("./hue.cfg").exists() {
        let mut file = File::open("./hue.cfg")?;
        file.read_to_string(&mut user)?;
    }

    if user.is_empty() {
        loop {
            match philipshue::bridge::register_user(&ip, "my_hue_app#homepc") {
                Ok(username) => {
                    println!("User registered: {}, on IP: {}", username, ip);
                    user = username.clone();
                    let mut file = File::create("./hue.cfg")?;
                    file.write_all(username.as_bytes())?;
                    break;
                }
                Err(HueError(
                    HueErrorKind::BridgeError {
                        error: BridgeError::LinkButtonNotPressed,
                        ..
                    },
                    _,
                )) => {
                    println!("Please, press the link on the bridge. Retrying in 5 seconds");
                    thread::sleep(Duration::from_secs(5));
                }
                Err(e) => {
                    println!("Unexpected error occured: {}", e);
                    break;
                }
            }
        }
    }

    let bridge = Bridge::new(ip, user.clone());
    let bridge_2 = Bridge::new(ip, user.clone());
    ctrlc::set_handler(move || {
        let cmd = LightCommand::default().off();

        match bridge_2.set_light_state(1, &cmd) {
            Ok(_) => {
                println!("Successfully switched light off.");
            }
            Err(e) => println!("Error occured when trying to send request:\n\t{}", e),
        }
        std::process::exit(0);
    }).expect("Error setting Ctrl-C handler");

    let cmd = LightCommand::default().on();

    match bridge.set_light_state(1, &cmd) {
        Ok(_) => {
            println!("Successfully switched light on.");
        }
        Err(e) => println!("Error occured when trying to send request:\n\t{}", e),
    }

    println!("Measuring CPU...");

    loop {
        let start = CpuInstant::now()?;
        std::thread::sleep(Duration::from_millis(100));
        let end = CpuInstant::now()?;
        let duration = end - start;

        let cpu_per = duration.non_idle();

        let cmd = LightCommand::default();

        let cpu_cmd = cmd
            .with_hue(21845 - (cpu_per * 21845.0) as u16)
            .with_sat(255)
            .with_bri(255);

        match bridge.set_light_state(1, &cpu_cmd) {
            Ok(_) => {}
            Err(e) => println!("Error occured when trying to send request:\n\t{}", e),
        }
    }
}
