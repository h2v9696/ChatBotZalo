#!/usr/bin/env python
# -*- coding: utf-8 -*-
from owlready2 import *
onto = get_ontology("../../Drink.owl")
onto.load()

if __name__ == '__main__':
    # print(list(onto.classes()))
    print(onto.search(iri = "*trà*"))
    print(onto["trà"].__subclasses__())
    print(onto["trà_oolong"].is_a)
    # if (read.isTest):
    #     for line in read.read_file('test'):
    #         print line[0] + ' ' + line[1] + ' ' + unicode(line[2], 'utf-8')
    # else:
    #     for line in read.read_file('../GR/Data/domain/product.txt'):
    #         print line[0] + ' ' + unicode(line[1], 'utf-8')
