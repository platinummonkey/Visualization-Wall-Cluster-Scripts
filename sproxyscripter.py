#!/usr/bin/python

#import pexpect
#import subprocess
#import threading
import time
import sys
import os
import array
import xmlrpclib

# Defines
SAGE_PROXY_SERVER='localhost'
SAGE_PROXY_PORT=20001 # port number listed in GUI (actual port is +3... thanks evl for not documenting this)
#SAGE_PID_PATH='/home/vizuser/.sageConfig/applications/pid'
SAGE_PATH='/usr/local/sage'
HORIZONTAL_RES = 2561
VERTICAL_RES   = 1600
BEZEL_RES      = 220
NUM_MONITORS_HORIZ=6
NUM_MONITORS_VERT=4

#DEBUG = False
DEBUG = True

# resize
# sageProxy.resizeWindow(int appId, int left, int right, int bottom, int top)
#
# move
# sageProxy.moveWindow(int appId, int x, int y)
#
# bring to front
# sageProxy.bringToFront(int appId)
#
# imageviewer/mplayer
# sageProxy.executeApp(string appName, configName="default", pos=False, size=False, shareable=False, optionalArgs="")
# pos = (int x, int y)
# size = (int left, int right, int bottom, int top)
# Returns: { int appId: [ string appName, int appId, int left, int right, int bottom, int top, int sailID, int zValue, int configNum, string title]}
# Returns -1 if something borks
#
# close imageviewer/mplayer
# sageProxy.closeApp(int appId)
#

FAR_EDGE=(-1*(NUM_MONITORS_HORIZ*HORIZONTAL_RES + NUM_MONITORS_HORIZ*BEZEL_RES), 0)

def sortAppID(d):
	"""Fixes sageProxies output... because evl used a string instead of an int... x.x
	returns list of tuples reverse sorted"""
	dnew = {}
	for k,v in d.items():
		dnew[int(k)] = v
	dlist = dnew.items()
	dlist.sort(reverse=True)
	print "dlist: " + repr(dlist)
	return dlist
	

def convertDisplayCoordinatesToPixels(d, x, y, sizeX, sizeY):
	d.l_ = x*(HORIZONTAL_RES+BEZEL_RES)
	d.r_ = d.l_ + sizeX*HORIZONTAL_RES + (sizeX-1)*BEZEL_RES
	d.b_ = y*(VERTICAL_RES+BEZEL_RES)
	d.t_ = d.b_ + sizeY*VERTICAL_RES + (sizeY-1)*BEZEL_RES
        print "%s: Left: %s Right: %s Bottom: %s Top: %s" % (d.winID_, d.l_, d.r_, d.b_, d.t_)

class DisplayObject:
	def __init__(self, app, filename, x, y, sizeX, sizeY):
		self.spawn_ = 0
		self.app_ = app
		self.filename_ = filename
		self.winID_ = -1
		self.sizeX_ = sizeX
		self.sizeY_ = sizeY
		convertDisplayCoordinatesToPixels(self, x, y, sizeX, sizeY)

class Scripter:
	# Class for scripting images and video to play on a tiled display
	# using SAGE, Magicarpet, and other methods.

	def __init__ (self):
		# System level configuration variables
		self.sageProxy = xmlrpclib.ServerProxy("http://%s:%s" % (SAGE_PROXY_SERVER, SAGE_PROXY_PORT+3))
		self.lastAppID = None

	def imageviewer(self, d):
		#d.filename_ file name
                
		iv = self.sageProxy.executeApp('imageviewer', "default", (0,0), False, False, d.filename_)
		time.sleep(1)
		iv = self.sageProxy.getAppStatus()
		ivl = sortAppID(iv)
		ivv = ivl[0] # latest appID we think
		print "I THINK THE APPID IS: " + str(ivv[0])
		if self.lastAppID is None:
			self.lastAppID = ivv[0]
			print "No lastAppID found: setting to: " + str(ivv[0])
		else:
			self.lastAppID += 1
		print "self.lastAppID = " + str(self.lastAppID)
		#if ivv[0] == self.lastAppID:
		#	# likely not right
		#	self.lastAppID = ivv[0]+1
		#	#if DEBUG: print "d:", repr(dir(d))
		#	d.app_ = 'mplayer'
		#	d.winID_ = self.lastAppID
		#else:
		# appID seems right
		d.app_ = 'imageviewer'
		d.winID_ = self.lastAppID
		#self.lastAppID = ivv[0]
		if DEBUG: print "Final WinID:", ivv[0]
		self.moveWindow(d)
		return

	def mplayer(self, d):
		iv = self.sageProxy.executeApp('mplayer', "default", (0,0), False, False, d.filename_)
		ivl = sortAppID(iv)
		ivv = ivl[0] # latest appID we think
		if ivv[0] == self.lastAppID:
			# likely not right
			self.lastAppID = ivv[0]+1
			#if DEBUG: print "d:", repr(dir(d))
			d.app_ = 'mplayer'
			d.winID_ = self.lastAppID
		else:
			# appID seems right
			d.app_ = ivv[1][0]
			d.winID_ = ivv[0]
			self.lastAppID = ivv[0]
		if DEBUG: print "Final WinID:", ivv[0]
		self.moveWindow(d)
		return
	
	# fidgets an images +/- 1 pixel to force sage to update display
	def fidgetWindow(self, d):
		if DEBUG: print "fidgeting window", repr(d.winID_)
		time.sleep(0.25) # give sage a quarter-second
		self.sageProxy.resizeWindow(d.winID_, d.l_-1, d.r_-1, d.b_-1, d.t_-1)
		time.sleep(0.25) # pause
		self.sageProxy.resizeWindow(d.winID_, d.l_, d.r_, d.b_, d.t_)
		return

	# Moves a sage window
	def moveWindow(self, d):
		if DEBUG: print "Moving window", repr(d.winID_)
		self.sageProxy.resizeWindow(d.winID_, d.l_, d.r_, d.b_, d.t_)
		self.fidgetWindow(d)
		return

	def hideWindow(self, d):
		if DEBUG: print "Hiding window", repr(d.winID_)
		self.sageProxy.resizeWindow(d.winID_, 0, 1, 0, 1)
		return
	
	def hideAllWindows(self,d):
		if DEBUG: print "Hiding ALL Windows!"
		for o in d:
			self.hideWindow(o)
			time.sleep(0.25)
		return
	
	def showWindow(self, d):
		if DEBUG: print "Showing window", repr(d.winID_)
		self.sageProxy.bringToFront(d.winID_)
		self.moveWindow(d)
		return

	# Kills a sage window
	def killSageApp(self, d):
		if DEBUG: print "Killing window", repr(d.winID_)
		self.sageProxy.closeApp(d.winID_)
		return
