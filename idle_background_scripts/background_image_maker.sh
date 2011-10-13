#!/bin/bash
# converts images of 16466x7060 100dpi into background tiles for each tilenode
# utsa vis wall
# Cody Lee
# 07-20-2011 18:45

SAGE_STDTILECONF="/usr/local/sage/sageConfig/stdtile.conf"
BACKGROUND_DIRECTORY="/nemo-nas/vizuser/backgrounds"
TILES_BACKGROUND_DIRECTORY="$BACKGROUND_DIRECTORY/tiles"
ORIGINAL_SUFFIX=".orig"
MONITORS_PER_ROW=6
MONITORS_PER_COL=4
HOSTS_FILE="$BACKGROUND_DIRECTORY/hosts.list"

### DONT TOUCH BELOW ###
#check for arugments
if [ $# -ne 1 ]; then
  echo "Usage: `basename $0` {filename}"
  exit 65
fi

#5120X1600
HEADNODE_RESOLUTION="`xdpyinfo | grep 'dimensions:' | awk '{ print $2 }'`"
# get tile node resolution
TILENODE_MONDIM_W="`cat $SAGE_STDTILECONF | grep Resolution | grep -v \# | awk '{ print $2}'`"
TILENODE_MONDIM_H="`cat $SAGE_STDTILECONF | grep Resolution | grep -v \# | awk '{ print $3}'`"
TILENODE_DIMENSION="${TILENODE_MONDIM_W}x${TILENODE_MONDIM_H}"
echo "tilenode resolution: $TILENODE_DIMENSION"

ORIG_IMAGE="`readlink -f $1`" # gets full un-ugly path
DIR="`dirname $ORIG_IMAGE`" # gets base path
# get just filename without .orig and without suffix or path prefix
BASEFNAME="`echo $ORIG_IMAGE | sed 's/.orig//' | sed 's|.*\/\([^\.]*\)\(\..*\)$|\1|g'`"

#final tiled directory
DIR="${TILES_BACKGROUND_DIRECTORY}/${BASEFNAME}"
mkdir -p $DIR

echo "Generating Background: $BASEFNAME"

#confirm input file is good
ORIG_DIM="`identify -format '%wx%h' $ORIG_IMAGE`"
ORIG_RES_X="`identify -format '%x' $ORIG_IMAGE | awk '{ print $1 }'`"
ORIG_RES_Y="`identify -format '%y' $ORIG_IMAGE | awk '{ print $1 }'`"

# Read sage Config and get chopping block size
Machines="`cat $SAGE_STDTILECONF |  grep Machines | grep -v \# | awk '{ print $2 }'`"
Monitors="`cat $SAGE_STDTILECONF |  grep Monitors | grep -v \# | line | awk '{ print $2 }'`"
#echo "Machines: $Machines - Monitors: $Monitors"
# Expected: Mullions top bottom left right
# Example: Mullions 1.1024 1.1024 1.1024 1.1014
Mullions="`cat $SAGE_STDTILECONF |  grep Mullions | grep -v top`"
MTOP="`echo $Mullions | awk '{ print $2 }'`"
MBOT="`echo $Mullions | awk '{ print $3 }'`"
MRIG="`echo $Mullions | awk '{ print $4 }'`"
MLEF="`echo $Mullions | awk '{ print $5 }'`"
DPI="`cat $SAGE_STDTILECONF |  grep PPI | grep -v \# | awk '{ print $2 }'`"
# The mullion (screen border) width in inches is converted to the number of pixels. In the example, the mullion width in pixel numbers is 0.6 (inch) x 90 (ppi) = 54 (pixels). 
CTOP="`echo \"($MTOP * $DPI)\" | bc -l  | xargs printf \"%1.0f\"`"
CBOT="`echo \"($MBOT * $DPI)\" | bc -l  | xargs printf \"%1.0f\"`"
CRIG="`echo \"($MRIG * $DPI)\" | bc -l  | xargs printf \"%1.0f\"`"
CLEF="`echo \"($MLEF * $DPI)\" | bc -l  | xargs printf \"%1.0f\"`"

CV="`echo \"$CTOP + $CBOT\" | bc -l`"
CH="`echo \"$CRIG + $CLEF\" | bc -l`"

#echo $CTOP $CBOT $CRIG $CLEF $CV $CH

# determine required input image size
REQUIRED_DIMENSION_W="`echo \"($CLEF + $CRIG + $TILENODE_MONDIM_W) * $MONITORS_PER_ROW\" | bc -l`"
REQUIRED_DIMENSION_H="`echo \"($CTOP + $CBOT + $TILENODE_MONDIM_H) * $MONITORS_PER_COL \" | bc -l`"
REQUIRED_DIMENSIONS="${REQUIRED_DIMENSION_W}x${REQUIRED_DIMENSION_H}"
REQUIRED_RESOLUTION=$DPI

#check if all conditions pass, if not then error out
if [  "$ORIG_DIM" != "$REQUIRED_DIMENSIONS" -o "$ORIG_RES_X" != "$REQUIRED_RESOLUTION" -o "$ORIG_RES_Y" != "$REQUIRED_RESOLUTION" ]; then
  # not all items passed, inform user and error out
  echo "Image size must be $REQUIRED_DIMENSIONS with a X and Y DPI of $REQUIRED_RESOLUTION"
  echo "Original Image size: $ORIG_DIM"
  echo "Original Image DPI: X:$ORIG_RES_X Y:$ORIG_RES_Y"
  exit 1
fi

echo "Image Size must be: $REQUIRED_DIMENSIONS with a X and Y DPI of $REQUIRED_RESOLUTION"

#create nemo image
# this will scale the image based on smallest fitting dimension
convert $ORIG_IMAGE -resize ${HEADNODE_RESOLUTION}^ -gravity center ${BACKGROUND_DIRECTORY}/${BASEFNAME}.jpg

# cut up the image into parts
TILENODE_FULL_DIM_W="`echo \"($Monitors * $TILENODE_MONDIM_W) + ($CH * $Monitors)\" | bc -l`"
MIDDLE_COL_OFFSET="`echo \"$CRIG + $TILENODE_MONDIM_W\" | bc -l`"
echo "Middle Column Offset: $MIDDLE_COL_OFFSET"
TILENODE_FULL_DIM_H="`echo \"$TILENODE_MONDIM_H + $CH\" | bc -l`"
TILENODE_FULL_DIM="${TILENODE_FULL_DIM_W}x${TILENODE_FULL_DIM_H}"
convert $ORIG_IMAGE +gravity -crop $TILENODE_FULL_DIM $DIR/tile_%d.jpg

#chop off edges of each image and rename tiles according to hostname
i=0
for h in `cat $HOSTS_FILE`
do
  #echo "$h -> tile_${i}.jpg"
  #convert filename -chop middleColumn -chop Top -chop Left -chop Right -chop Bottom output
  convert $DIR/tile_${i}.jpg -chop ${CH}x0+${MIDDLE_COL_OFFSET}+0 -chop 0x${CTOP} -chop ${CLEF}x0 -gravity East -chop ${CRIG}x0 -gravity South -chop 0x${CBOT} $DIR/${h}.jpg 
  rm $DIR/tile_${i}.jpg
  let i+=1
done
