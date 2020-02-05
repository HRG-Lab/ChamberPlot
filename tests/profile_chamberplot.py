import os
import re

import chamberplot

dat_file = os.path.abspath("tests/test_data/Donovan/Initial Data Sets/0el_Channel1.dat")

chamberplot.dat_to_dataframes(dat_file)
        
        