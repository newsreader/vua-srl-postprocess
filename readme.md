
Semantic Role Labeling Postprocessing script which uses the ESO ontology to decide which of the FrameNet predicates and roles are correct. 

Requirements
------------

* Python (this module has been tested with version 2.7.5) and the following module:

	
* [KafNafParser](https://github.com/opener-project/KafNafParserPy)

* OWL format of the ESO ontology (version 0.6)


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
This software is distributed under the Apache v2.0 license. See LICENSE for more info. 


	
**To do**	
* Improve the module in the future