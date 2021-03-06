"""list.py unit tests."""
import pypyr.parser.list
import pytest


def test_comma_string_parses_to_dict():
    """Comma delimited input returns dictionary key argList with value list."""
    out = pypyr.parser.list.get_parsed_context('value 1,value 2, value3')
    assert out['argList'] == ['value 1', 'value 2', ' value3']
    assert len(out) == 1, "1 item expected"
    assert len(out['argList']) == 3, "3 items expected in argList"


def test_no_commas_string_parses_to_single_entry():
    """No commas input string should return list with 1 item."""
    out = pypyr.parser.list.get_parsed_context('value 1 value 2 value3')
    assert out['argList'] == ['value 1 value 2 value3']
    assert len(out) == 1, "1 item expected in context"
    assert len(out['argList']) == 1, "1 item expected in argList"


def test_empty_string_throw():
    """Empty input string should throw assert error."""
    with pytest.raises(AssertionError) as err_info:
        pypyr.parser.list.get_parsed_context(None)

    assert repr(err_info.value) == (
        "AssertionError(\"pipeline must be invoked with context arg set. For "
        "this list parser you're looking for something like: "
        "pypyr pipelinename 'spam,eggs' "
        "OR: pypyr pipelinename 'spam'.\",)")


def test_builtin_list_still_works():
    """Don't break built-in list keyword."""
    test_list = [0, 1, 2]
    test_list.append(3)
    assert test_list.count(0) == 1
    test_list.extend([4, 5, 6])
    assert test_list == [0, 1, 2, 3, 4, 5, 6]
    assert isinstance(test_list, list)
