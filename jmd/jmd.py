#!/usr/bin/env python3

import frontmatter
import os
import sys
import getopt
import re
import argparse


class join_object():

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
        self.output_list = []

    def gather_data(self):
        number_output_dirs = self.output_path.count('/')

        for root, dirs, files in os.walk(self.base_dir, topdown=False):
            for file in files:

                if file.endswith(".md") and file != os.path.basename(self.meta_data_path):
                    try:
                        file_content = frontmatter.load(
                            os.path.join(root, file))

                        content = ''

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

                        if self.include_title == True:
                            content = "# " + \
                                file_content['title'] + \
                                "\n\n" + file_content.content
                        else:
                            content = file_content.content

                        if self.document_id in ids:
                            index = ids.index(self.document_id)

                            if self.header_offset == True:
                                content = re.sub(
                                    self.pattern_titles, self.sub_titles, content)

                            # Detect HTML tags
                            if self.detect_html_tex_tags == True:
                                content = re.sub(
                                    self.pattern_tex_begin, self.sub_tex_begin, content)
                                content = re.sub(
                                    self.pattern_tex_command, self.sub_tex_command, content)
                                content = re.sub(
                                    self.pattern_tex_end, self.sub_tex_end, content)
                            try:
                                content = str(
                                    file_content['parsed-header']) + '\n\n' + content
                            except:
                                pass

                            try:
                                content = content + '\n\n' + \
                                    str(file_content['parsed-footer'])
                            except:
                                pass

                            # Fix paths for images
                            # content = re.sub(
                            #     self.pattern_path, self.sub_path, content)

                            number_dirs = number_output_dirs - \
                                len(dirs) - len(root)

                            print(str(number_dirs))
                            string = ''

                            if number_dirs == 0:
                                pass
                            elif number_dirs > 0:
                                string = self.sub_begin_image_path
                                for i in range(number_dirs):
                                    string = string + self.sub_path
                                content = re.sub(
                                    self.pattern_begin_image_path, string, content)
                            elif number_dirs < 0:
                                string = self.pattern_begin_image_path
                                number_dirs = -1 * number_dirs
                                for i in range(number_dirs):
                                    string = string + self.pattern_path
                                content = re.sub(
                                    string, self.sub_begin_image_path, content)

                            try:
                                self.output_list.append(
                                    [int(positions[index]), content])
                            except:
                                self.output_list.append(
                                    [int(positions), content])

                    except:
                        print('ERROR')
                        # print("File " + str(file) + " does not contain parsed_document_id and/or parsed_document_position.\nThis can be intentional, the file will therefor be ignored.\n")
                    # Adapt file path

        if self.meta_data_path != "":
            try:
                meta_data = open(self.meta_data_path, "r")
                self.output_list.append([0, meta_data.read()])
                meta_data.close()
            except:
                print("No file found on path to meta data: " +
                      str(self.meta_data_path))
        else:
            self.output_list.append([0, ''])

    def join_data(self):
        self.output_list = sorted(self.output_list, key=lambda x:  x[0])

        output = self.output_list[0][1]
        for element in self.output_list[1:]:
            output = output + '\n\n' + element[1]

        if self.reduce_infile_references == True:
            if self.pandoc_references == True:
                output = re.sub(self.pattern_refs, lambda m: m.expand(
                    self.sub_refs_pandoc).lower(), output)
            else:
                output = re.sub(self.pattern_refs, self.sub_refs, output)

        return output

    def write_data(self, output):

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

        parser.add_argument('-m', '--meta_data_path', default='',
                            help='Reference a file, where metadata in yml format shall be included from.')

        parser.add_argument('-i', '--include_title', type=bool, default=False,
                            help='Include meta data title as first level title (#).')

        parser.add_argument('-j', '--header_offset', type=bool, default=False,
                            help='Add an additional `#` to titles in order to manipulate final file structure.')

        parser.add_argument('-r', '--reduce_infile_references', type=bool, default=False,
                            help='Reduce file references that are now merged.')

        parser.add_argument('-p', '--pandoc_references', type=bool, default=False,
                            help='Output Markdown file with Pandoc ready in file references')

        parser.add_argument('-s', '--set_default_true', type=bool, default=False,
                            help='Set all default false to default true to have a cleaner cmd command.')

        parser.add_argument('-t', '--detect_html_tex_tags', type=bool, default=False,
                            help='Detect LaTeX commands nested in html tags')

        args_list = parser.parse_args()

        self.document_id = args_list.document_id
        self.output_path = args_list.output
        self.base_dir = args_list.base_dir
        self.meta_data_path = args_list.meta_data_path
        self.include_title = args_list.include_title
        self.header_offset = args_list.header_offset
        self.reduce_infile_references = args_list.reduce_infile_references
        self.pandoc_references = args_list.pandoc_references
        self.detect_html_tex_tags = args_list.detect_html_tex_tags

        if args_list.set_default_true == True:
            self.include_title = True
            self.header_offset = True
            self.reduce_infile_references = True
            self.pandoc_references = True
            self.detect_html_tex_tags = True


if __name__ == '__main__':

    document = join_object()

    document.get_cmd_args()

    document.gather_data()

    text = document.join_data()

    document.write_data(text)
