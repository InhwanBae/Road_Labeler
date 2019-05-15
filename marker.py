#!/usr/bin/env python
# -*- coding:utf8 -*-
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from PyQt5.QtCore import *


class DelayedUpdater(QObject):

    def __init__(self, target, parent=None):
        super(DelayedUpdater, self).__init__(parent)
        self.target = target
        target.installEventFilter(self)

        self.delayEnabled = True
        self.delayTimeout = 1000

        self._resizeTimer = QTimer()
        self._resizeTimer.timeout.connect(self._delayedUpdate)

    def eventFilter(self, obj, event):
        if self.delayEnabled and obj is self.target:
            if event.type() == event.MouseButtonRelease:
                self._resizeTimer.start(self.delayTimeout)
                #self.target.setUpdatesEnabled(False)

        return False

    def _delayedUpdate(self):
        #print("Performing actual update")
        self._resizeTimer.stop()
        #self.target.setUpdatesEnabled(True)
        self.target.update()

class DraggablePoint:
    showverts = True
    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, pathpatch, pathtype):
        self.ax = pathpatch.axes
        canvas = self.ax.figure.canvas
        self.pathpatch = pathpatch
        self.pathpatch.set_animated(True)
        self.pathtype = pathtype

        x, y = zip(*self.pathpatch.get_path().vertices)

        if self.pathtype == "line":
            self.line, = self.ax.plot(x, y, marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)
        elif self.pathtype == "polygon":
            self.line, = self.ax.plot(x[:-1], y[:-1], marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)
        elif self.pathtype == "object":
            self.line, = self.ax.plot(x[:-1], y[:-1], marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)
        elif self.pathtype == "point":
            self.line, = self.ax.plot(x, y, marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)
        else:
            print("Missing Pathtype")
            self.line, = self.ax.plot(x, y, marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)

        self._ind = None  # the active vert

        self.canvas = canvas

        #self.delayer = DelayedUpdater(self.canvas)
        self.drawStatus = 0

    def connect(self):
        self.canvas.mpl_connect('draw_event', self.draw_callback)
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.button_press_callback)
        self.canvas.mpl_connect('key_press_event', self.key_press_callback)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.button_release_callback)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)




    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.pathpatch)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

    def pathpatch_changed(self, pathpatch):
        print("pathpatch_changed")
        'this method is called whenever the pathpatchgon object is called'
        # only copy the artist props to the line (except visibility)
        vis = self.line.get_visible()
        plt.Artist.update_from(self.line, pathpatch)
        self.line.set_visible(vis)  # don't use the pathpatch visibility state

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
        xy = np.asarray(self.pathpatch.get_path().vertices)
        xyt = self.pathpatch.get_transform().transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)
        ind = d.argmin()

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)
        #self.drawStatus = 1



    def draw_once(self):
        if self.drawStatus:
            self.drawStatus = 0
            # for faster scene update
            self.canvas.setUpdatesEnabled(False)
            self.canvas.draw()
            # for faster scene update
            self.canvas.setUpdatesEnabled(True)

    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self.showverts:
            return
        if event.button != 1:
            return
        self._ind = None
        #self.canvas.draw()
        #self.canvas.update()
        self.draw_once()


    def key_press_callback(self, event):
        print('key_press_callback')
        'whenever a key is pressed'
        if not event.inaxes:
            return
        if event.key == 't':
            self.showverts = not self.showverts
            self.line.set_visible(self.showverts)
            if not self.showverts:
                self._ind = None

        self.canvas.draw()

    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self.showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        xc, yc = event.xdata, event.ydata

        vertices = self.pathpatch.get_path().vertices

        vertices[self._ind] = xc, yc

        if self.pathtype == "polygon":
            vertices[-1] = vertices[0]
        if self.pathtype == "object":
            if self._ind == 0:
                vertices[4] = vertices[0]
                vertices[1][0] = xc
                vertices[3][1] = yc
            if self._ind == 1:
                vertices[0][0] = xc
                vertices[4][0] = xc
                vertices[2][1] = yc
            if self._ind == 2:
                vertices[3][0] = xc
                vertices[1][1] = yc
            if self._ind == 3:
                vertices[2][0] = xc
                vertices[0][1] = yc
                vertices[4][1] = yc

        self.line.set_data(zip(*vertices))

        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.pathpatch)

        x, y = zip(*self.pathpatch.get_path().vertices)

        # for test
        if self.pathtype == "line":
            #self.line, = self.ax.plot(x, y, marker='o', markerfacecolor='r', markeredgecolor='y', lw=0, linestyle='dashed', animated=True)
            pass
        elif self.pathtype == "polygon":
            self.line, = self.ax.plot(x[:-1], y[:-1], marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)
        elif self.pathtype == "object":
            self.line, = self.ax.plot(x[:-1], y[:-1], marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)
        elif self.pathtype == "point":
            self.line, = self.ax.plot(x, y, marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)
        else:
            print("Missing Pathtype")
            self.line, = self.ax.plot(x, y, marker='o', markerfacecolor='r', markeredgecolor='w', linestyle='none', animated=True)

        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)
        #self.canvas.draw()
        #self.canvas.flush_events()
        #self.canvas.update()
        #self.drawStatus = 1
        #self.draw_once();
        self.drawStatus = 1

        """
        # for faster scene update
        self.canvas.setUpdatesEnabled(False)
        self.canvas.draw()
        # for faster scene update
        self.canvas.setUpdatesEnabled(True)
        """

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.canvas.mpl_disconnect(self.cidpress)
        self.canvas.mpl_disconnect(self.cidrelease)
        self.canvas.mpl_disconnect(self.cidmotion)


    def get_position(self):
        return self.pathpatch.get_path().vertices
