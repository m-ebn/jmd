import unittest
import pytest

import jmd.jmd


def test_inDocumentReference():
    string1 = "[File1](testfile1.md#And-a-subtitle)"
    string1Result = jmd.jmd.updateFileReferences([1, string1, "", "file.md"],
                                                 ".",
                                                 "/output.md",
                                                 ".",
                                                 ["testfile1.md"])[1]
    assert string1Result == "[File1](#And-a-subtitle)", "Reference linking to another file could not be converted into a inline reference."


def test_stringStartReference():
    string1 = "[File1](testfile1.md#And-a-subtitle)"
    string1Result = jmd.jmd.updateFileReferences([1, string1, "", "file.md"],
                                                 ".",
                                                 "/output.md",
                                                 ".",
                                                 ["testfile1.md"])[1]
    assert string1Result == "[File1](#And-a-subtitle)", "Reference at start of string not detected"


def test_leadingSpaceReference():
    string1 = " [File1](testfile1.md#And-a-subtitle)"
    string1Result = jmd.jmd.updateFileReferences([1, string1, "", "file.md"],
                                                 ".",
                                                 "/output.md",
                                                 ".",
                                                 ["testfile1.md"])[1]
    assert string1Result == " [File1](#And-a-subtitle)", "Reference with leading space not detected"


def test_leadingNewlineReference():
    string = "\n[File1](testfile1.md#And-a-subtitle)"
    stringResult = jmd.jmd.updateFileReferences([1, string, "", "file.md"],
                                                ".",
                                                "/output.md",
                                                ".",
                                                ["testfile1.md"])[1]
    assert stringResult == "\n[File1](#And-a-subtitle)", "Reference with leading new line not detected"


def test_referenceOutsideFile():
    string = "[File2](testfile.md)"
    stringResult = jmd.jmd.updateFileReferences([1, string, "", "images.md"],
                                                "",
                                                "output.md",
                                                ".",
                                                [""])[1]
    assert stringResult == "[File2](testfile.md)", "Reference to on device file wrong."


def test_referenceOutsideFileInOldFolder():
    string = "[File2](testfile.md)"
    stringResult = jmd.jmd.updateFileReferences([1, string, "", "test/images.md"],
                                                "test",
                                                "output.md",
                                                ".",
                                                [""])[1]
    assert stringResult == "[File2](test/testfile.md)", "Reference to on device file wrong."


def test_outputInSubfolder():
    string = "[File2](testfile.md)"
    stringResult = jmd.jmd.updateFileReferences([1, string, "", "images.md"],
                                                "",
                                                "test/output.md",
                                                ".",
                                                [""])[1]
    assert stringResult == "[File2](../testfile.md)", "Reference to on device file wrong."


def test_bothInSubfolder():
    string = "[File2](testfile.md)"
    stringResult = jmd.jmd.updateFileReferences([1, string, "", "test/images.md"],
                                                "test",
                                                "old/output.md",
                                                "",
                                                [""])[1]
    assert stringResult == "[File2](../test/testfile.md)", "Reference to on device file wrong."


def test_detectOnlineUrl():
    string = "[File2](https://www.github.com)"
    stringResult = jmd.jmd.updateFileReferences([1, string, "", "images.md"],
                                                "",
                                                "output.md",
                                                "",
                                                [""])[1]
    assert stringResult == "[File2](https://www.github.com)", "Online reference wrong."
