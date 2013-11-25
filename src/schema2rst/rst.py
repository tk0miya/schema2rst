# -*- coding: utf-8 -*-

import io
import sys
import six
import unicodedata


def string_width(string):
    width = 0
    for c in string:
        char_width = unicodedata.east_asian_width(c)
        if char_width in six.u("WFA"):
            width += 2
        else:
            width += 1

    return width


class RestructuredTextGenerator:
    def __init__(self, output=None):
        if output:
            self.output = io.open(output, 'w', encoding='utf-8')
        else:
            self.output = io.open(sys.stdout.fileno(), 'w', encoding='utf-8')

    def out(self, string):
        self.output.write(string + six.u("\n"))

    def header(self, string, char=six.u("=")):
        self.out(six.u(""))
        self.out(string)
        self.out(char * string_width(string))
        self.out(six.u(""))

    def listtable(self, header=None):
        self.out(six.u(".. list-table::"))
        if header:
            self.out(six.u("   :header-rows: 1"))

        self.out(six.u(""))

        if header:
            self.listtable_column(header)

    def listtable_column(self, columns):
        for i, column in enumerate(columns):
            if i == 0:
                self.out(six.u("   * - %s") % column)
            else:
                self.out(six.u("     - %s") % column)

    def list_item(self, item):
        self.out(six.u("* %s") % item)
