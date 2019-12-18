extern crate philipshue;

use philipshue::bridge::Bridge;
use philipshue::errors::{BridgeError, HueError, HueErrorKind};
use philipshue::hue::LightCommand;

use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::io::stdin;
use std::io::stdout;
use std::path::Path;
use std::sync::atomic::{AtomicU8, Ordering};
use std::sync::Arc;
use std::thread;
use std::time::Duration;
use sys_info::*;

use cpu_monitor::CpuInstant;

#[macro_use]
extern crate text_io;

use text_io::try_read;

fn get_mem_usage() -> f64 {
    let mem = mem_info().unwrap();
    mem.free as f64 / mem.total as f64
}

fn get_cpu_usage() -> Result<f64, io::Error> {
    let start = CpuInstant::now()?;
    std::thread::sleep(Duration::from_millis(500));
    let end = CpuInstant::now()?;
    let duration = end - start;
    Ok(duration.non_idle())
}

fn switch_light(bridge: &Bridge, on: bool) {
    let cmd = if on {
        LightCommand::default().on()
    } else {
        LightCommand::default().off()
    };

    match bridge.set_light_state(1, &cmd) {
        Ok(_) => {}
        Err(e) => println!("Error occured when trying to send request:\n\t{}", e),
    }
}

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
    let bridge_for_handler = Bridge::new(ip, user.clone());

    ctrlc::set_handler(move || {
        switch_light(&bridge_for_handler, false);
        println!("\nSuccessfully switched light off");
        std::process::exit(0);
    })
    .expect("Error setting Ctrl-C handler");

    let brightness = Arc::new(AtomicU8::new(255));
    let brightness_for_thread = brightness.clone();

    let mode = Arc::new(AtomicU8::new(0));
    let mode_for_thread = mode.clone();

    let threshold = Arc::new(AtomicU8::new(0));
    let threshold_for_thread = threshold.clone();

    println!("Measuring Systems CPU...");

    thread::spawn(move || -> Result<(), io::Error> {
        loop {
            let bri = brightness_for_thread.load(Ordering::SeqCst);
            let thres = threshold_for_thread.load(Ordering::SeqCst) as f64;
            let mode = mode_for_thread.load(Ordering::SeqCst);

            let usage = if mode == 0 {
                get_cpu_usage()?
            } else {
                get_mem_usage()
            };

            let cmd = LightCommand::default();

            if usage * 100.0 >= thres {
                switch_light(&bridge, true);
                let cpu_cmd = cmd
                    .with_hue(21845 - (usage * 21845.0) as u16)
                    .with_sat(255)
                    .with_bri(bri);

                match bridge.set_light_state(1, &cpu_cmd) {
                    Ok(_) => {}
                    Err(e) => println!("Error occured when trying to send request:\n\t{}", e),
                }
            } else {
                switch_light(&bridge, false);
            }
        }
    });

    loop {
        let mut t = String::new();
        print!("syshue> ");
        stdout().flush()?;
        stdin().read_line(&mut t)?;

        let bri_cmd: Result<u8, _> = try_read!("Brightness: {}", t.bytes());
        let thres_cmd: Result<u8, _> = try_read!("Threshold: {}%", t.bytes());

        if let Ok(num) = bri_cmd {
            println!("[OK] Setting brightness to {}", num);
            brightness.store(num, Ordering::SeqCst);
        } else if let Ok(num) = thres_cmd {
            println!("[OK] Setting threshold to {}%", num);
            threshold.store(num, Ordering::SeqCst);
        } else if t.contains("Mode: MEM") {
            println!("[OK] Tracking Memory now.");
            mode.store(1, Ordering::SeqCst);
        } else if t.contains("Mode: CPU") {
            println!("[OK] Tracking CPU usage now.");
            mode.store(0, Ordering::SeqCst);
        } else if t == "exit" {

            std::process::exit(0);
        } else {
            println!("[ERR] Unknown Command");
        }
    }
}
