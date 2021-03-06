#!/usr/bin/python

import sys, os
import unittest

from window.hamming_signal_window import HammingSignalWindow
from window.rectangular_signal_window import RectangularSignalWindow


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


WINDOW_SIZE = 4
INIT_WINDOW = {"X": {'quality': [], 'value': []}}

def _fillValues(window, count, start=0):
    for i in range(start, count):
        window.addData({"X": {"value" : i, "quality": i**2}})

def _fillWindowFull(window):
    _fillValues(window, WINDOW_SIZE)

class RectanglarSignalWindowTest(unittest.TestCase):

    def setUp(self):
        self.window = RectangularSignalWindow(WINDOW_SIZE, ["X"])

    def notify(self, data):
        self.notifyCalled += 1

    def test_windowsFilled(self):        
        self.assertEquals(self.window.window, INIT_WINDOW)
        
        _fillValues(self.window, WINDOW_SIZE / 2)
        self.assertEquals(self.window.window, {"X": {'quality': [0, 1], 'value': [0, 1]}}) 
        
        _fillValues(self.window, WINDOW_SIZE, WINDOW_SIZE / 2)
        self.assertEquals(self.window.window, INIT_WINDOW) 

    def test__register(self):
        self.notifyCalled = 0
        win = self.window
        win.registerObserver(self)
        _fillWindowFull(win)
        self.assertEqual(self.notifyCalled, 1)

    def test__unregister(self):
        self.notifyCalled = 0
        win = self.window
        win.registerObserver(self)
        _fillWindowFull(win)
        self.assertEqual(self.notifyCalled, 1)
                
        win.unregisterObserver(self)
        _fillWindowFull(win)
        self.assertEqual(self.notifyCalled, 1) 


class HammingSignalWindowTest(unittest.TestCase):

    def setUp(self):
        self.window = HammingSignalWindow(WINDOW_SIZE, ["X"])

    def notify(self, data):
        self.notifyCalled += 1

    def test_windowsFilled(self):        
        self.assertEquals(self.window.window, INIT_WINDOW)
        
        _fillValues(self.window, WINDOW_SIZE / 2)
        self.assertEquals(self.window.window, {"X": {'quality': [0, 1], 'value': [0, 1]}}) 
        
        _fillValues(self.window, WINDOW_SIZE, WINDOW_SIZE / 2)
        self.assertEquals(self.window.window, INIT_WINDOW) 

    def test__register(self):
        self.notifyCalled = 0
        win = self.window
        win.registerObserver(self)
        _fillWindowFull(win)
        self.assertEqual(self.notifyCalled, 1)

    def test__unregister(self):
        self.notifyCalled = 0
        win = self.window
        win.registerObserver(self)
        _fillWindowFull(win)
        self.assertEqual(self.notifyCalled, 1)
                
        win.unregisterObserver(self)
        _fillWindowFull(win)
        self.assertEqual(self.notifyCalled, 1) 
        
if __name__ == '__main__':
    unittest.main()












    
