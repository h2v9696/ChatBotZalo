#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ReadData(object):
    def __init__(self, _isTest = False):
        self.data = None
        self.isTest = _isTest

    def process_string_test(self, line):
        s = line.split(' : ')
        label1 = s[0]
        rest = s[1].split(' ', 1)
        label2 = rest[0]
        string = rest[1]
        content = [label1, label2, string]
        return content

    def process_string(self, line):
        s = line.split(' , ')
        label = s[0]
        data = s[1]
        content = [label, data]
        return content

    def read_file(self, path):
        f=open(path, "r")
        contents = []
        if f.mode == 'r':
            lines = f.readlines()
            for line in lines:
                if (self.isTest):
                    content = self.process_string_test(line)
                else:
                    content = self.process_string(line)
                contents.append(content)
        return contents

#test
if __name__ == '__main__':
    read = ReadData(True)
    # if (read.isTest):
    #     for line in read.read_file('test'):
    #         print line[0] + ' ' + line[1] + ' ' + unicode(line[2], 'utf-8')
    # else:
    #     for line in read.read_file('../GR/Data/domain/product.txt'):
    #         print line[0] + ' ' + unicode(line[1], 'utf-8')
