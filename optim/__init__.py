import ctypes
import os
from ctypes import POINTER, byref, c_float, c_uint

_lib_path = os.path.join(os.path.dirname(__file__), "optim.so")

lib = ctypes.CDLL(_lib_path)

lib.crosspoint.argtypes = [POINTER(c_float), POINTER(c_float), c_uint]
lib.crosspoint.restype = c_uint


def crosspoint_np(a, b, size):
    arr_a = a.ctypes.data_as(POINTER(c_float))
    arr_b = b.ctypes.data_as(POINTER(c_float))

    volume = c_float()
    price = lib.crosspoint(arr_a, arr_b, size, byref(volume))

    return price, volume.value


crosspoint = lib.crosspoint

__all__ = ["crosspoint", "crosspoint_np"]
