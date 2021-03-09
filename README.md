# Image Batch Resizer

## What
This script takes a folder that contains images and reduces them into a new folder

It is written in Python 3

## Why
I needed a simple way to get thumbnails of multiple images

## Requirements
```bash
pip install -r requirements.txt
```

OR

```bash
pip install pillow
pip install progress
```

## --help
```bash
usage: batch_resizer.py [-h] [-p <percentage>] [-o OUTPUT] [-v] <source folder>

Reduce size of a bunch of images

positional arguments:
  <source folder>

optional arguments:
  -h, --help            show this help message and exit
  -p <percentage>, --percent <percentage>
                        resize in percent (default: 10)
  -o OUTPUT, --output OUTPUT
                        destination folder (default: .)
  -v, --verbose         increase output verbosity
```

### Exemple
Call the script with the following command:
```bash
python3 -p 50 /home/me/vacation_photos
```