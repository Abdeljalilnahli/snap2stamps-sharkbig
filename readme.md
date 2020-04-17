
# snap2stamps/automatical-splitting

*this is the **test** version modified from snap2stamps code to auto-choose burst and swath durring splitting.*

folk from https://github.com/mdelgadoblasco/snap2stamps

### Addings:

1. bin/splitting_slave_readIWs.py
2. bin/inSide.py
3. bin/IWs.py
4. graphs/slave_split_applyorbit_readIWs.xml

### Usage

1. Running snap2stamps procedure please refers to Manual 4.1 - 4.5.
2. Replace command at section 4.2 with the following command:
```
$ python splitting_slaves_readIWs.py project.conf
```

2. Run command below to see which swath and burst is used in automatically splitting.
```
$ python IWs.py project.conf
```

### Reference
1. https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
2. Jose Manuel Delgado Blasco. Sentinel Application Platform asc InSAR processor fro PSI processing with StaMPS, 2018.
3. Dipankar Mandal, Divya Sekhar Vaka, Narayana Rao Bhogapurapu, V. S. K. Vanama, Vineet Kuma, Y. S. Rao, Avik Bhattacharya. Semtinel-1 SLC preprocessing workflow from polarimetric application: A generic practice for generating dual-pool covariance elements in SNAP S-1 toolbox, 2019.

### Future Work
1. Automatically merge difference swath.


======================================================================
# snap2stamps <a href="https://doi.org/10.5281/zenodo.1308687"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1308687.svg" alt="DOI"></a> 

Using SNAP as InSAR processor for StaMPS

This manual and the included scripts call routines of the ESA SentiNel Application Platform (SNAP) to perform TOPSAR interferometric processing with ingestion in the open source StaMPS package.

The provided scripts with this SNAP to StaMPS manual are not part of the SNAP software. SNAP therefore needs to be installed independently (version 6.0 or higher). The provided scripts are open-source contributions and should not be mistaken for official Applications within SNAP. The scripts are provided to you "as is" with no warranties of corrections. Use at your own risk.

This provided package evolved from inital bash script routines used for the publication "ESA SNAP – StaMPS integrated processing for Sentinel-1 Persistent Scatterer Interferometry" presented at IGARSS 2018 in Valencia in collaboration with UJA, BRGM, ESA, Progressive Systems and ARRAY

This work was done with the collaboration of Prof Andrew Hooper for ensuring the SNAP StaMPS compatibility.

Author: Jose Manuel Delgado Blasco(1), Michael Foumelis(2) Organizations: 1. Microgeodesia Jaen Research Group, University of Jaen (Spain) / Grupo de Investigación Microgeodesia Jaen, Universidad de Jaen 2. BRGM - French Geological Survey
