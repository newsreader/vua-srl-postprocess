#!/usr/bin/env python

from KafNafParserPy import *

from rdflib import URIRef, Namespace
from rdflib.namespace import RDF,Namespace, NamespaceManager
from rdflib.graph import Graph    
import sys, getopt

if __name__ == '__main__':

    # read the input and output NAF files
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h': #Help option
            print 'main.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"): # get input file
            inputfile = arg
        elif opt in ("-o", "--ofile"): # get output file
            outputfile = arg

    # Parse using the KafNafParser
    my_parser = KafNafParser(inputfile)    
    
    # Add the relevant namespaces: OWL and NWR
    OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
    NWR_NS = Namespace('http://www.newsreader-project.eu/domain-ontology#')
    namespace_manager = NamespaceManager(Graph())
    namespace_manager.bind('owl', OWL_NS, override=False)
    namespace_manager.bind('nwr', NWR_NS)
    g = Graph()
    g.namespace_manager = namespace_manager
    
    # Parse the ESO ontology
    g1 = g.parse("ESO.owl")

    
    # Iterate over the predicates and check for ESO predicates in the external references
    for predicate in my_parser.get_predicates():
        pred_id = predicate.get_id()
        for ext_ref in predicate.get_external_references():
            if ext_ref.get_resource()=='ESO':
                eso_property = ext_ref.get_reference()
                for single_res in predicate.get_external_references():
                    if single_res.get_resource()=='FrameNet':
                        fn_pred = single_res.get_reference()
                        # Check if the ESO predicate coresponds to this FrameNet predicate
                        pred_res = g1.query('SELECT * WHERE { nwr:' + eso_property + ' nwr:correspondToFrameNetFrame "http://www.newsreader-project.eu/framenet#' + fn_pred + '" }', initNs={ 'owl': OWL_NS, 'nwr': NWR_NS })
                        # Depending on the query results, add "+" or "-"
                        if len(pred_res)>0:
                            single_res.set_resource(single_res.get_resource() + "+")
                        else:
                            single_res.set_resource(single_res.get_resource() + "-")
                                
                # When there is an ESO choice, iterate through the roles and identify the right FrameNet meanings there as well
                for role in predicate.get_roles():
                    for role_ext_ref in role.get_external_references():
                        if role_ext_ref.get_resource()=='ESO':
                            eso_property2 = role_ext_ref.get_reference().split("@")
                            for other_res in role.get_external_references():
                                if other_res.get_resource()=='FrameNet':
                                    fn_ref = other_res.get_reference().split("@")
                                    # Check if both the predicate and the role correspond between ESO and FrameNet
                                    role_res = g1.query('SELECT * WHERE { nwr:' + eso_property2[0] + ' nwr:correspondToFrameNetFrame "http://www.newsreader-project.eu/framenet#' + fn_ref[0] + '" . nwr:' + eso_property2[1] + ' nwr:correspondToFrameNetElement "http://www.newsreader-project.eu/framenet#' + fn_ref[1] + '" }', initNs={ 'owl': OWL_NS, 'nwr': NWR_NS })
                                    if len(role_res)>0:
                                        other_res.set_resource(other_res.get_resource() + "+")
                                    else:
                                        other_res.set_resource(other_res.get_resource() + "-")

    # Dump the resulting NAF to an output file                                        
    my_parser.dump(outputfile)