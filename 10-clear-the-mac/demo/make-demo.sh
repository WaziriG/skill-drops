#!/bin/bash
# Builds a pretend computer and two pretend drives in ~/clear-the-mac-demo so you can watch
# the whole cycle (list, copy, check, clear, pull back) before touching anything real.
set -e
D="$HOME/clear-the-mac-demo"
rm -rf "$D"
mkdir -p "$D/home/Clients | Old/Acme Co/Receipts" "$D/home/Clients | Old/Beta LLC" "$D/home/Projects/Current" "$D/DRIVE_A" "$D/DRIVE_B"
head -c 3000000 /dev/urandom > "$D/home/Clients | Old/Acme Co/Receipts/2023-invoices.pdf"
head -c 4000000 /dev/urandom > "$D/home/Clients | Old/Acme Co/launch-video.mov"
head -c 3000000 /dev/urandom > "$D/home/Clients | Old/Beta LLC/photos.jpg"
head -c 3000000 /dev/urandom > "$D/home/Projects/Current/draft.mov"
touch -t 202301010000 "$D/home/Clients | Old/Acme Co/Receipts/2023-invoices.pdf" "$D/home/Clients | Old/Acme Co/launch-video.mov" "$D/home/Clients | Old/Beta LLC/photos.jpg"
echo "Demo ready at $D"
echo "Pretend computer: $D/home    Pretend drives: $D/DRIVE_A and $D/DRIVE_B"
echo "Now open Claude Code and say: /clear-the-mac demo, using $D"
