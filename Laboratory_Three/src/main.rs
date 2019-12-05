extern crate philipshue;

use std::env;
use std::num::ParseIntError;
use std::thread;
use std::time::Duration;

use philipshue::bridge::Bridge;
use philipshue::errors::{BridgeError, HueError, HueErrorKind};
use philipshue::hue::LightCommand;

use sysinfo::SystemExt;

fn main() {
    match run() {
        Ok(()) => (),
        Err(_) => println!("Invalid number!"),
    }
}

fn run() -> Result<(), ParseIntError> {
    let args: Vec<String> = env::args().collect();

    let ip = "141.37.168.50";
    let mut user = String::from("dMv8oSnasGXAB0G7t0ZmHF4lgYei4OO9J7wg8dhZ");

    if user.is_empty() {
        loop {
            match philipshue::bridge::register_user(&ip, "my_hue_app#homepc") {
                Ok(username) => {
                    println!("User registered: {}, on IP: {}", username, ip);
                    user = username;
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

    let bridge = Bridge::new(ip, user);

    let cmd = LightCommand::default();

    let cmd = match &*args[1] {
        "on" => cmd.on(),
        "off" => cmd.off(),
        "bri" => cmd.with_bri(args[2].parse()?),
        "hue" => cmd.with_hue(args[2].parse()?),
        "sat" => cmd.with_sat(args[2].parse()?),
        "hsv" => cmd
            .with_hue(args[2].parse()?)
            .with_sat(args[3].parse()?)
            .with_bri(args[4].parse()?),
        "rgb" => {
            let (hue, sat, bri) = rgb_to_hsv(args[2].parse()?, args[3].parse()?, args[4].parse()?);
            cmd.with_hue(hue).with_sat(sat).with_bri(bri)
        }
        "mired" => cmd
            .with_ct(args[4].parse()?)
            .with_bri(args[5].parse()?)
            .with_sat(254),
        "kelvin" => cmd
            .with_ct((1000000u32 / args[4].parse::<u32>()?) as u16)
            .with_bri(args[5].parse()?)
            .with_sat(254),
        _ => return Ok(println!("Invalid command!")),
    };

    match bridge.set_light_state(1, &cmd) {
        Ok(resps) => {
            for resp in resps.into_iter() {
                println!("{:?}", resp)
            }
        }
        Err(e) => println!("Error occured when trying to send request:\n\t{}", e),
    }

    let info = sysinfo::System::new();
    let processors: &[sysinfo::Processor] = info.get_processor_list();

    loop {
        thread::sleep(Duration::from_secs(5));
        println!("{:?}", processors);
    }

    Ok(())
}

pub fn rgb_to_hsv(r: u8, g: u8, b: u8) -> (u16, u8, u8) {
    let r = r as f64 / 255f64;
    let g = g as f64 / 255f64;
    let b = b as f64 / 255f64;
    let max = r.max(g.max(b));
    let min = r.min(g.min(b));

    if max == min {
        (0, 0, (max * 255.) as u8)
    } else {
        let d = max - min;
        let s = d / max;
        let h = if max == r {
            (g - b) / d + (if g < b { 6f64 } else { 0f64 })
        } else if max == g {
            (b - r) / d + 2f64
        } else {
            (r - g) / d + 4f64
        };
        (
            (65535. * h / 6.) as u16,
            (s * 255.) as u8,
            (max * 255.) as u8,
        )
    }
}