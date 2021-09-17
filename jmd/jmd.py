#!/usr/bin/env python3

import frontmatter
import os
import re
import argparse
import numpy as np


def splitPath(path):
    return path.split("/")


def includeTitle(element):
    element[1] = '\n\n' + element[1]
    element[2] = '# ' + element[2]

    return element


def headerOffset(element):
    element[1] = re.sub(JmdPatterns.pattern_titles,
                        JmdPatterns.sub_titles, element[1])
    element[2] = re.sub(JmdPatterns.pattern_titles,
                        JmdPatterns.sub_titles, element[2])

    return element


def addHeader(element):
    # To be implemented in the future
    pass


def addFooter(element):
    # To be implemented in the future
    pass


def updateImageLinks(element, base_dir, outputPath, jmdFile):
    print(element)
    print(base_dir)
    print(outputPath)
    print(jmdFile)
    # Get variable without filename for further filepath processing
    outputPathHead = os.path.split(os.path.join(jmdFile, outputPath))[0]
    # Find all image references in a file
    imageUrlList = re.findall(
        JmdPatterns.pattern_image_path, element[1])
    # Get new file reference and update the old one
    for image in imageUrlList:
        """ Create a normalized, relative path between the image and path of the output file
            1. get path to file withour filename
            2. joing the absolute path to the jmd.py file with the base_Dir with 1. and the image path
            3. normalize the filepath with os.path.normpath
        """
        normalizedImagePath = os.path.normpath(
            os.path.join(jmdFile, base_dir, os.path.split(element[3])[0], image[1]))
        # Generate a relative path from the image path to the path of the output file
        fixedOutputPath = os.path.relpath(
            normalizedImagePath, outputPathHead)
        # Replace the original url with the newly generated url
        element[1] = re.sub(JmdPatterns.pattern_begin_image_path
                            + image[0]
                            + JmdPatterns.pattern_center_image_path
                            + image[1]
                            + JmdPatterns.pattern_end_image_path,
                            JmdPatterns.sub_begin_image_path
                            + image[0]
                            + JmdPatterns.sub_center_image_path
                            + fixedOutputPath
                            + JmdPatterns.sub_end_image_path,
                            element[1])
    return element


def updateFileReferences(element, base_dir, outputPath, jmdFile, includedFiles):
    # Get variable without filename for further filepath processing
    outputPathHead = os.path.split(os.path.join(jmdFile, outputPath))[0]
    # Find all files references in a file
    fileUrlList = re.findall(JmdPatterns.pattern_file_ref, element[1])
    # Get new file reference and update the old one
    for file in fileUrlList:
        includeFilesNames = []
        for includeFile in includedFiles:
            includeFilesNames.append(os.path.split(includeFile)[1])
        if file[2].split("#")[0] in includeFilesNames:
            fixedOutputPath = '#' + file[2].split("#")[1]
        else:
            # Create a normalized, relative path between the image and path of the output file
            normalizedImagePath = os.path.normpath(
                os.path.join(jmdFile, base_dir, file[2]))
            fixedOutputPath = os.path.relpath(
                normalizedImagePath, outputPathHead)
        # Replace the original url with the newly generated url
        element[1] = re.sub(file[0]
                            + JmdPatterns.pattern_file_ref_begin
                            + file[1]
                            + JmdPatterns.pattern_file_ref_center
                            + file[2]
                            + JmdPatterns.pattern_file_ref_end,
                            file[0]
                            + JmdPatterns.sub_file_ref_begin
                            + file[1]
                            + JmdPatterns.sub_file_ref_center
                            + fixedOutputPath
                            + JmdPatterns.sub_file_ref_end,
                            element[1])
    return element


class JmdPatterns():
    # Collection of Python3 regex commands for text manipulation

    pattern_titles = r'(#{1,6}) '
    sub_titles = r'#\g<1> '

    # Detect Markdown style image
    pattern_image_path = r'\!\[(.*)\]\((.*)\)'

    pattern_begin_image_path = r'\!\['
    pattern_center_image_path = r'\]\('
    pattern_end_image_path = r'\)'

    sub_begin_image_path = r'!['
    sub_center_image_path = r']('
    sub_end_image_path = r')'

    # Detect file references
    pattern_file_ref = r'(^|\n| )\[(.*)\]\((?!https://)(.*)\)'

    pattern_file_ref_begin = r'\['
    pattern_file_ref_center = r'\]\((?!https://)'
    pattern_file_ref_end = r'\)'

    sub_file_ref_begin = r'['
    sub_file_ref_center = r']('
    sub_file_ref_end = r')'

    # cmd path pattern
    pattern_path = r'\.\.\/'
    sub_path = r'../'


class jmd():

    def __init__(self):
        # default values
        self.document_id = "doc"
        self.base_dir = "."
        self.outputPath = "document.md"
        self.meta_data_path = ""
        self.include_title = False
        self.header_offset = False
        self.reduce_infile_references = False
        self.pandoc_references = False
        self.detect_html_tex_tags = False

        # Patterns
        self.patterns = JmdPatterns

        # Fil contents
        # 0: index
        # 1: content
        # 2: title
        # 3: original file path
        self.fileContentList = []

    def gatherDocuments(self):
        for root, dirs, files in os.walk(self.base_dir, topdown=False):
            for file in files:

                if file.endswith(".md") and file != os.path.basename(self.meta_data_path):
                    filePath = self.base_dir + '/' + file
                    try:
                        file_content = frontmatter.load(
                            os.path.join(root, file))

                        content = file_content.content
                        try:
                            title = file_content['title']
                        except:
                            title = ""

                        ids = ""
                        try:
                            if type(file_content['parsed_document_id']) != str:
                                ids = file_content['parsed_document_id']
                            else:
                                ids = file_content['parsed_document_id'].split(
                                    ", ")
                        except:
                            pass

                        try:
                            if type(file_content['parsed_document_position']) != str:
                                positions = file_content['parsed_document_position']
                            else:
                                positions = file_content['parsed_document_position'].split(
                                    ", ")
                        except:
                            pass

                        if self.document_id in ids:

                            # Get the position, at which the index is located in the list of document id's
                            index = ids.index(self.document_id)

                            # Append content to fileContentList
                            try:
                                self.fileContentList.append(
                                    [int(positions[index]), content, title, filePath])
                            except:
                                self.fileContentList.append(
                                    [int(positions), content, title, filePath])

                    except:
                        print('ERROR')
        # Sort all entries based on the `parsed_documen_position`
        self.fileContentList = sorted(
            self.fileContentList, key=lambda x:  x[0])

    def applyOptions(self):
        # Go over all detected files
        for element in self.fileContentList:
            element = updateImageLinks(
                element, self.base_dir, self.outputPath, __file__)
            includedFilesList = np.array(self.fileContentList)[:, 3]
            element = updateFileReferences(element, self.base_dir,
                                           self.outputPath, __file__, includedFilesList)
            if self.include_title == True:
                element = includeTitle(element)
            if self.header_offset == True:
                element = headerOffset(element)

    def getText(self):
        textList = ''

        for element in self.fileContentList:

            textElement = ''

            if self.include_title == True:
                textElement = element[2] + element[1]
            else:
                textElement = element[1]

            textList = textList + textElement + '\n\n'

        return textList

    def writeText(self, output):

        path, file = os.path.split(self.outputPath)

        try:
            os.makedirs(path)
        except:
            print("existing directory.")

        try:
            f = open(self.outputPath, "x")

            f.write(output)

            f.close()

            print("Output file " + str(file) +
                  " was successfully created at " + path + ".")
        except:
            print("Filename already taken.")

        print("File goin to: ")
        print(str(file))

    def getCmdArgs(self):
        parser = argparse.ArgumentParser(description='Process some integers.')

        parser.add_argument('-d', '--document_id', default='docs',
                            help='Specyfies the ID of to be included files.')

        parser.add_argument('-o', '--output', default='document.md',
                            help='Output directory/filename. This shall also include the extension `.md`. Example: `doc/documentation.md`.')

        parser.add_argument('-b', '--base_dir', default='.',
                            help='Base directory, the tool shall look for Markdown files.')

        parser.add_argument('-i', '--include_title', type=bool, default=False,
                            help='Include meta data title as first level title (#).')

        parser.add_argument('-h', '--header_offset', type=bool, default=False,
                            help='Add an additional `#` to titles in order to manipulate final file structure.')

        args_list = parser.parse_args()

        self.document_id = args_list.document_id
        self.outputPath = args_list.output
        self.base_dir = args_list.base_dir


if __name__ == '__main__':

    document = jmd()

    document.getCmdArgs()

    document.gatherDocuments()

    document.applyOptions()

    text = document.getText()

    document.writeText(text)
