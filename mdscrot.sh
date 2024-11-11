#!/bin/sh

# basic tool so I can add images to writeups less painfully
# I have this bound to a key in openbox
imagepath="~/Documents/coding/ctf/writeups/ctf-writeups/images/"
githubpath="https://github.com/mythemeria/ctf-writeups/blob/main/images/"
imagename=$(date +"%d%m%Y-%H%M%S.png")
mdpath="~/Documents/coding/ctf/writeups/ctf-writeups/working.md"

scrot -s $imagepath$imagename

if [ -f "$imagepath$imagename" ]; then
  [ ! -f mdpath ] && touch $mdpath

  set +H
  echo "![screenshot]($githubpath$imagename?raw=true)" >> $mdpath
  echo "" >> $mdpath
  set -H
fi