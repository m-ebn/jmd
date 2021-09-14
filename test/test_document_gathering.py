from jmd.jmd import jmd


def test_documentGathering1():
    document = jmd()
    document.document_id = "doc0"
    document.gatherDocuments()
    result = [[1, "Testfile 1.", "", "./testfile1.md"],
              [2, "Testfile 2 Content.", "Testfile 2 Title", "./testfile2.md"]]
    assert document.fileContentList == result, ""


def test_documentGathering2():
    document = jmd()
    document.document_id = "doc1"
    document.gatherDocuments()
    result = [[1, "Testfile 1.", "", "./testfile1.md"]]
    assert document.fileContentList == result, ""


def test_documentGathering3():
    document = jmd()
    document.document_id = "doc2"
    document.gatherDocuments()
    result = [[1, "Testfile 3.", "", "./testfile3.md"],
              [2, "Testfile 1.", "", "./testfile1.md"]]
    assert document.fileContentList == result, ""


def test_documentGathering4():
    document = jmd()
    document.document_id = "doc3"
    document.gatherDocuments()
    result = [[1, "Testfile 3.", "", "./testfile3.md"],
              [2, "Testfile 2 Content.", "Testfile 2 Title", "./testfile2.md"]]
    assert document.fileContentList == result, ""
