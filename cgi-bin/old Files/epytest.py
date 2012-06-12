#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module **foobar** serves as an *example* of documentation style for
**Python** using Docutils_' reStructuredText_ as markup language.

.. _Docutils: http://docutils.sourceforge.net/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html

..  This is a comment, the following line too.
    The following fields define some module metadata.

:date: '2009-08-07'
:authors:
    - Walter
    - Walterina
:see:
    - http://docutils.sourceforge.net/docs/user/rst/quickref.html
"""

__version__ = '0.1'
__license__ = 'GNU General Public License 3'
__docformat__ = 'restructuredtext en'

# Recommended order of imports is (alphabetically sorted in each group):
# - standard library
# - third party libraries
# - internal modules
# Also:
# - "import a.b" is preferred over "from a import b"
# - "from a import b" is preferred over "from a import *"

import logging
import os
import sys

import simplejson

# Constants are written ALL_IN_CAPS
# Variables are written in lowercase_with_underscore
# Internals are preceded with an underscore

CONNECTION_TIMEOUT = 60
_WORD_PATTERN = re.compile(r'\w+')
last_modified = datetime.utcnow()
_item_cache = {}

class Walter(object):
    """
    Model for a Walter sprite in a virtual world.

    Walters can do amazing stuff such as walking and pushing boxes.
    """

    _instance_count = 0 # a class variable
    """:cvar: Some class variable."""

    _avatar = None # an instance variable
    """:ivar: Some instance variable."""

    def __init__(self, avatar, lives=0, **kwargs):
        """
        `Walter` initializer.

        Initializing a `Walter` is extremely funny. You should try it!

        :parameters:
          avatar : unicode
            An identifier for `Walter`'s appearance.
          lives : int
            Number of lives `Walter` initially has.

        :keywords:
          position : tuple(int, int)
            `Walter`'s position in a 2-tuple.

        :exceptions:
          - `ValueError`: Raised when `lives` is less than ``0``.

        :note:
          You should write class names between backtics (`````), as in
          ```Walter``` to get links to that object as in `Walter`.
        """
        self._avatar = avatar
        if lives < 0:
            raise ValueError(lives)
        self._lives = lives
        self._position = kwargs.get('position', (0, 0))

    def move(self, direction='up'):
        """
        Makes `Walter` move one step towars given `direction`.

        :return: `True` if `Walter` could move. `False` otherwise.

        :parameters:
          direction : str
            Determines the direction where to move.

            Posible values are:

              - ``'up'``
              - ``'left'``
              - ``'down'``
              - ``'right'``
        """
        dx, dy = self._can_move(direction)
        if None in (dx, dy):
            return False
        self._position = (self._position[0] + dx, self._position[1] + dy)
        return True

# NOTE:
# the only non-empty lines before the module docstring may be:
#   - shebang (#!/usr/bin/env python)
#   - file encoding line (# -*- coding: utf-8 -*-)
#   - __future__ imports 
