# -*- coding: utf-8 -*-
'''
  This module includes functions to:
    Audit attributes,
    Count the type of key values, and
    Show inconsistencies for the cleaning process.
'''

import xml.etree.cElementTree as ET
import re
from pprint import pprint
from datetime import datetime

lower = re.compile(r'^([a-z]|-|_)*$')
lower_colon = re.compile(r'^([a-z]|-|_)*:([a-z]|-|_)*$')

def audit_attribs(attribs,types,schars):
  ''' Audit attributes according to the types and schars parameters.
  
  Args:
    attribs (dict): element attributes.
    types (dict): data types as keys and list of attributes as values.
    schars (str): special characters.
  
  Returns:
    NoneType.
  '''
  
  for attrib in attribs:
    try:
      if attrib in types['int']:
        int(attribs[attrib])
      elif attrib in types['float']:
        float(attribs[attrib])
      elif attrib in types['timestamp']:
        datetime.strptime(attribs[attrib],"%Y-%m-%dT%H:%M:%SZ")
      elif attrib in types['string']:
        for c in schars:
          if c in attribs[attrib]:
            print('Special char',c, 'found in : ',attribs[attrib])
      elif attrib in types['unaudited']:
        continue
      else:
        print('Attribute type not covered!\nAttr: '+attrib)
    except:
        print("Can't convert the value: ", attribs[attrib],'\nAttrib: ',attrib)

def audit_keys(k_value,keys):
  '''Classify and count the type of a key value and save on a dict.
  
  Args:
    k_value (str): key value.
    keys (dict): dictionary to count the classification and store the other keys occurence.
  
  Returns:
    dict: increased keys parameter.
  '''

  if lower.match(k_value):
    keys['lower'] += 1
  elif lower_colon.match(k_value):
    keys['lower_colon'] += 1
  elif k_value.count(':') > 1:
    keys['lower_multi_colon'] += 1
  else:
    keys['other'][0] += 1
    keys['other'][1].add(k_value)
  
  return keys

def audit(filename,types,schars):
  ''' Audit xml file with audit_attribs and audit_keys functions.
  
  Args:
    filename (str): xml file.
    types (dict): data types as keys and list of attributes as values.
    schars (str): special characters.

  Returns:
    dict: count of key types and list of "other" keys.
  '''
  
  print("Auditing...")
  keys = {"lower": 0
          ,"lower_multi_colon": 0
          ,"lower_colon": 0
          ,"other": [0,set([])]
         }
  for _,element in ET.iterparse(filename):
    if element.tag not in ('osm','note','meta','bounds'):
      audit_attribs(element.attrib,types,schars)
    
    if element.tag == 'tag':
      keys=audit_keys(element.attrib['k'],keys)
  
  return keys

if __name__ == "__main__":
  FILE = "area.osm"
  schars = '!"#$%&\'()*+,./;<=>?@[\\]^`{|}~ç\t\r\n'
  data_types={'int':['id','version','changeset','uid','ref']
             ,'float':['lat','lon']
             ,'timestamp':['timestamp']
             ,'string':['type','role','k']
             ,'unaudited':['user','v']
            }
  
  keys = audit(FILE,data_types,schars)
  pprint(keys)
  print('Done!!!')
