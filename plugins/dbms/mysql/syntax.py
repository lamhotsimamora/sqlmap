#!/usr/bin/env python2

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import binascii

from lib.core.common import getUnicode
from lib.core.convert import getBytes
from lib.core.convert import getOrds
from plugins.generic.syntax import Syntax as GenericSyntax

class Syntax(GenericSyntax):
    @staticmethod
    def escape(expression, quote=True):
        """
        >>> Syntax.escape("SELECT 'abcdefgh' FROM foobar") == "SELECT 0x6162636465666768 FROM foobar"
        True
        >>> Syntax.escape(u"SELECT 'abcd\xebfgh' FROM foobar") == "SELECT CONVERT(0x61626364c3ab666768 USING utf8) FROM foobar"
        True
        """

        def escaper(value):
            if all(_ < 128 for _ in getOrds(value)):
                return "0x%s" % getUnicode(binascii.hexlify(getBytes(value)))
            else:
                return "CONVERT(0x%s USING utf8)" % getUnicode(binascii.hexlify(getBytes(value)))

        return Syntax._escape(expression, quote, escaper)
