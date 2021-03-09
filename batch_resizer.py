#!/usr/bin/env python3

from os import path, walk
import sys
from datetime import datetime
from distutils.dir_util import copy_tree
from PIL import Image
import argparse
from progress.bar import Bar

# Options
parser = argparse.ArgumentParser(description="Reduce size of a bunch of images")
parser.add_argument('source', metavar='<source folder>')
parser.add_argument("-p", "--percent", default=10, type=int, metavar='<percentage>',
					help='resize in percent (default: 10)')
parser.add_argument("-o", "--output", default=".",
					help='destination folder (default: .)')
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

if args.percent not in range(1, 99):
	parser.print_usage()
	print("Error: Percent must be between 1 and 99")
	sys.exit()
else:
	_percent = args.percent

_src_folder = args.source
_dest_folder = args.output

if not path.exists(_src_folder):
	parser.print_usage()
	print(f"Error: {_src_folder} folder does not exist")
	sys.exit()
if not path.exists(_dest_folder):
	parser.print_usage()
	print(f"Error: {_dest_folder} folder does not exist")
	sys.exit()

# Step 1: copy images folder
while _src_folder.endswith(path.sep):
	_src_folder = _src_folder[:-1]
while _dest_folder.endswith(path.sep):
	_dest_folder = _dest_folder[:-1]

_folder_name = path.basename(_src_folder)
_timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
_dest_folder = path.join(_dest_folder, _folder_name + "_" + str(_timestamp))

print(f"Destination folder: {_dest_folder}")
if path.exists(_dest_folder):
	print(f"Destination folder {_dest_folder} exists. Wait for a second then retry")
	sys.exit()
try:
	copy_tree(_src_folder, _dest_folder)
except Exception as e:
	print(f"{_src_folder} cannot be copied into {_dest_folder}")
	print(str(e))

# Step 2: Parse and resize images
if not args.verbose:
	bar = Bar('Processing', max=sum([len(files) for r, d, files in walk(_dest_folder)]))
for root, dirs, files in walk(_dest_folder):
	if args.verbose:
		if len(files) > 0:
			bar = Bar(root, max=len(files))
	for name in files:
		fullname = str(path.join(root, name))
		try:
			image = Image.open(fullname)
			width, height = image.size
			image.thumbnail((width * _percent // 100, height * _percent // 100))
			image.save(fullname)
		except:
			pass
		bar.next()
	if args.verbose:
		if len(files) > 0:
			bar.finish()
if not args.verbose:
	bar.finish()
