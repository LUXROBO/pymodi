# -*- coding: utf-8 -*-

"""Json Box module."""

from __future__ import absolute_import

class JsonBox:
    def __init__(self):
        self._buffer = str()
        self._json = str()

    def add(self, data):
        self._buffer += data

    def has_json(self):
        end = self._buffer.find('}')

        if end >= 0:
            start = self._buffer.rfind('{', 0, end)

            if start >= 0:
                self._json = self._buffer[start:end+1]
                self._buffer = self._buffer[end+1:]

                return True
            else:
                self._buffer = self._buffer[end+1:]

                return False
        else:
            start = self._buffer.rfind('{')

            if start >= 0:
                self._buffer = self._buffer[start:]
            else:
                self._buffer = ""

            return False

    @property
    def json(self):
        return self._json
