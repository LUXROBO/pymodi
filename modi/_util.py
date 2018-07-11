# -*- coding: utf-8 -*-

"""Util module."""

from __future__ import absolute_import

def append_hex(a, b):
    sizeof_b = 0

    while((b >> sizeof_b) > 0):
        sizeof_b += 1

    sizeof_b += sizeof_b % 4

    return (a << sizeof_b) | b