#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            user = element.attrib['user']
            if user in users:
                pass
            else:
                users.add(user)
        except:
            pass
    return users


def test():

    users = process_map('edinburgh_scotland.osm')
    pprint.pprint(users)



if __name__ == "__main__":
    test()
