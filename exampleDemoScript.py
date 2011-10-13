#! /usr/bin/python

import time
from sagescripts.sproxyscripter import *

imagePath='/home/vizuser/art_francesca/UTSA3/'

d = []

s = Scripter()
d.append(DisplayObject('imageviewer', imagePath+'shaken1.jpg', 0, 0, 2, 4))
d.append(DisplayObject('imageviewer', imagePath+'GW22.jpg', 2, 0 ,4, 4))
d.append(DisplayObject('imageviewer', imagePath+'pc2.jpg', 5, 0, 1, 4))
d.append(DisplayObject('imageviewer', imagePath+'RO4.jpg', 2, 0, 1, 1))
d.append(DisplayObject('imageviewer', imagePath+'gsw7.jpg', 3, 3, 1, 1))
d.append(DisplayObject('imageviewer', imagePath+'gsw1.jpg', 3, 0, 1, 1))
d.append(DisplayObject('imageviewer', imagePath+'gsw2.jpg', 3, 1, 1, 1))
d.append(DisplayObject('imageviewer', imagePath+'gsw9.jpg', 5, 2, 1, 1))
d.append(DisplayObject('imageviewer', imagePath+'gsw10.jpg', 0, 0, 1, 1))


# initially display all images
i = 0   
for o in d: 
        print 'Showing image #' + str(i)
        s.imageviewer(o)
        time.sleep(2)
        i += 1  

# start loop
while True:
        yesno = raw_input('Loop? [Y/n] ')
        yesno = yesno.lower()[0] # take lowercase of first letter
        if yesno == 'n':
                break
        s.hideAllWindows(d)
        i=0
        for o in d:
                print 'Showing image #' + str(i)
                s.showWindow(o)
                time.sleep(2)

# close out all images
i = 0
for o in d:
        print 'Closing image #' + str(i)
        s.killSageApp(o)
        time.sleep(0.25)
        i += 1

