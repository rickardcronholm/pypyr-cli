"""env.py unit tests."""
import os
from pypyr.context import Context
import pypyr.steps.env
import pytest
from unittest.mock import patch, DEFAULT

# ------------------------- env base -----------------------------------------#


def test_env_throws_on_empty_context():
    """context must exist."""
    with pytest.raises(AssertionError) as err_info:
        pypyr.steps.env.run_step(None)

    assert repr(err_info.value) == ("AssertionError('context must have value "
                                    "for pypyr.steps.env',)")


def test_env_throws_if_all_env_context_missing():
    """env context keys must exist."""
    with pytest.raises(AssertionError) as err_info:
        pypyr.steps.env.run_step(Context({'arbkey': 'arbvalue'}))

    assert repr(err_info.value) == ("AssertionError('context must contain "
                                    "any combination of envGet, envSet or "
                                    "envUnset for pypyr.steps.env',)")


def test_env_throws_if_env_context_wrong_type():
    """env context keys must exist."""
    with pytest.raises(AssertionError) as err_info:
        pypyr.steps.env.run_step(
            Context({'envSet': 'it shouldnt be a string'}))

    assert repr(err_info.value) == ("AssertionError('context must contain "
                                    "any combination of envGet, envSet or "
                                    "envUnset for pypyr.steps.env',)")


def test_env_only_calls_get():
    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envGet': {
            'key2': 'ARB_GET_ME1',
            'key4': 'ARB_GET_ME2'
        }
    })

    with patch.multiple('pypyr.steps.env',
                        env_get=DEFAULT,
                        env_set=DEFAULT,
                        env_unset=DEFAULT
                        ) as mock_env:
        pypyr.steps.env.run_step(context)

    mock_env['env_get'].assert_called_once()
    mock_env['env_set'].assert_not_called()
    mock_env['env_unset'].assert_not_called()


def test_env_only_calls_set():
    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envSet': {
            'ARB_SET_ME1': 'key2',
            'ARB_SET_ME2': 'key1'
        }
    })

    with patch.multiple('pypyr.steps.env',
                        env_get=DEFAULT,
                        env_set=DEFAULT,
                        env_unset=DEFAULT
                        ) as mock_env:
        pypyr.steps.env.run_step(context)

    mock_env['env_get'].assert_not_called()
    mock_env['env_set'].assert_called_once()
    mock_env['env_unset'].assert_not_called()


def test_env_only_calls_unset():
    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envUnset': [
            'ARB_DELETE_ME1',
            'ARB_DELETE_ME2'
        ]
    })

    with patch.multiple('pypyr.steps.env',
                        env_get=DEFAULT,
                        env_set=DEFAULT,
                        env_unset=DEFAULT
                        ) as mock_env:
        pypyr.steps.env.run_step(context)

    mock_env['env_get'].assert_not_called()
    mock_env['env_set'].assert_not_called()
    mock_env['env_unset'].assert_called_once()


def test_env_only_calls_set_unset():
    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envUnset': [
            'ARB_DELETE_ME1',
            'ARB_DELETE_ME2'
        ],
        'envSet': {
            'ARB_SET_ME1': 'key2',
            'ARB_SET_ME2': 'key1'
        }
    })

    with patch.multiple('pypyr.steps.env',
                        env_get=DEFAULT,
                        env_set=DEFAULT,
                        env_unset=DEFAULT
                        ) as mock_env:
        pypyr.steps.env.run_step(context)

    mock_env['env_get'].assert_not_called()
    mock_env['env_set'].assert_called_once()
    mock_env['env_unset'].assert_called_once()


def test_env_all_operations():
    """env should run all specified operations"""
    os.environ['ARB_GET_ME1'] = 'arb value from $ENV ARB_GET_ME1'
    os.environ['ARB_GET_ME2'] = 'arb value from $ENV ARB_GET_ME2'
    os.environ['ARB_DELETE_ME1'] = 'arb value from $ENV ARB_DELETE_ME1'
    os.environ['ARB_DELETE_ME2'] = 'arb value from $ENV ARB_DELETE_ME2'

    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envGet': {
            'key2': 'ARB_GET_ME1',
            'key4': 'ARB_GET_ME2'
        },
        'envSet': {
            'ARB_SET_ME1': 'value 4',
            'ARB_SET_ME2': 'go go {key2} end end'
        },
        'envUnset': [
            'ARB_DELETE_ME1',
            'ARB_DELETE_ME2'
        ]
    })

    pypyr.steps.env.run_step(context)

    assert context['key1'] == 'value1'
    assert context['key2'] == 'arb value from $ENV ARB_GET_ME1'
    assert context['key3'] == 'value3'
    assert context['key4'] == 'arb value from $ENV ARB_GET_ME2'
    assert os.environ['ARB_SET_ME1'] == 'value 4'
    assert os.environ['ARB_SET_ME2'] == ('go go arb value from '
                                         '$ENV ARB_GET_ME1 end end')
    assert 'ARB_DELETE_ME1' not in os.environ
    assert 'ARB_DELETE_ME2' not in os.environ

    del os.environ['ARB_GET_ME1']
    del os.environ['ARB_GET_ME2']
    del os.environ['ARB_SET_ME1']
    del os.environ['ARB_SET_ME2']

# ------------------------- env base -----------------------------------------#
#
# ------------------------- envGet -------------------------------------------#


def test_envget_pass():
    """envget success case"""
    os.environ['ARB_DELETE_ME1'] = 'arb value from $ENV ARB_DELETE_ME1'
    os.environ['ARB_DELETE_ME2'] = 'arb value from $ENV ARB_DELETE_ME2'

    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envGet': {
            'key2': 'ARB_DELETE_ME1',
            'key4': 'ARB_DELETE_ME2'
        }
    })

    pypyr.steps.env.env_get(context)

    assert context['key1'] == 'value1'
    assert context['key2'] == 'arb value from $ENV ARB_DELETE_ME1'
    assert context['key3'] == 'value3'
    assert context['key4'] == 'arb value from $ENV ARB_DELETE_ME2'

    del os.environ['ARB_DELETE_ME1']
    del os.environ['ARB_DELETE_ME2']


def test_envget_env_doesnt_exist():
    """envget when $ENV doesn't exist"""
    os.environ['ARB_DELETE_ME2'] = 'arb from pypyr context ARB_DELETE_ME2'

    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envGet': {
            'key2': 'ARB_DELETE_ME1',
            'key4': 'ARB_DELETE_ME2'
        }
    })

    with pytest.raises(KeyError) as err_info:
        pypyr.steps.env.env_get(context)

    assert repr(err_info.value) == ("KeyError('ARB_DELETE_ME1',)")
    del os.environ['ARB_DELETE_ME2']
# ------------------------- envGet -------------------------------------------#

# ------------------------- envSet -------------------------------------------#


def test_envset_pass():
    """envset success case"""
    # Deliberately have 1 pre-existing $ENV to update, and 1 unset so can
    # create it anew as part of test
    os.environ['ARB_DELETE_ME2'] = 'arb from pypyr context ARB_DELETE_ME2'

    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envSet': {
            'ARB_DELETE_ME1': 'text value 2',
            'ARB_DELETE_ME2': 'text value 1'
        }
    })

    pypyr.steps.env.env_set(context)

    assert os.environ['ARB_DELETE_ME1'] == 'text value 2'
    assert os.environ['ARB_DELETE_ME2'] == 'text value 1'

    del os.environ['ARB_DELETE_ME1']
    del os.environ['ARB_DELETE_ME2']


def test_envset_with_string_interpolation():
    """envset success case"""
    # Deliberately have 1 pre-existing $ENV to update, and 1 unset so can
    # create it anew as part of test
    os.environ['ARB_DELETE_ME2'] = 'arb from pypyr context ARB_DELETE_ME2'

    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envSet': {
            'ARB_DELETE_ME1': 'blah blah {key2} and {key1} goes here.',
            'ARB_DELETE_ME2': 'plain old string',
            'ARB_DELETE_ME3': '{key3}'
        }
    })

    pypyr.steps.env.env_set(context)

    assert os.environ['ARB_DELETE_ME1'] == ('blah blah value2 and value1 goes '
                                            'here.')
    assert os.environ['ARB_DELETE_ME2'] == 'plain old string'
    assert os.environ['ARB_DELETE_ME3'] == 'value3'

    del os.environ['ARB_DELETE_ME1']
    del os.environ['ARB_DELETE_ME2']
    del os.environ['ARB_DELETE_ME3']

# ------------------------- envSet -------------------------------------------#

# ------------------------- envUnset -----------------------------------------#


def test_envunset_pass():
    """envUnset success case"""
    # Deliberately have 1 pre-existing $ENV to update, and 1 unset so can
    # create it anew as part of test
    os.environ['ARB_DELETE_ME1'] = 'arb from pypyr context ARB_DELETE_ME1'
    os.environ['ARB_DELETE_ME2'] = 'arb from pypyr context ARB_DELETE_ME2'

    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envUnset': [
            'ARB_DELETE_ME1',
            'ARB_DELETE_ME2'
        ]
    })

    pypyr.steps.env.env_unset(context)

    assert 'ARB_DELETE_ME1' not in os.environ
    assert 'ARB_DELETE_ME2' not in os.environ


def test_envunset_doesnt_exist():
    """envUnset success case"""
    # Make sure $ENV isn't set
    try:
        del os.environ['ARB_DELETE_SNARK']
    except KeyError:
        pass

    context = Context({
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'envUnset': [
            'ARB_DELETE_SNARK'
        ]
    })

    pypyr.steps.env.env_unset(context)

    assert 'ARB_DELETE_SNARK' not in os.environ

# ------------------------- envUnset -----------------------------------------#
