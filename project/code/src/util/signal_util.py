#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 10.05.2016

:author: Paul Pasler
:organization: Reutlingen University
'''

from itertools import groupby

from numpy import array, count_nonzero, mean, var, isnan, where, hstack, ones, NAN
from scipy.ndimage.morphology import binary_closing
from scipy.signal import butter, lfilter

MAX_ZERO_SEQUENCE_LENGTH = 3
MAX_SEQUENCE_LENGTH = 3

class SignalUtil(object):

    def __init__(self):
        """This class does signal processing with raw signals"""

    def normalize(self, data):
        '''normalizes data between -1 and 1

        :param numpy.array data: list of values
        
        :return: normalized data
        :rtype: numpy.array
        '''
        if count_nonzero(data) == 0:
            return data

        extreme = float(max(max(data), abs(min(data))))

        return data / extreme

    def maximum(self, data):
        '''calculates the signal max 

        :param numpy.array data: list of values
        
        :return: signal maximum
        :rtype: float
        '''
        return max(data)

    def minimum(self, data):
        '''calculates the signal min

        :param numpy.array data: list of values
        
        :return: signal minimum
        :rtype: float
        '''
        return min(data)

    def mean(self, data):
        '''calculates the signal mean

        :param numpy.array data: list of values
        
        :return: signal mean
        :rtype: float
        '''
        return mean(data)

    def energy(self, data):
        '''calculates signal energy 
        
        :math:`E = \sum(data^2)`
        
        * `Energy_(signal_processing) <https://en.wikipedia.org/wiki/Energy_(signal_processing)>`_
        
        :param numpy.array data: list of values
        
        :return: signal energy
        :rtype: float
        '''
        return sum(data ** 2)

    def var(self, data):
        '''calculates the signal varaince

        :param numpy.array data: list of values
        
        :return: signal variance
        :rtype: float
        '''
        return var(data)

    def countZeros(self, data):
        '''calculates the number of countZeros in data

        :param numpy.array data: list of values
        
        :return: zero count
        :rtype: int
        '''
        return len(data) - count_nonzero(data)

    def countNans(self, data):
        '''calculates the number of NaNs in data

        :param numpy.array data: list of values
        
        :return: NaN count
        :rtype: int
        '''
        return count_nonzero(isnan(data))

    def replaceZeroSequences(self, data):
        '''replaces zero sequences, which is an unwanted artefact, with NaN 
        see http://stackoverflow.com/questions/38584956/replace-a-zero-sequence-with-other-value

        :param numpy.array data: list of values

        :return: zero sequences replaced data
        :rtype: numpy.array
        '''
        a_extm = hstack((True,data!=0,True))
        mask = a_extm == binary_closing(a_extm,structure=ones(MAX_ZERO_SEQUENCE_LENGTH))
        return where(~a_extm[1:-1] & mask[1:-1],NAN, data)

    def countSequences(self, data):
        seqList = self._getSequenceList(data)
        return len([s for s in seqList if len(s) >= MAX_SEQUENCE_LENGTH])

    def replaceSequences(self, data):
        '''replaces any sequences of more than MAX_SEQUENCE_LENGTH same numbers in a row with NaN 
        see http://stackoverflow.com/questions/38584956/replace-a-zero-sequence-with-other-value

        :param numpy.array data: list of values

        :return: sequences replaced data
        :rtype: numpy.array
        '''
        seqList = self._getSequenceList(data)
        return array( [ item for l in seqList for item in l ] )

    def _getSequenceList(self, data):
        return array([self._getSequence(value, it) for value, it in groupby(data)])

    def _getSequence(self, value, it):
        itLen = sum(1 for _ in it) # length of iterator
    
        if itLen>=MAX_SEQUENCE_LENGTH:
            return [ NAN ]*itLen
        else:
            return [ value ]*itLen

    def butterBandpass(self, lowcut, highcut, samplingRate, order=5):
        '''
        Creates a butterworth filter design from lowcut to highcut and returns the filter coefficients
        :see: `scipy.signal.butter <http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html#scipy.signal.butter>`_

        note: :math:`lowcut >= 0` and :math:`highcut <= samplingRate / 2`

        :param int lowcut: lower border
        :param int highcut: upper border
        :param int samplingRate: sample frequency
        
        :return: filter coefficients a, b
        :rtype: float
        '''
        # TODO throw exception here? 
        if highcut > samplingRate / 2:
            highcut = samplingRate / 2
        if lowcut < 0:
            lowcut = 0
        
        nyq = 0.5 * samplingRate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a
    
    
    def butterBandpassFilter(self, data, lowcut, highcut, samplingRate, order=5):
        b, a = self.butterBandpass(lowcut, highcut, samplingRate, order)
        y = lfilter(b, a, data)
        return y
