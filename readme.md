
# snap2stamps modified for automatical-splitting

*this is the **test** version to modified snap2stamps code to auto choose burst and swath.*
IWs.py print out for each slave which burst to use.

folk from https://github.com/mdelgadoblasco/snap2stamps

### Addings:

1. bin/splitting_slave_readIWs.py
2. bin/inSide.py
3. bin/IWs.py
4. graphs/slave_split_applyorbit_readIWs.xml

### Usage
1. Automatically choose subswath and IWs with respect to the region designated from the  project.conf.
`$ python splitting_slave_readIWs.py proj.conf`

2. Printing/Logging wihch swath and burst to use, and the result log is preserved in "logs/IW_list"
`$ python IWs.py proj.conf`

### reference
1. https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
2. Jose Manuel Delgado Blasco. Sentinel Application Platform asc InSAR processor fro PSI processing with StaMPS, 2018.
3. Dipankar Mandal, Divya Sekhar Vaka, Narayana Rao Bhogapurapu, V. S. K. Vanama, Vineet Kuma, Y. S. Rao, Avik Bhattacharya. Semtinel-1 SLC preprocessing workflow from polarimetric application: A generic practice for generating dual-pool covariance elements in SNAP S-1 toolbox, 2019.
