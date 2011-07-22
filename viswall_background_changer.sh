#!/bin/bash
# converts images of 16466x7060 100dpi into background tiles for each tilenode
# utsa vis wall
# Cody Lee
# 07-20-2011 18:45

BACKGROUND_DIRECTORY="/nemo-nas/vizuser/backgrounds"
TILES_BACKGROUND_DIRECTORY="$BACKGROUND_DIRECTORY/tiles"
HOSTS_FILE="$BACKGROUND_DIRECTORY/hosts.list"

echo $HOSTS_FILE

### DONT TOUCH BELOW ###
#check for arugments
if [ $# -ne 1 ]; then
  echo "Usage: `basename $0` {background name}"
  exit 68
fi

#make sure images exist
SH="`cat $HOSTS_FILE | line`"
echo "omfg: $TILES_BACKGROUND_DIRECTORY/$1/$SH.jpg"
if [ -f "$TILES_BACKGROUND_DIRECTORY/$1/$SH.jpg" ]; then
  # all good - let it fall through
  echo "Setting backgrounds"
else
  # files dont exist
  echo "Image does not exist!"
  echo "Remember dont use the file extension! ie. 'avl.jpg' would just be 'avl'"
  echo "Run the background image creation tool to create image!"
  exit 50
fi

for h in `cat $HOSTS_FILE`
do
  ssh $h /home/vizuser/viswall_tile_setbg.sh $TILES_BACKGROUND_DIRECTORY/$1/$h.jpg \&
  echo "Background for $h set"
done
echo "Done"
