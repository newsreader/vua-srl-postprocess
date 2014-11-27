#!/usr/bin/env python

from KafNafParserPy import *

from rdflib import URIRef, Namespace
from rdflib.namespace import RDF,Namespace, NamespaceManager
from rdflib.graph import Graph    
import sys
import os

path='/mnt/scistor0/Cars/Cars-new-out'


# Add the relevant namespaces: OWL and NWR
OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
NWR_NS = Namespace('http://www.newsreader-project.eu/domain-ontology#')
namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('owl', OWL_NS, override=False)
namespace_manager.bind('nwr', NWR_NS)

# predicate counters
predicates_total = 0
predicates_eso = 0
predicates_pos_fn = 0
predicates_neg_fn = 0
predicates_fn_total = 0
predicates_vn_total = 0
predicates_wn_total = 0
predicates_pb_total = 0

# role counters
roles_total = 0
roles_eso = 0
roles_pos_fn = 0
roles_neg_fn = 0
roles_fn_total = 0
roles_vn_total = 0
roles_wn_total = 0
roles_pb_total = 0

w=open("log.txt", "w")

for root, dirs, files in os.walk(path):
    
    for inputfile in files:
        
        try:    
            # Parse using the KafNafParser
            my_parser = KafNafParser(root + "/" + inputfile)    
        except:
            w.write(root + "/" + inputfile)
            continue

        g = Graph()
        g.namespace_manager = namespace_manager
        
        # Parse the ESO ontology
        g1 = g.parse("ESO.owl")

    
        # Iterate over the predicates and check for ESO predicates in the external references
        for predicate in my_parser.get_predicates():
            pred_id = predicate.get_id()
            predicates_total+=1
            for ext_ref in predicate.get_external_references():
                if ext_ref.get_resource()=='ESO':
                    predicates_eso+=1
                    eso_property = ext_ref.get_reference()
                    for single_res in predicate.get_external_references():
                        if single_res.get_resource()=='FrameNet':
                            fn_pred = single_res.get_reference()
                            # Check if the ESO predicate coresponds to this FrameNet predicate
                            pred_res = g1.query('SELECT * WHERE { nwr:' + eso_property + ' nwr:correspondToFrameNetFrame "http://www.newsreader-project.eu/framenet#' + fn_pred + '" }', initNs={ 'owl': OWL_NS, 'nwr': NWR_NS })
                            # Depending on the query results, add "+" or "-"
                            if len(pred_res)>0:
                                single_res.set_resource(single_res.get_resource() + "+")
                                predicates_pos_fn+=1
                            else:
                                single_res.set_resource(single_res.get_resource() + "-")
                                predicates_neg_fn+=1
                elif ext_ref.get_resource()=='FrameNet':
                    predicates_fn_total+=1
                elif ext_ref.get_resource()=='VerbNet':
                    predicates_vn_total+=1
                elif ext_ref.get_resource()=='WordNet':
                    predicates_wn_total+=1
                elif ext_ref.get_resource()=='PropBank':
                    predicates_pb_total+=1
                    
                # When there is an ESO choice, iterate through the roles and identify the right FrameNet meanings there as well
            for role in predicate.get_roles():
                roles_total+=1
                for role_ext_ref in role.get_external_references():
                    if role_ext_ref.get_resource()=='ESO':
                        roles_eso+=1
                        eso_property2 = role_ext_ref.get_reference().split("@")
                        for other_res in role.get_external_references():
                            if other_res.get_resource()=='FrameNet':
                                fn_ref = other_res.get_reference().split("@")
                                # Check if both the predicate and the role correspond between ESO and FrameNet
                                role_res = g1.query('SELECT * WHERE { nwr:' + eso_property2[0] + ' nwr:correspondToFrameNetFrame "http://www.newsreader-project.eu/framenet#' + fn_ref[0] + '" . nwr:' + eso_property2[1] + ' nwr:correspondToFrameNetElement "http://www.newsreader-project.eu/framenet#' + fn_ref[1] + '" }', initNs={ 'owl': OWL_NS, 'nwr': NWR_NS })
                                if len(role_res)>0:
                                    other_res.set_resource(other_res.get_resource() + "+")
                                    roles_pos_fn+=1
                                else:
                                    other_res.set_resource(other_res.get_resource() + "-")
                                    roles_neg_fn+=1
                    elif role_ext_ref.get_resource()=='FrameNet':
                        roles_fn_total+=1
                    elif role_ext_ref.get_resource()=='VerbNet':
                        roles_vn_total+=1
                    elif role_ext_ref.get_resource()=='WordNet':
                        roles_wn_total+=1
                    elif role_ext_ref.get_resource()=='PropBank':
                        roles_pb_total+=1
        
        
print "##### Predicates #####"

print "Total predicates: " + str(predicates_total)
print "Predicates with ESO: " + str(predicates_eso)
print "Percentage of ESO predicates: " + str(predicates_eso*100.0/predicates_total) + "%"
print "Positive FrameNet cases: " + str(predicates_pos_fn)
print "Negative FrameNet cases:" + str(predicates_neg_fn)
print "Unjudged FrameNet cases: " + str(predicates_fn_total-predicates_pos_fn-predicates_neg_fn)

print "Total FrameNet predicates: " + str(predicates_fn_total) + ". FN predicates per mention: " + str(predicates_fn_total*1.0/predicates_total)
print "Total VerbNet predicates: " + str(predicates_vn_total) + ". VN predicates per mention: " + str(predicates_vn_total*1.0/predicates_total)
print "Total WordNet predicates: " + str(predicates_wn_total) + ". WN predicates per mention: " + str(predicates_wn_total*1.0/predicates_total)
print "Total PropBank predicates: " + str(predicates_pb_total) + ". PB predicates per mention: " + str(predicates_pb_total*1.0/predicates_total)

print "##### Roles #####"

print "Total roles: " + str(roles_total)
print "Roles with ESO: " + str(roles_eso)
print "Percentage of ESO roles: " + str(roles_eso*100.0/roles_total) + "%"
print "Positive FrameNet cases: " + str(roles_pos_fn)
print "Negative FrameNet cases:" + str(roles_neg_fn)
print "Unjudged FrameNet cases: " + str(roles_fn_total-roles_pos_fn-roles_neg_fn)

print "Total FrameNet roles: " + str(roles_fn_total) + ". FN roles per mention: " + str(roles_fn_total*1.0/roles_total)
print "Total VerbNet roles: " + str(roles_vn_total) + ". VN roles per mention: " + str(roles_vn_total*1.0/roles_total)
print "Total WordNet roles: " + str(roles_wn_total) + ". WN roles per mention: " + str(roles_wn_total*1.0/roles_total)
print "Total PropBank roles: " + str(roles_pb_total) + ". PB roles per mention: " + str(roles_pb_total*1.0/roles_total)