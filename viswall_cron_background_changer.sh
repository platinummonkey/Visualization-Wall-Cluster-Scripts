#!/bin/bash
# converts images of 16466x7060 100dpi into background tiles for each tilenode
# utsa vis wall
# Cody Lee
# 07-20-2011 18:45

BACKGROUND_DIRECTORY="/nemo-nas/vizuser/backgrounds"
TILES_BACKGROUND_DIRECTORY="$BACKGROUND_DIRECTORY/tiles"
HOSTS_FILE="$BACKGROUND_DIRECTORY/hosts.list"

### DONT TOUCH BELOW ###
# create array of available backgrounds
i=0
for b in `ls $TILES_BACKGROUND_DIRECTORY`
do
  BGCHOICES[$i]=$b
  let i+=1
done

# randomly choose a background from available choices
BGCOUNT=${#BGCHOICES[@]} # number of available options
RNCHOICE="$(($RANDOM % $BGCOUNT))" # random # 0 through #Choices-1 (0-index)
CHOICE="${BGCHOICES[$RNCHOICE]}" # random choice
#echo "$BGCOUNT $RANDOM $RNCHOICE $CHOICE"
#echo "Choice 1: ${BGCHOICES[0]}"
#echo "Choice 2: ${BGCHOICES[1]}"
#echo "Choice 3: ${BGCHOICES[2]}"
#echo "Choice 4: ${BGCHOICES[3]}"

#set random background if sage or cglX isnt running
SAGEPROCS="`ps aux | grep sage | grep -v grep | wc -l`"
CGLXPROCS="`ps aux | grep cs | grep -v scsi | grep -v grep | wc -l`"
if [ $SAGEPROCS -gt 0 -o $CGLXPROCS -gt 0 ]
then
  # sage or CGLX is running do nothing
  echo "SAGE or cglX is running, doing nothing"
else
  /home/vizuser/viswall_background_changer.sh $CHOICE
fi
