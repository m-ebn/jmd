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


def headerOffset(element):
    element[1] = re.sub(JmdPatterns.pattern_titles,
                        JmdPatterns.sub_titles, element[1])
    element[2] = re.sub(JmdPatterns.pattern_titles,
                        JmdPatterns.sub_titles, element[2])


def addHeader(element):
    # To be implemented in the future
    pass


def addFooter(element):
    # To be implemented in the future
    pass


def updateImageLinks(element, base_dir, outputPath, jmdFile):
    # Get variable without filename for further filepath processing
    outputPathHead = os.path.split(os.path.join(jmdFile, outputPath))[0]
    # Find all image references in a file
    imageUrlList = re.findall(
        JmdPatterns.pattern_image_path, element[1])
    # Get new file reference and update the old one
    for image in imageUrlList:
        # Create a normalized, relative path between the image and path of the output file
        normalizedImagePath = os.path.normpath(
            os.path.join(jmdFile, base_dir, image[1]))
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

# https://stackoverflow.com/questions/8170982/strip-string-after-third-occurrence-of-character-python
# def truncStringAt(s, d, n=1):
#     "Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d."
#     return d.join(s.split(d, n)[:n])


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

    pattern_titles = '(#{1,6}) '
    sub_titles = '#\g<1> '

    # Detect Markdown style image
    pattern_image_path = '\!\[(.*)\]\((.*)\)'

    pattern_begin_image_path = '\!\['
    pattern_center_image_path = '\]\('
    pattern_end_image_path = '\)'

    sub_begin_image_path = '!['
    sub_center_image_path = ']('
    sub_end_image_path = ')'

    # Detect file references
    pattern_file_ref = '(\n| )\[(.*)\]\((?!https://)(.*)\)'

    pattern_file_ref_begin = '\['
    pattern_file_ref_center = '\]\((?!https://)'
    pattern_file_ref_end = '\)'

    sub_file_ref_begin = '['
    sub_file_ref_center = ']('
    sub_file_ref_end = ')'

    # cmd path pattern
    pattern_path = '\.\.\/'
    sub_path = '../'


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
        # 4: list of all references in file pointing to another local file
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
                        title = file_content['title']

                        try:
                            ids = file_content['parsed_document_id'].split(
                                ", ")
                        except:
                            ids = file_content['parsed_document_id']

                        try:
                            positions = file_content['parsed_document_position'].split(
                                ", ")
                        except:
                            positions = file_content['parsed_document_position']

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
        self.fileContentList = sorted(
            self.fileContentList, key=lambda x:  x[0])

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

    def get_cmd_args(self):
        parser = argparse.ArgumentParser(description='Process some integers.')

        parser.add_argument('-d', '--document_id', default='docs',
                            help='Specyfies the ID of to be included files.')

        parser.add_argument('-o', '--output', default='document.md',
                            help='Output directory/filename. This shall also include the extension `.md`. Example: `doc/documentation.md`.')

        parser.add_argument('-b', '--base_dir', default='.',
                            help='Base directory, the tool shall look for Markdown files.')

        # To be implemented later!
        # parser.add_argument('-m', '--meta_data_path', default='',
        #                    help='Reference a file, where metadata in yml format shall be included from.')

        parser.add_argument('-i', '--include_title', type=bool, default=False,
                            help='Include meta data title as first level title (#).')

        parser.add_argument('-h', '--header_offset', type=bool, default=False,
                            help='Add an additional `#` to titles in order to manipulate final file structure.')

        # parser.add_argument('-r', '--reduce_infile_references', type=bool, default=False,
        #                    help='Reduce file references that are now merged.')

        # parser.add_argument('-p', '--pandoc_references', type=bool, default=False,
        #                    help='Output Markdown file with Pandoc ready in file references')

        # parser.add_argument('-s', '--set_default_true', type=bool, default=False,
        #                    help='Set all default false to default true to have a cleaner cmd command.')

        # parser.add_argument('-t', '--detect_html_tex_tags', type=bool, default=False,
        #                    help='Detect LaTeX commands nested in html tags')

        args_list = parser.parse_args()

        self.document_id = args_list.document_id
        self.outputPath = args_list.output
        self.base_dir = args_list.base_dir
        # To be implemented later!
        # self.meta_data_path = args_list.meta_data_path
        # self.include_title = args_list.include_title
        # self.header_offset = args_list.header_offset
        # self.reduce_infile_references = args_list.reduce_infile_references
        # self.pandoc_references = args_list.pandoc_references
        # self.detect_html_tex_tags = args_list.detect_html_tex_tags

        # if args_list.set_default_true == True:
        #     self.include_title = True
        #     self.header_offset = True
        #     self.reduce_infile_references = True
        #     self.pandoc_references = True
        #     self.detect_html_tex_tags = True


if __name__ == '__main__':

    # document = jmd()

    # document.getCmdArgs()

    # document.gatherDocuments()

    # document.applyOptions()

    # text = document.getText()

    # document.writeText(text)
    document2 = jmd()
    document2.document_id = "images"
    document2.base_dir = "test/testfiles"
    document2.outputPath = "hui/testi/output.md"
    document2.gatherDocuments()
    document2.applyOptions()
    text = document2.getText()
    document2.writeText(text)


# elementDepth = element[3].count('/') - element[3].count('./')
    # depthDifference = elementDepth - outputFileDepth
    # elementPathList = splitPath(element[3])
    # print(outputPathList)
    # print(elementPathList)
    # dirtest = dircmp(self.outputPath, element[3])
    # left = dirtest.subdirs
    # print(depthDifference)
    # if depthDifference < 0:
    #     print("Difference smaller")
    #     string = self.patterns.sub_begin_image_path
    #     levels = depthDifference + 1
    #     print(depthDifference)
    #     if depthDifference < 2:
    #         levels = levels + 1
    #     for i in range(levels):
    #         string = string + self.patterns.sub_path
    #     element[2] = re.sub(
    #         self.patterns.pattern_begin_image_path, string, element[2])
    # elif depthDifference > 0:
    #     print("Difference greater")
    #     string = self.patterns.pattern_begin_image_path
    #     print(depthDifference)
    #     levels = depthDifference - 1
    #     if depthDifference > 2:
    #         print("Level Offset")
    #         levels = levels + 1
    #     for i in range(levels):
    #         string = string + self.patterns.pattern_path
    #     element[1] = re.sub(
    #         string, self.patterns.sub_begin_image_path, element[1])

    #     print(element[2])
