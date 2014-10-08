from ctypes import *
from math import log

dll = CDLL('magic.so')

MAX_LENGTH = 4096

class Model(Structure):
    _fields_ = [
        ('length', c_int),
        ('bits', c_int),
        ('keys', c_ulonglong * MAX_LENGTH),
        ('values', c_ulonglong * MAX_LENGTH),
    ]

dll.magic_search.restype = c_ulonglong
dll.magic_search.argtypes = [POINTER(Model), c_double, c_double, c_int]

def magic_search(mapping, bits_delta=0):
    model = Model()
    model.length = len(mapping)
    model.bits = int(log(model.length) / log(2)) - bits_delta
    # print model.length, model.bits
    for i, (key, value) in enumerate(mapping.items()):
        model.keys[i] = key
        model.values[i] = value
    return dll.magic_search(byref(model), 10, 1, 10000000)

dll.magic_search_random.restype = c_ulonglong
dll.magic_search_random.argtypes = [POINTER(Model)]

def magic_search_random(mapping, bits_delta=0):
    model = Model()
    model.length = len(mapping)
    model.bits = int(log(model.length) / log(2)) - bits_delta
    # print model.length, model.bits
    for i, (key, value) in enumerate(mapping.items()):
        model.keys[i] = key
        model.values[i] = value
    return dll.magic_search_random(byref(model))
