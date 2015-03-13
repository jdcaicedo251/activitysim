# ActivitySim
# Copyright (C) 2014-2015 Synthicity, LLC
# See full license in LICENSE.txt.

import os.path

import pandas as pd
import pandas.util.testing as pdt
import pytest

from ..activitysim import eval_variables
from .. import mnl


# this is lifted straight from urbansim's test_mnl.py
@pytest.fixture(scope='module', params=[
    ('fish.csv',
        'fish_choosers.csv',
        pd.DataFrame(
            [[-0.02047652], [0.95309824]], index=['price', 'catch'],
            columns=['Alt']),
        pd.DataFrame([
            [0.2849598, 0.2742482, 0.1605457, 0.2802463],
            [0.1498991, 0.4542377, 0.2600969, 0.1357664]],
            columns=['beach', 'boat', 'charter', 'pier']))])
def test_data(request):
    data, choosers, spec, probabilities = request.param
    return {
        'data': data,
        'choosers': choosers,
        'spec': spec,
        'probabilities': probabilities
    }


@pytest.fixture
def choosers(test_data):
    filen = os.path.join(
        os.path.dirname(__file__), 'data', test_data['choosers'])
    return pd.read_csv(filen)


@pytest.fixture
def spec(test_data):
    return test_data['spec']


@pytest.fixture
def choosers_dm(choosers, spec):
    return eval_variables(spec.index, choosers)


@pytest.fixture
def utilities(choosers_dm, spec, test_data):
    utils = choosers_dm.dot(spec).astype('float')
    return pd.DataFrame(
        utils.as_matrix().reshape(test_data['probabilities'].shape),
        columns=test_data['probabilities'].columns)


def test_mnl(utilities, test_data):
    probs = mnl.utils_to_probs(utilities)
    pdt.assert_frame_equal(probs, test_data['probabilities'])
