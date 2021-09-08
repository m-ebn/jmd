#!/usr/bin/env python3

import frontmatter
import os
import sys
import getopt
import re
import argparse


class jmd_patterns():

    pattern_titles = '(#{1,6}) '
    sub_titles = '#\g<1> '

    pattern_refs = '\[(.*)\]\((?!https)(.*).md#(.*)\)'
    sub_refs = '[\g<1>](#\g<3>)'
    sub_refs_pandoc = '\g<1> \\ref{\g<3>}'

    pattern_tex_begin = '\<p tex\-begin=\"(.*)\"/\>'
    sub_tex_begin = '\\\\Begin{\g<1>}'

    pattern_tex_command = '\<p tex\-command=\"(.*)\"\/\>'
    sub_tex_command = '\g<1>'

    pattern_tex_end = '\<p tex\-end=\"(.*)\"/\>'
    sub_tex_end = '\\\\End{\g<1>}'

    pattern_path = '\.\.\/'
    pattern_begin_image_path = '\!\[(.*)\]\('
    sub_path = '../'
    sub_begin_image_path = '![\g<1>]('


class jmd():

    def __init__(self):
        # default values
        self.document_id = "doc"
        self.base_dir = "."
        self.output_path = "document.md"
        self.meta_data_path = ""
        self.include_title = False
        self.header_offset = False
        self.reduce_infile_references = False
        self.pandoc_references = False
        self.detect_html_tex_tags = False

        # Fil contents
        # 1: index
        # 2: content
        # 3: title
        self.fileContentList = []

    def gather_documents(self):
        for root, dirs, files in os.walk(self.base_dir, topdown=False):
            for file in files:

                if file.endswith(".md") and file != os.path.basename(self.meta_data_path):
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
                                    [int(positions[index]), content, title])
                            except:
                                self.fileContentList.append(
                                    [int(positions), content, title])

                    except:
                        print('ERROR')

    def applyOptions(self):
        if self.include_title == True:
            self.includeTitle()

    def includeTitle(self):
        for element in self.fileContentList:
            element[1] = '\n\n' + element[1]
            element[2] = '# ' + element[2]

    def headerOfset(self):
        # To be implemented in the future
        pass

    def addHeader(self):
        # To be implemented in the future
        pass

    def addFooter(self):
        # To be implemented in the future
        pass

    def get_text(self):
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

    def write_text(self, output):

        path, file = os.path.split(self.output_path)

        try:
            os.makedirs(path)
        except:
            print("existing directory.")

        try:
            f = open(self.output_path, "x")

            f.write(output)

            f.close()

            print("Output file " + str(file) +
                  " was successfully created at " + path + ".")
        except:
            print("Filename already taken.")

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

        # parser.add_argument('-i', '--include_title', type=bool, default=False,
        #                    help='Include meta data title as first level title (#).')

        # parser.add_argument('-j', '--header_offset', type=bool, default=False,
        #                    help='Add an additional `#` to titles in order to manipulate final file structure.')

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
        self.output_path = args_list.output
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

    document = jmd()

    document.get_cmd_args()

    document.get_text()

    text = document.get_text()

    document.write_write(text)
