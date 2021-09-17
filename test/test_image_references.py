import jmd.jmd as jmd


def test_imageLinkOutputInSubfolder():
    string = "![Image](image.png)"
    string1Result = jmd.updateImageLinks([1, string, "", "file.md"],
                                         "",
                                         "output/output.md",
                                         ".")[1]
    assert string1Result == "![Image](../image.png)", "Function retunred wrong link"


def test_imageLinkOriginalInSubfolder():
    string = "![Image](image.png)"
    string1Result = jmd.updateImageLinks([1, string, "", "test/file.md"],
                                         ".",
                                         "output.md",
                                         ".")[1]
    assert string1Result == "![Image](test/image.png)", "Function retunred wrong link"


def test_imageLinkSameFolder():
    string = "![Image](image.png)"
    string1Result = jmd.updateImageLinks([1, string, "", "file.md"],
                                         "",
                                         "output/output.md",
                                         ".")[1]
    assert string1Result == "![Image](../image.png)", "Function retunred wrong link"
