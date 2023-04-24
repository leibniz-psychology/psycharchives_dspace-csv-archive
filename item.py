
"""
A representation of an item in DSpace.

An item has a collection of files (aka Bitstreams) and a number of metadata name value pairs. 
"""

import os
import re
import html

class Item:
    delimiter = '||'

    def __init__(self, delimiter = '||'):
        self.delimiter = delimiter
        self._attributes = {}
        self.files = ""
        self.collections = ""

    """
    Get a dict of all attributes.
    """
    def getAttributes(self):
        return self._attributes

    """
    Set an attribute value.
    """
    def setAttribute(self, attribute, value):
        if attribute == "files":
            self.files = value
        elif attribute == "collections":
            self.collections = value
        else:
            self._attributes[attribute] = value
    """
    Get an attribute value. 
    """
    def getAttribute(self, attribute):
        return self._attributes[attribute]

    """
    Convert the item to a string
    """
    def __str__(self):
        return str(self._attributes)

    """
    Get the files (bitstreams) associated with this item.
    This function just returns the file name, with no path.
    """
    def getFiles(self):
        values = []
        files = self.files.split(self.delimiter)
        for index, file_name in enumerate(files):
            file = os.path.basename(file_name).strip()
            values.append(file)
        return values

    """
    Get the files (bitstreams) associated with this item.
    This function returns the file with the full import path.
    """
    def getFilePaths(self):
        values = []
        files = self.files.split(self.delimiter)
        for index, file_name in enumerate(files):
            file = file_name.strip()
            values.append(file)
        return values


    """
    Get the collection(s) for the individual items 
    """
    def getCollections(self):
        values = []
        handles = {'article':'20.500.12034/6', 'bachelorThesis':'20.500.12034/723', 
                    'book':'20.500.12034/4', 'bookPart':'20.500.12034/586',
                    'code':'20.500.12034/721', 'conferenceObject':'20.500.12034/7', 
                    'courseMaterial':'20.500.12034/8', 'doctoralThesis':'20.500.12034/724',
                    'habilitationTreatise':'20.500.12034/725', 'image':'20.500.12034_627',
                    'masterThesis':'20.500.12034/10', 'movingImage':'20.500.12034/626',
                    'other':'20.500.12034/720', 'preprint':'20.500.12034/718',
                    'preregistration':'20.500.12034/736', 'report':'20.500.12034/9',
                    'researchData':'20.500.12034/576', 'review':'20.500.12034/719',
                    'sound':'20.500.12034/722', 'test':'20.500.12034/12'}
                    
        collections = self._attributes['dc.type'].split(self.delimiter)
        for index, collection_name in enumerate(collections):
            collection = collection_name.strip()
            if collection in handles:
                collection = handles[collection]
            else:
                print("This Collection does not exist!")
            values.append(collection)
        return values


    """
    Get all the used schemas.
    """
    def getUsedSchemas(self):
        values = []
        for index, value in iter(self.getAttributes().items()):
            schema = self.getSchema(index)
            if schema in values:
                continue
            else:
                values.append(schema)

        return values

    """
    Returns an XML represenatation of the item.
    Extended for multiple namespaces/schemas
    """
    def toXML(self, mdschema):
        output = ""
        output += "<dublin_core schema=\"" + mdschema + "\">" + os.linesep
        #for index, value in self.getAttributes().iteritems():
        for index, value in iter(self.getAttributes().items()):
            if self.getSchema(index) != mdschema:
                continue
            tag_open = self.getOpenAttributeTag(index)
            tag_close = "</dcvalue>" + os.linesep

            values = value.split(self.delimiter)

            for val in values:
                if not val:
                    continue

                output += tag_open
                output += html.escape(val.strip(), quote=True)
                output += tag_close
        output += "</dublin_core>" + os.linesep

        return output

    """
    Get the opening XML tag for a metadata attribute.
    """
    def getOpenAttributeTag(self, attribute):
        lang = self.getAttributeLangString(attribute)
        element = self.getAttributeElementString(attribute)
        qualifier = self.getAttributeQualifierString(attribute)

        tag_open = '<dcvalue%s%s%s>' % (element, qualifier, lang)

        return tag_open

    """
    Get a string the key value pair for the lang attribute.
    eg 'language="en"'
    """
    def getAttributeLangString(self, attribute):
        match = re.search('\[(\w+)\]', attribute)

        if match != None:
            return ' language="' + html.escape(match.group(1), quote=True) + '" '
        else:
            return ''

    """
    Strip the language bit off of a metadata attribute.
    """
    def stripAttributeLang(self, attribute):
        attribs = attribute.split('[')
        return attribs[0]

    """
    Get a string of the key value pair for the element attribute.
    eg 'element="contributor"'
    """
    def getAttributeElementString(self, attribute):
        attribute = self.stripAttributeLang(attribute)
        attribs = attribute.split('.')

        if len(attribs) >= 2:
            return ' element="' + html.escape(attribs[1], quote=True) + '" '
        else:
            return ''

    """
    Get a string the key value pair for the qualifier attribute.
    eg 'qualifier="author"'
    """
    def getAttributeQualifierString(self, attribute):
        attribute = self.stripAttributeLang(attribute)
        attribs = attribute.split('.')

        if len(attribs) >= 3:
            return ' qualifier="' + html.escape(attribs[2], quote=True) + '" '
        else:
            return ''

    def getSchema(self, attribute):
        #attribute = self.stripAttributeLang(attribute)
        attribs = attribute.split('.')

        return html.escape(attribs[0].strip('_'), quote=True)