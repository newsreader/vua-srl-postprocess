
vua-srl-postprocess
=======

Semantic Role Labeling Postprocessing script which uses the ESO ontology to decide which of the FrameNet predicates and roles are correct. 

Requirements
------------

* Python (this module has been tested with version 2.7.5) and the following module:

* [KafNafParser](https://github.com/cltl/KafNafParserPy)

* OWL format of the ESO ontology (version 0.6)


This module can be used for two purposes: analysis of SRL data and for postprocessing.

1. Analysis
----------- 

In order to run the module:

1. clone the repository from guthub: https://github.com/newsreader/vua-srl-postprocess. 
2. In states.py, modify the path variable to point to the root location of the files.
3. Execute:

python states.py

Usage
------

The postprocessing module should be executed with passing the input and the output file in NAF format, as follows:

        main.py -i <inputfile> -o <outputfile>
        
The module expects the ESO ontology (named "ESO.owl") and the KafNafParser to exist in the same directory.

2. Postprocessing
-----------------

Usage
------

The postprocessing module should be executed with passing the input and the output file in NAF format, as follows:

        main.py -i <inputfile> -o <outputfile>
        
The module expects the ESO ontology (named "ESO.owl") and the KafNafParser to exist in the same directory.

	
Contact
-------
* Filip Ilievski
* VU University Amsterdam
* [f.ilievski@student.vu.nl](f.ilievski@student.vu.nl)


License
-------
Software distributed under Apache License Version 2.0, January 2004.
See LICENSE file for more details.
