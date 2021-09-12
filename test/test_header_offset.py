import jmd.jmd as jmd

# def headerOffset(element):
#     element[1] = re.sub(JmdPatterns.pattern_titles,
#                         JmdPatterns.sub_titles, element[1])
#     element[2] = re.sub(JmdPatterns.pattern_titles,
#                         JmdPatterns.sub_titles, element[2])


def test_headerOffset():
    element = [1, "This is the file content.", "# This is the title", ""]
    result = jmd.headerOffset(element)
    assert result == [1, "This is the file content.",
                      "## This is the title", ""], ""


def test_headerOffsetSubtitleLevel2():
    element = [1, "## This is the file content.", "# This is the title", ""]
    result = jmd.headerOffset(element)
    assert result == [1, "### This is the file content.",
                      "## This is the title", ""], ""


def test_headerOffsetSubtitleLevel3():
    element = [1, "### This is the file content.", "# This is the title", ""]
    result = jmd.headerOffset(element)
    assert result == [1, "#### This is the file content.",
                      "## This is the title", ""], ""


def test_headerOffsetSubtitleLevel4():
    element = [1, "#### This is the file content.", "# This is the title", ""]
    result = jmd.headerOffset(element)
    assert result == [1, "##### This is the file content.",
                      "## This is the title", ""], ""


def test_headerOffsetSubtitleLevel5():
    element = [1, "##### This is the file content.", "# This is the title", ""]
    result = jmd.headerOffset(element)
    assert result == [1, "###### This is the file content.",
                      "## This is the title", ""], ""
