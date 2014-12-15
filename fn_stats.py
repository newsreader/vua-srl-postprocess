#!/usr/bin/env python

from KafNafParserPy import *

from rdflib import URIRef, Namespace
from rdflib.namespace import RDF,Namespace, NamespaceManager
from rdflib.graph import Graph    
import sys
import os

path='example'

predicates_pos_fn = 0
predicates_neg_fn = 0
predicates_fn_total=0

roles_pos_fn = 0
roles_neg_fn = 0
roles_fn_total=0

for root, dirs, files in os.walk(path):
    
    for inputfile in files:
        
        try:    
            # Parse using the KafNafParser
            my_parser = KafNafParser(root + "/" + inputfile)    
        except:
            continue

        # Iterate over the predicates and check for ESO predicates in the external references
        for predicate in my_parser.get_predicates():
            for ext_ref in predicate.get_external_references():
                if ext_ref.get_resource()=='FrameNet+':
                    predicates_pos_fn+=1
                elif ext_ref.get_resource()=='FrameNet-':
                    predicates_neg_fn+=1
                elif ext_ref.get_resource()=='FrameNet':
                    predicates_fn_total+=1
                    
                # When there is an ESO choice, iterate through the roles and identify the right FrameNet meanings there as well
            for role in predicate.get_roles():
                for role_ext_ref in role.get_external_references():
                    if role_ext_ref.get_resource()=='FrameNet+':
                        roles_pos_fn+=1
                    elif role_ext_ref.get_resource()=='FrameNet-':
                        roles_neg_fn+=1
                    elif role_ext_ref.get_resource()=='FrameNet':
                        roles_fn_total+=1
        
        
print "Positive FrameNet predicates: " + str(predicates_pos_fn)
print "Negative FrameNet predicates:" + str(predicates_neg_fn)
print "Unjudged FrameNet predicates: " + str(predicates_fn_total)


print "Positive FrameNet roles: " + str(roles_pos_fn)
print "Negative FrameNet roles:" + str(roles_neg_fn)
print "Unjudged FrameNet roles: " + str(roles_fn_total)
