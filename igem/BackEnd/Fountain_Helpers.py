import struct
import random
import os
import numpy as np
import argparse
import logging
import sys
import operator
from hashlib import md5
from reedsolo import RSCodec
from math import ceil
from math import log, floor, sqrt
import random
import json
import numpy as np
from numpy.random import RandomState
import scipy.interpolate as inter
import csv
import math

#------------------------------------------------------------------transformers------------------------------------------------------------#

def byte_to_int_array(s):
    #convert a strong like \x01\x02 to [1,2,]
    a = list()
    for t in range(0, len(s)):
        a.append(ord(s[t]))
    return a
  
def byte_to_dna(s):
    #convert byte data (\x01 \x02) to DNA data: ACTC
    bin_data = ''.join('{0:08b}'.format(s[t]) for t in range(0,len(s)))
    return bin_to_dna(bin_data)

def int_to_dna(a):
    #a is an array of integers between 0-255.
    #returns ACGGTC
    bin_data = ''.join('{0:08b}'.format(element) for element in a) #convert to a long sring of binary values
    s = ''.join(str(int(bin_data[t:t+2],2)) for t in range(0, len(bin_data),2)) #convert binary array to a string of 0,1,2,3
    return s.translate(trantab)
  
def int_to_four(a):
    #a is an array of integers between 0-255.
    #returns 0112322102
    bin_data = ''.join('{0:08b}'.format(element) for element in a) #convert to a long sring of binary values
    return ''.join(str(int(bin_data[t:t+2],2)) for t in range(0, len(bin_data),2)) #convert binary array to a string of 0,1,2,3 def four_to_dna(s):
    return s.translate(trantab)


def dna_to_byte(dna_str):
    #convert a string like ACTCA to a string of bytes like \x01 \x02
    num = dna_str.translate(revtab)
    s = ''.join('{0:02b}'.format(int(num[t])) for t in range(0, len(num),1))
    data = b''.join(bytes([int(s[t:t+8],2)]) for t in range(0, len(s), 8))

    return data
  
def dna_to_int_array(dna_str):
    #convert a string like ACTCA to an array of ints like [10, 2, 4]
    num = dna_str.translate(revtab)
    s = ''.join('{0:02b}'.format(int(num[t])) for t in range(0, len(num),1))
    data = [int(s[t:t+8],2) for t in range(0,len(s), 8)]

    return data

intab = "0123"
outtab = "ACGT"

trantab = str.maketrans(intab, outtab)
revtab = str.maketrans(outtab, intab)

#---------------------------------------------------------------------xor and other manuplations---------------------------------------#

def file_compare(f1,f2):
    l1 = len(f1)
    l2 = len(f2)
    if(l1 != l2):
        print("size not equal:",l1,l2)
    dismatch = 0
    for i in range(min(l1,l2)):
        if(f1[i] != f2[i]):
            logging.debug("byte not equal at position %d",i)
            dismatch += 1
    #if(dismatch == 0 and l1 == l2):
        #print("all the same")
    #else:
     #   print(dismatch,"dismatch")
    return dismatch