#!/usr/bin/python

import sys, os
import threading
from time import sleep
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_collector import EEGDataCollector
from util.eeg_data_converter import EEGTableToPacketConverter





WINDOW_SIZE = 4
FIELDS = ["F3", "F4", "X", "Y"]

class DataCollectorTest(unittest.TestCase):

    def setUp(self):
        source = EEGTableToPacketConverter()
        source.convert()
        self.collector = EEGDataCollector(source, FIELDS, WINDOW_SIZE)
        dataHandler = lambda x: x
        self.collector.setHandler(dataHandler)
        self.notifyCalled = 0

    def notify(self, data):
        self.notifyCalled += 1

    def _fillValues(self, count):
        data = self.collector.datasource.data
        fields = self.collector.fields
        for i in range(count):
            row = data[i].sensors
            fData = {x: row[x] for x in fields}
            self.collector._addData(fData)

    def _fillWindowFull(self):
        self._fillValues(WINDOW_SIZE)

    def getInitWindow(self):
        d = {}
        for key in FIELDS:
            d[key] = {"value": [], "quality": []} 
        return d

    def test_windowsFilled(self):
        initWindow = self.getInitWindow()
                
        win1 = self.collector.windows[0]
        win2 = self.collector.windows[1]
        
        self.assertEquals(win1.index, WINDOW_SIZE / 2)
        self.assertEquals(win1.window, initWindow)
        self.assertEquals(win2.index, 0)
        self.assertEquals(win2.window, initWindow)
        
        self._fillValues(WINDOW_SIZE / 2)
        self.assertEquals(win1.window, initWindow)
        self.assertEquals(win1.index, 0) 
        self.assertEquals(win2.index, WINDOW_SIZE / 2)
        self.assertEquals(win2.window["X"], {'quality': [0, 0], 'value': [24.0, 24.0]})

        self._fillValues(WINDOW_SIZE / 2)
        self.assertEquals(win1.index, 2) 
        self.assertEquals(win2.window, initWindow) 

    def test_addData(self):
        win1, win2 = self.collector.windows
        win1.registerObserver(self)
        win2.registerObserver(self)
        
        self.assertEqual(self.notifyCalled, 0)
        
        # stop populating after 1 round
        collectorThread = threading.Thread(target=self.collector.collectData)
        collectorThread.start()
        
        sleep(0.1)
        self.collector.close()
        collectorThread.join()

        self.assertTrue(self.notifyCalled > 0)

    def test_filter(self):
        fields = ["F3", "X"]
        self.collector.fields = fields
        
        data = self.collector.datasource.data;
        
        filteredData = self.collector._filter(data[0].sensors)
        
        self.assertEqual(len(filteredData), len(fields))
        self.assertTrue(set(filteredData.keys()).issubset(set(fields)))
        self.assertTrue(set(filteredData.keys()).issuperset(set(fields)))

if __name__ == '__main__':
    unittest.main()