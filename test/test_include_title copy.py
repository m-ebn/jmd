import jmd.jmd as jmd


def test_title():
    element = [1, "This is the file content.", "This is the title", ""]
    result = jmd.includeTitle(element)
    assert result == [1, "\n\nThis is the file content.",
                      "# This is the title", ""], ""
