#!/usr/bin/env python

from KafNafParserPy import *

from rdflib import URIRef, Namespace
from rdflib.namespace import RDF,Namespace, NamespaceManager
from rdflib.graph import Graph    
import sys, getopt

if __name__ == '__main__':

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

    # We create the parser object
    my_parser = KafNafParser(inputfile)    

    OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
    NWR_NS = Namespace('http://www.newsreader-project.eu/domain-ontology#')
    namespace_manager = NamespaceManager(Graph())
    namespace_manager.bind('owl', OWL_NS, override=False)
    namespace_manager.bind('nwr', NWR_NS)
    g = Graph()
    g.namespace_manager = namespace_manager
    
    g1 = g.parse("ESO.owl")

    
    eso_counter=0
    non_eso_counter=0
    
    # Iterate over the entities and print some information
    for predicate in my_parser.get_predicates():
        eso_found=False
        pred_id = predicate.get_id()
        for ext_ref in predicate.get_external_references():
            if ext_ref.get_resource()=='ESO':
                eso_found=True
                eso_property = ext_ref.get_reference()
                for single_res in predicate.get_external_references():
                    if single_res.get_resource()=='FrameNet':
                        fn_pred = single_res.get_reference()
                        pred_res = g1.query('SELECT * WHERE { nwr:' + eso_property + ' nwr:correspondToFrameNetFrame "http://www.newsreader-project.eu/framenet#' + fn_pred + '" }', initNs={ 'owl': OWL_NS, 'nwr': NWR_NS })

                        if len(pred_res)>0:
                            single_res.set_resource(single_res.get_resource() + "+")
                        else:
                            single_res.set_resource(single_res.get_resource() + "-")
                                
                # When there is an ESO choice, iterate through the roles and identify the right meanings there as well
                for role in predicate.get_roles():
                    for role_ext_ref in role.get_external_references():
                        if role_ext_ref.get_resource()=='ESO':
                            eso_property2 = role_ext_ref.get_reference().split("@")
                            for other_res in role.get_external_references():
                                if other_res.get_resource()=='FrameNet':
                                    fn_ref = other_res.get_reference().split("@")
                                    role_res = g1.query('SELECT * WHERE { nwr:' + eso_property2[0] + ' nwr:correspondToFrameNetFrame "http://www.newsreader-project.eu/framenet#' + fn_ref[0] + '" . nwr:' + eso_property2[1] + ' nwr:correspondToFrameNetElement "http://www.newsreader-project.eu/framenet#' + fn_ref[1] + '" }', initNs={ 'owl': OWL_NS, 'nwr': NWR_NS })
                                    if len(role_res)>0:
                                        other_res.set_resource(other_res.get_resource() + "+")
                                    else:
                                        other_res.set_resource(other_res.get_resource() + "-")
                                            
        if eso_found:
            eso_counter+=1
        else:
            non_eso_counter+=1
            
    print "Predicates with ESO: " + str(eso_counter) + ", predicates without ESO: " + str(non_eso_counter) + ". Usability rate: " + str(100.0*eso_counter/(eso_counter+non_eso_counter)) + "%"        
            
    my_parser.dump(outputfile)