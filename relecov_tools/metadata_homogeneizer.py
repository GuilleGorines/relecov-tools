#!/usr/bin/env python

# Imports
# import os
import sys
import json
import pandas as pd


def check_extension(instring, extensions):
    """Given a file as a string and a list of possible extensions,
    returns true if the extension can be found in the file"""
    for extension in extensions:
        if instring.endswith(extension):
            return True


def open_json(json_path):
    """Load the json file"""
    with open(json_path) as file:
        json_dict = json.load(file)
    return json_dict


class Homogeneizer:
    """Homogeneizer object"""

    def __init__(filename, self):
        self.filename = filename
        self.dictionary = None
        self.centre = None
        self.dataframe = None

        # To Do: replace string with local file system for testing
        # Header path can be found in conf/configuration.json

        header_path = ""
        self.translated_dataframe = pd.DataFrame(
            columns=open_json(header_path)["new_table_headers"]
        )
        return

    def associate_dict(self):
        """Detect the origin centre of the metadata, and finds the corresponding json file to use"""

        # Check name of the file attribute of the object
        # Check schema with all centres and find their json
        # associate centre and json with object
        # raise error when in doubt
        # must check on schema/institution_schemas

        path_to_institution_json = ""

        detected = []
        institution_dict = open_json(path_to_institution_json)

        for key in institution_dict.keys():
            # cap insensitive
            if key.lower() in self.filename.lower():
                detected.append(institution_dict[key])

        if len(set(detected)) != 1:
            print("some problems arised!!!")  # change this to an elegant form
            sys.exit()  # maybe check which ones are being mixed or when none is being found
        else:
            print("works fine")  # delete this after testing
            self.dictionary = detected[0]  # first item, they are all equal

        return

    def load_dataframe(self):
        """Detect possible extensions for the metadata file
        Open it into a dataframe"""

        excel_extensions = [".xlsx", ".xls", ".xlsm", ".xlsb"]
        odf_extension = [".odf"]
        csv_extensions = [".csv"]
        tsv_extensions = [".tsv"]

        if check_extension(self.filename, excel_extensions):
            self.dataframe = pd.read_excel(self.filename, header=0)
        elif check_extension(self.filename, odf_extension):
            # Needs a special package
            self.dataframe = pd.read_excel(self.filename, engine="odf", header=0)
        elif check_extension(self.filename, csv_extensions):
            self.dataframe = pd.read_csv(self.filename, sep=",", header=0)
        elif check_extension(self.filename, tsv_extensions):
            self.dataframe = pd.read_csv(self.filename, sep="\t", header=0)

        return

    def load_dictionary(self):
        """Load the corresponding dictionary"""

        # To Do: replace string with local file system for testing
        path_to_tools = ""
        dict_path = path_to_tools + "/schema/institution_schemas" + self.filename
        self.dictionary = open_json(dict_path)
        return

    def translate_dataframe(self):
        """Use the corresponding dictionary to translate the df"""
        # if dictionary is "none" or similar, do nothing

        for key, value in self.dictionary["equivalence"].items():
            self.translate_dataframe[key] = self.dataframe[value]

        for key, value in self.dictionary["constants"].items():
            self.translate_dataframe[key] = value

        return

    def verify_translated_dataframe(self):
        """Checks if the dataframe holds all the needed values for the relecov tools suite"""

        pass
        return
