#!/usr/bin/env python

import time
from sproxyscripter import *

#os.system('rm *.dxt')
#os.system('rm /home/vizuser/.sage/bin/appLauncher/pid/*.pid')
imagePath = '/home/vizuser/art_francesca/UTSA1/'


s = Scripter()

d = []



#d.append(DisplayObject('imageviewer', '/home/vizuser/Desktop/h.jpg', 0, 3, 6, 1 ))
#d.append(DisplayObject('imageviewer', '/home/vizuser/Desktop/h.jpg', 0, 3, 6, 3 ))

d.append(DisplayObject('imageviewer', imagePath+'W51.jpg', 0, 0, 6, 3 ))
d.append(DisplayObject('imageviewer', imagePath+'MG.tif', 0, 0, 6, 3 ))
d.append(DisplayObject('imageviewer', imagePath+'WB1.jpg', 5, 0, 1, 4 ))
d.append(DisplayObject('imageviewer', imagePath+'YW1.jpg', 0, 0, 3, 4 ))
d.append(DisplayObject('imageviewer', imagePath+'BR.jpg', 1, 0, 5, 1 ))
d.append(DisplayObject('imageviewer', imagePath+'Z.jpg', 1, 1, 1, 3 ))
d.append(DisplayObject('imageviewer', imagePath+'Ab21.jpg', 4, 2, 2, 2 ))
d.append(DisplayObject('imageviewer', imagePath+'Ab18.jpg', 2, 1, 2, 2 ))
d.append(DisplayObject('imageviewer', imagePath+'RO2.jpg', 4, 0, 2, 4 ))
d.append(DisplayObject('imageviewer', imagePath+'RO8.jpg', 2, 0, 1, 4 ))
d.append(DisplayObject('imageviewer', imagePath+'WR.jpg', 0, 0, 5, 4 ))
d.append(DisplayObject('imageviewer', imagePath+'BR.jpg', 0, 3, 4, 1 ))
d.append(DisplayObject('imageviewer', imagePath+'GhFlight.jpg', 4, 0, 2, 4 ))
d.append(DisplayObject('imageviewer', imagePath+'FPw13.jpg', 4, 0, 1, 4 ))


i = 0
for o in d:
	print 'd' + str(i)
	
	# If title slide wait before display
	if o.filename_ == imagePath+'title.png':
		time.sleep(5)
	s.imageviewer(o)
	if i == 14:
		time.sleep(2)
	else:
		time.sleep(2)
	i += 1

