#!/usr/bin/env python

from KafNafParserPy import *
import os

path='example'

which_fn_cov = {} # Frequency of the FN frames which are covered by ESO
which_fn_uncov = {} # Frequency of the FN frames which are not covered by ESO
which_eso = {} # Frequency of the ESO classes
which_no_fe = {} # Frequency of the predicate mentions (lemmas) which are not linked to FN, nor ESO

no_fe = 0 # Number of total cases with no FrameNet and no ESO

for root, dirs, files in os.walk(path):
    
    for inputfile in files:
        
        try:    
            # Parse using the KafNafParser
            my_parser = KafNafParser(root + "/" + inputfile)    
        except:
            continue

        # Iterate over the predicates and check for ESO predicates in the external references
        for predicate in my_parser.get_predicates():
            shit = False
            for ext_ref in predicate.get_external_references():
                if ext_ref.get_resource() in ['FrameNet', 'FrameNet+', 'FrameNet-', 'ESO']:
                    if ext_ref.get_resource()=='ESO':
                        try:
                            which_eso[ext_ref.get_reference()]+=1
                        except KeyError:
                            which_eso[ext_ref.get_reference()]=1
                    elif ext_ref.get_resource()=='FrameNet':
                        try:
                            which_fn_uncov[ext_ref.get_reference()]+=1
                        except KeyError:
                            which_fn_uncov[ext_ref.get_reference()]=1                        
                    else:
                        try:
                            which_fn_cov[ext_ref.get_reference()]+=1
                        except KeyError:
                            which_fn_cov[ext_ref.get_reference()]=1                        
                    shit=True
            if shit==False:
                no_fe += 1
                
                pred_mention=""
                target_ids = predicate.get_span().get_span_ids()
                for tid in target_ids:
                    pred_mention += my_parser.get_term(tid).get_lemma() + " "
                pred_mention=pred_mention.strip()
                try:
                    which_no_fe[pred_mention]+=1
                except KeyError:
                    which_no_fe[pred_mention]=1
                    
print "ESO classes: "
print which_eso

print "FN frames covered: "
print which_fn_cov

print "FN frames not covered: "
print which_fn_uncov

print "Mentions with no FN and no ESO: "
print which_no_fe

print "No FN & No ESO: " + str(no_fe)