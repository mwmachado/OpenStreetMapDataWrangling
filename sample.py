# -*- coding: utf-8 -*-
'''
  This module includes functions to:
    Open an xml file,
    Study its structure, and
    Generate samples files.
'''

import xml.etree.ElementTree as ET
from pprint import pprint

def open_xml(file):
  '''Open a xml file and return the root element.
  
  Args:
    file (str): xml file name.
  
  Returns:
    xml.etree.ElementTree.Element: xml root element.
  '''
  
  print('Openning the file...')
  return ET.parse(file).getroot()

def count_elements(root):
  '''Count the first level sub-elements tags from an element (root).
  
  Args:
    root (xml.etree.ElementTree.Element): xml root element.
  
  Returns:
    dict: first level sub-elements tags and their occurence.
  '''
  
  print('Counting first level tags...')
  tags = {}
  for elem in root:
    if elem.tag not in tags:
      tags[elem.tag] = 1
    else:
      tags[elem.tag] += 1
  
  return tags

def rm_unused_elements(root,tags):
  '''Remove tags that just appears once from a dictionary and an xml element.
  
  Args:
    root (xml.etree.ElementTree.Element): xml root element.
    tags (dict): xml tags and their occurence.
  
  Returns:
    xml.etree.ElementTree.Element: xml root without elements that just appears once.
    dict: dictionary without elements that just appears once.
  '''
  
  print('Removing unsed tags...')
  for tag in tags.copy():
    if tags[tag] == 1:
      del tags[tag]
      root.remove(root.find(tag))
  
  return root, tags

def genealogy(root,gen={}):
  '''Get children and attributes from an xml element recursively.
  
  Args:
    root (xml.etree.ElementTree.Element): xml root element.
    gen (dict, optional): dictionary to add children of the root.
  
  Returns:
    dict: all children and attributes from an xml element.
  '''
  
  for elem in root:
    if elem.tag not in gen:
      gen[elem.tag] = {'attributes': list(elem.attrib.keys())
                        ,'children':{}
                       }
    else:
      genealogy(elem,gen[elem.tag]['children'])
  
  return gen

def sample(root,tags,k):
  '''Generate files with 1/k sample proportion for each tag (on tags) from an xml element (root).
  
  Args:
    root (xml.etree.ElementTree.Element): xml root element.
    tags (dict): xml tags for file generation.
    k (int): one sample for each k elements.
  
  Returns:
    NoneType.
  '''
  
  print('Creating samples...')
  for tag in tags:
    i = 0
    filename = tag+"_sample"+".osm" 
    with open(filename, "wb") as f:
      f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
      f.write(b"<osm>\n  ")
      for elem in root.findall(tag):
        if list(elem) and i%k==0:
          f.write(ET.tostring(elem, encoding="utf-8"))
        
        i += 1
      
      f.write(b"</osm>")
      print("Created "+filename+" with "+str(i//k)+" samples.")

if __name__ == "__main__":
  # str: xml file name.
  FILE = "area.osm"
  # int: sample proportion seed.
  K = 100
  
  root = open_xml(FILE)
  tags = count_elements(root)
  print('First Level Elements:')
  pprint(tags)
  print('Children and Attributes:')
  pprint(genealogy(root))
  root,tags = rm_unused_elements(root,tags)
  sample(root,tags.keys(),K)
  print('Done!!!')
