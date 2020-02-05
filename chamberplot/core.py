# -*- coding: utf-8 -*-
import re

from .structures import Record
from . import helpers

# FIXME: Right now, this only grabs one record
def dat_to_dataframes(dat_file):
    with open(dat_file, 'r') as dat:
        lines = dat.read().splitlines()

        # Deletes comment lines at the beginning of the file
        while lines[0][0].lstrip() != '(':
            del lines[0]

        dat_string = " ".join(lines)
        helpers.find_parens(dat_string)

        records = []
        locs = [m.start() for m in re.finditer('Record', dat_string)]
        print('locs: {}'.format(locs))
        for i, loc in enumerate(locs):
            if i == len(locs) - 1:
                print(dat_string[loc:][0:600])
                records.append(Record(dat_string[i:]))
            else:
                records.append(Record(dat_string[loc-1:locs[i+1]-1]))

        [r.clean_freq_data() for r in records]
        dataframes = [r.to_dataframes() for r in records]
        print(len(dataframes))
