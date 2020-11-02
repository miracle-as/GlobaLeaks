# -*- coding: utf-8
import ctypes

def set_proc_title(title):
    """
    Set the process title

    :param title: A title to be assigned to the process
    """
    libc = ctypes.cdll.LoadLibrary('libc.so.6')
    buff = ctypes.create_string_buffer(len(title) + 1)
    buff.value = title.encode()
    libc.prctl(15, ctypes.byref(buff), 0, 0, 0)
