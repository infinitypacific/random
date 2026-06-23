use clap::{Parser, ValueEnum};
use std::fs;
use std::path::{Path, PathBuf};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    #[arg(short, long, value_delimiter = ',')]
    extensions: Vec<String>,

    #[arg(short, long, value_enum)]
    format: LineFormat,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum, Debug)]
enum LineFormat {
    Lf,
    Crlf,
    Cr,
}

fn main() {
    let args = Args::parse();
    if args.extensions.is_empty() {
        eprintln!("You must specify at least one file extension using --extensions.");
        std::process::exit(1);
    }
    for entry_result in WalkDir::new(&args.path) {
        let entry = match entry_result {
            Ok(e) => e,
            Err(e) => {
                eprintln!("Failed to access path: {}", e);
                continue;
            }
        };
        let path = entry.path();
        if path.is_file() {
            if let Some(ext) = path.extension().and_then(|s| s.to_str()) {
                if args.extensions.iter().any(|e| e == ext) {
                    process_file(path, args.format);
                }
            }
        }
    }
}

fn process_file(path: &Path, target_format: LineFormat) {
    let content = match fs::read(path) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Failed to read {}: {}", path.display(), e);
            return;
        }
    };

    let content_str = match String::from_utf8(content) {
        Ok(s) => s,
        Err(_) => {
            eprintln!("Skipped non-UTF-8: {}", path.display());
            return;
        }
    };

    let normalized = content_str.replace("\r\n", "\n").replace('\r', "\n");
    let result = match target_format {
        LineFormat::Lf => normalized,
        LineFormat::Crlf => normalized.replace('\n', "\r\n"),
        LineFormat::Cr => normalized.replace('\n', "\r"),
    };

    if let Err(e) = fs::write(path, result) {
        eprintln!("Failed to write {}: {}", path.display(), e);
    } else {
        println!("Converted {}", path.display());
    }
}
