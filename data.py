#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "edinburgh_scotland.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
# PROBLEMCHARS = re.compile(r'[=\+/&<>\'"\?%#$@\,\. \t\r\n]')
PROBLEMCHARS = re.compile(r'[:;,]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    tag_detail = {}
    
    if element.tag == 'node':
        node_attribs = populate_attributes(element, NODE_FIELDS)
        
        tags = populate_tags(element, node_attribs['id'])
        
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        way_attribs = populate_attributes(element, WAY_FIELDS)
        
        tags = populate_tags(element, way_attribs['id'])
                
        tag_detail = {}
        i = 0
        for tag in element.findall('nd'):
            for key, value in tag.attrib.items():
                tag_detail['id'] = way_attribs['id']
                if key == 'ref':
                    tag_detail['node_id'] = value
                    tag_detail['position'] = i
                    i += 1
            way_nodes.append(tag_detail.copy())

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               User-Defind Helper Functions         #
# ================================================== #
# https://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
def is_ascii(my_string):
    '''detects the presence of non-ascii characters in my_string'''
    if isinstance(my_string, unicode):
        try:
            my_string.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            my_string.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True

def is_compound_value(value):
    '''check if the passed in value contains values separated by a : or ;'''
    m = PROBLEMCHARS.search(value)
    if m:
        return True
    else:
        return False

# dictionary for converting key values to another key value already present in
# the data that has the same meaning
synonym_mapping = {'postal_code' : 'postcode',
                    'url' : 'website'}

synonym_keys = ['postal_code', 'url']


def has_synonym_key(value):
    '''check if the value is in the list of values that will be swapped for
    another existing value'''
    if value in synonym_keys:
        return True
    else:
        return False


def update_synonym_key_value(name, mapping):
   name = name.replace(name, mapping[name])

   return name


def is_source_key(tag):
    return tag['key'] == 'source'


# iterates over the elements object and adds entries for any key that is in the
# list of attr_fields that is passed in
def populate_attributes(element, attr_fields):
    '''iterates over the elements object and adds entries for any key that is in
    the list of attr_fields that is passed in'''
    attrib_dict = {}
    for key, value in element.attrib.items():
        if is_ascii(key) and is_ascii(value):
            if key in attr_fields:
                attrib_dict[key] = value

    return attrib_dict


def populate_tags(element, parent_id):
    '''iterates over the element object and adds entries for any tags'''
    tags = []
    tag_detail = {}
    for tag in element.findall('tag'):
        for key, value in tag.attrib.items():
            # include only key value pairs that use only ascii characters
            if is_ascii(key) and is_ascii(value):
                tag_detail['id'] = parent_id
                
                if key == 'k':
                    if not is_compound_value(value):
                        
                        # check if the value is one that will be updated with some other
                        # value
                        if has_synonym_key(value):
                            value = update_synonym_key_value(value, synonym_mapping)

                        tag_detail['key'] = value
                        tag_detail['type'] = 'regular'
                    else:
                        # split key on : and assign second element as the key
                        # and the first (and third if it exists) elements as the type
                        key_strs = value.split(':')
                        # check if the value is one that will be updated with some other
                        # value
                        if has_synonym_key(key_strs[1]):
                            key_strs[1] = update_synonym_key_value(key_strs[1], synonym_mapping)
                        
                        if len(key_strs) == 3:
                            tag_detail['key'] = key_strs[1]
                            tag_detail['type'] = key_strs[0] + ':' + key_strs[2]
                        else:
                            tag_detail['key'] = key_strs[1]
                            tag_detail['type'] = key_strs[0]
                elif key == 'v':
                    if not is_compound_value(value):
                        tag_detail['value'] = value
                    else:
                        # if key=source then split the value on any ; in the string.
                        # Only use the first element as the value (e.g.
                        # Bing;survey becomes Bing)
                        if is_source_key(tag_detail):
                            val_strs = value.split(';')[0]
                            tag_detail['value'] = val_strs
                        else:
                            tag_detail['value'] = value
                            
        tags.append(tag_detail.copy())
    return tags


# ================================================== #
#               Provided Helper Functions            #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """""Modified to just return True or False"""
    return validator.validate(element, schema)
    

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in
            row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    if validate_element(el, validator):
                        if element.tag == 'node':
                            nodes_writer.writerow(el['node'])
                            node_tags_writer.writerows(el['node_tags'])
                        elif element.tag == 'way':
                            ways_writer.writerow(el['way'])
                            way_nodes_writer.writerows(el['way_nodes'])
                            way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
