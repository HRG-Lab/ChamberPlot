import re
from itertools import islice

import pandas as pd

from . import helpers

class Record():
    def __init__(self, string):
        self.__dim= 0
        self.__size = 0
        self.__schema = None
        self.__data = {}

        string = string[9:-1] # Trim '(Record ...)'
        self.parse_input_string(string)

    def __str__(self):
        return """Record:
    dim: {}
    size: {}
    schema: {}
    data: {}
        """.format(self.dim, self.size, self.schema, self.data)

    @property
    def dim(self):
        return self.__dim

    @property
    def size(self):
        return self.__dim

    @property
    def schema(self):
        return self.__schema

    @property
    def data(self):
        return self.__data

    def clean_freq_data(self):
        # In the files used as reference when creating this every record
        # contained a list of all the frequency points. This is nonsense
        if "Freq" not in self.__data:
            raise KeyError("Data does not contain frequency field")

        self.data["Freq"] = self.data["Freq"][0]

    def parse_input_string(self, string):
        data_re = re.compile(r'\(data[\s\S]+\)')
        matches = re.search(data_re, string)
        if data_re:
            data = matches.group(0)
            data = data[4:-1] # strip "(data ...)"
            string = re.sub(data_re, '', string)

        it = iter(enumerate(string))
        for i, c in it:
            if c == '(':
                end = helpers.find_close_paren(string, start=i)
                statement = re.sub('[\(\)]', '', string[i:end]).split()
                keyword = statement[0]
                
                if keyword == 'schema':
                    self.__schema = Schema(string[i:end+1])
                    for key in self.schema.fields.keys():
                        self.__data[key] = []
                    skip = end-i
                    next(islice(it, skip, skip), None)

                elif keyword == 'numDims':
                    self.__dim = statement[1]
                
                elif keyword == 'size':
                    self.__size = statement[1]

                else:
                    raise KeyError('Unexpected keyword: {}'.format(statement[0]))

        record_locs = [x.start() for x in re.finditer('\((record)', data)]
        records = []
        for i, _ in enumerate(record_locs):
            if i == len(record_locs)-1:
                records.append(data[record_locs[-1]:-2])
            else:
                records.append(data[record_locs[i]:record_locs[i+1]-2])

        for record in records:
            record_dict = self.parse_record(record)

    def parse_record(self, record):
        record = record[7:-1] # strip "(record ...)"
        fields = re.findall('\(([^)]+)', record)
        for field in fields:
            field_name = re.search('\"\w+\"', field).group(0).strip('"')
            list_search = re.search('\[.*\]', field) 
            number_search = re.search('-?\d+\.?\d*', field)

            # This converts the freqs to floats which is okay but maybe not ideal
            if list_search:
                field_val = list_search.group(0)
                field_val = re.sub('[\[\]]', '', field_val).strip()
                field_val = [float(x) for x in field_val.split()]
            elif number_search:
                field_val = number_search.group(0)
                field_val = float(field_val)

            self.__data[field_name].append(field_val)
        
    def to_dataframes(self):
        proper_keys = ("Mag", "Phase", "Vpos", "Hpos", "HV", "Freq")
        if not all(k in self.data.keys() for k in proper_keys):
            raise KeyError("Record does not contain the correct keys: {}".format(self.data.keys()))
        
        pos = list(zip(self.data["Vpos"], self.data["Hpos"]))
        dataframes = {}
        for i, freq in enumerate(self.data["Freq"]):
            mags = [mag[i] for mag in self.data["Mag"]]
            phases = [phase[i] for phase in self.data["Phase"]]
            df = pd.DataFrame({'Position': pos, 'Mag': mags, 'Phase': phases})
            dataframes['{}'.format(freq)] = df

        return dataframes



class Schema():
    def __init__(self, string):
        self.__numFields = 0
        self.__fields = {}

        string = string[7:-1] # strip "(schema ...)"

        it = iter(enumerate(string))
        for i, c in it:
            if c == '(':
                end = helpers.find_close_paren(string, start=i)
                statement = re.sub('[\(\)]', '', string[i:end]).split()
                keyword = statement[0]

                if keyword == 'numFields':
                    self.__numFields = statement[1]

                elif keyword == 'fieldName':
                    self.new_field(string[i:end+1])
                    skip = end-i
                    next(islice(it, skip, skip), None)

                else:
                    raise NotImplementedError('{} is not yet implemented\n\tFull statement: {}'.format(keyword, statement))

    def __str__(self):
        return """
    numFields: {}
    fields: {}
        """.format(self.__numFields, self.__fields)

    @property
    def fields(self):
        return self.__fields

    @property
    def numFields(self):
        return self.__numFields

    def new_field(self, string):
        string = string[10:-1]
        fields = [s.strip().split() for s in re.split(r'[()]', string) if not s.isspace()]
        fieldname = fields[0][0].strip('"')
        fields = fields[1:]
        temp = {}
        for field in fields:
            temp[field[0]] = field[1]

        self.__fields[fieldname] = temp



    
