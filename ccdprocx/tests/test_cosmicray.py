# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np

from numpy.testing import assert_allclose
import pytest
from astropy.utils import NumpyRNGContext
from astropy.nddata import StdDevUncertainty
from astropy import units as u

# cosmicray_lacosmic,
from ccdprocx.core import (cosmicray_median,
                    background_deviation_box, background_deviation_filter)
from ccdprocx.tests.pytest_fixtures import ccd_data as ccd_data_func


DATA_SCALE = 5.3
NCRAYS = 30


def add_cosmicrays(data, scale, threshold, ncrays=NCRAYS):
    size = data.shape[0]
    with NumpyRNGContext(125):
        crrays = np.random.randint(0, size, size=(ncrays, 2))
        # use (threshold + 1) below to make sure cosmic ray is well above the
        # threshold no matter what the random number generator returns
        crflux = (10 * scale * np.random.random(NCRAYS) +
                  (threshold + 5) * scale)
        for i in range(ncrays):
            y, x = crrays[i]
            data.data[y, x] = crflux[i]


















#=============================================================================================================================
# def test_cosmicray_lacosmic():
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     threshold = 5
#     add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
#     noise = DATA_SCALE * np.ones_like(ccd_data.data)
#     data, crarr = cosmicray_lacosmic(ccd_data.data, sigclip=5)

#     # check the number of cosmic rays detected
#     # currently commented out while checking on issues
#     # in astroscrappy
#     # assert crarr.sum() == NCRAYS


# def test_cosmicray_lacosmic_ccddata():
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     threshold = 5
#     add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
#     noise = DATA_SCALE * np.ones_like(ccd_data.data)
#     ccd_data.uncertainty = noise
#     nccd_data = cosmicray_lacosmic(ccd_data, sigclip=5)

#     # check the number of cosmic rays detected
#     # currently commented out while checking on issues
#     # in astroscrappy
#     # assert nccd_data.mask.sum() == NCRAYS


# def test_cosmicray_lacosmic_check_data():
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     with pytest.raises(TypeError):
#         noise = DATA_SCALE * np.ones_like(ccd_data.data)
#         cosmicray_lacosmic(10, noise)


# @pytest.mark.parametrize('array_input', [True, False])
# @pytest.mark.parametrize('gain_correct_data', [True, False])
# def test_cosmicray_gain_correct(array_input, gain_correct_data):
#     # Add regression check for #705 and for the new gain_correct
#     # argument.
#     # The issue is that cosmicray_lacosmic gain-corrects the
#     # data and returns that gain corrected data. That is not the
#     # intent...
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     threshold = 5
#     add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
#     noise = DATA_SCALE * np.ones_like(ccd_data.data)
#     ccd_data.uncertainty = noise
#     # No units here on purpose.
#     gain = 2.0
#     # Don't really need to set this (6.5 is the default value) but want to
#     # make lack of units explicit.
#     readnoise = 6.5
#     if array_input:
#         new_data, cr_mask = cosmicray_lacosmic(ccd_data.data,
#                                                gain=gain,
#                                                gain_apply=gain_correct_data)
#     else:
#         new_ccd = cosmicray_lacosmic(ccd_data,
#                                      gain=gain,
#                                      gain_apply=gain_correct_data)
#         new_data = new_ccd.data
#         cr_mask = new_ccd.mask
#     # Fill masked locations with 0 since there is no simple relationship
#     # between the original value and the corrected value.
#     orig_data = np.ma.array(ccd_data.data, mask=cr_mask).filled(0)
#     new_data = np.ma.array(new_data.data, mask=cr_mask).filled(0)
#     if gain_correct_data:
#         gain_for_test = gain
#     else:
#         gain_for_test = 1.0

#     np.testing.assert_allclose(gain_for_test * orig_data, new_data)


# def test_cosmicray_lacosmic_accepts_quantity_gain():
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     threshold = 5
#     add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
#     noise = DATA_SCALE * np.ones_like(ccd_data.data)
#     ccd_data.uncertainty = noise
#     # The units below are the point of the test
#     gain = 2.0 * u.electron / u.adu

#     # Since gain and ccd_data have units, the readnoise should too.
#     readnoise = 6.5 * u.electron
#     new_ccd = cosmicray_lacosmic(ccd_data,
#                                  gain=gain,
#                                  gain_apply=True)


# def test_cosmicray_lacosmic_accepts_quantity_readnoise():
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     threshold = 5
#     add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
#     noise = DATA_SCALE * np.ones_like(ccd_data.data)
#     ccd_data.uncertainty = noise
#     gain = 2.0 * u.electron / u.adu
#     # The units below are the point of this test
#     readnoise = 6.5 * u.electron
#     new_ccd = cosmicray_lacosmic(ccd_data,
#                                  gain=gain,
#                                  gain_apply=True,
#                                  readnoise=readnoise)


# def test_cosmicray_lacosmic_detects_inconsistent_units():
#     # This is intended to detect cases like a ccd with units
#     # of adu, a readnoise in electrons and a gain in adu / electron.
#     # That is not internally inconsistent.
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     ccd_data.unit = 'adu'
#     threshold = 5
#     add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
#     noise = DATA_SCALE * np.ones_like(ccd_data.data)
#     ccd_data.uncertainty = noise
#     readnoise = 6.5 * u.electron

#     # The units below are deliberately incorrect.
#     gain = 2.0 * u.adu / u.electron
#     with pytest.raises(ValueError) as e:
#         cosmicray_lacosmic(ccd_data,
#                            gain=gain,
#                            gain_apply=True,
#                            readnoise=readnoise)
#     assert 'Inconsistent units' in str(e.value)


# def test_cosmicray_lacosmic_warns_on_ccd_in_electrons(recwarn):
#     # Check that an input ccd in electrons raises a warning.
#     ccd_data = ccd_data_func(data_scale=DATA_SCALE)
#     # The unit below is important for the test; this unit on
#     # input is supposed to raise an error.
#     ccd_data.unit = u.electron
#     threshold = 5
#     add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
#     noise = DATA_SCALE * np.ones_like(ccd_data.data)
#     ccd_data.uncertainty = noise
#     # No units here on purpose.
#     gain = 2.0
#     # Don't really need to set this (6.5 is the default value) but want to
#     # make lack of units explicit.
#     readnoise = 6.5
#     new_ccd = cosmicray_lacosmic(ccd_data,
#                                  gain=gain,
#                                  gain_apply=True,
#                                  readnoise=readnoise)

#     assert "Image unit is electron" in str(recwarn.pop())

#===================================================================================================================================























def test_cosmicray_median_check_data():
    with pytest.raises(TypeError):
        ndata, crarr = cosmicray_median(10, thresh=5, mbox=11,
                                        error_image=DATA_SCALE)


def test_cosmicray_median():
    ccd_data = ccd_data_func(data_scale=DATA_SCALE)
    threshold = 5
    add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
    ndata, crarr = cosmicray_median(ccd_data.data, thresh=5, mbox=11,
                                    error_image=DATA_SCALE)

    # check the number of cosmic rays detected
    assert crarr.sum() == NCRAYS


def test_cosmicray_median_ccddata():
    ccd_data = ccd_data_func(data_scale=DATA_SCALE)
    threshold = 5
    add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
    ccd_data.uncertainty = ccd_data.data*0.0+DATA_SCALE
    nccd = cosmicray_median(ccd_data, thresh=5, mbox=11,
                            error_image=None)

    # check the number of cosmic rays detected
    assert nccd.mask.sum() == NCRAYS


def test_cosmicray_median_masked():
    ccd_data = ccd_data_func(data_scale=DATA_SCALE)
    threshold = 5
    add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
    data = np.ma.masked_array(ccd_data.data, (ccd_data.data > -1e6))
    ndata, crarr = cosmicray_median(data, thresh=5, mbox=11,
                                    error_image=DATA_SCALE)

    # check the number of cosmic rays detected
    assert crarr.sum() == NCRAYS


def test_cosmicray_median_background_None():
    ccd_data = ccd_data_func(data_scale=DATA_SCALE)
    threshold = 5
    add_cosmicrays(ccd_data, DATA_SCALE, threshold, ncrays=NCRAYS)
    data, crarr = cosmicray_median(ccd_data.data, thresh=5, mbox=11,
                                   error_image=None)

    # check the number of cosmic rays detected
    assert crarr.sum() == NCRAYS


def test_cosmicray_median_gbox():
    ccd_data = ccd_data_func(data_scale=DATA_SCALE)
    scale = DATA_SCALE  # yuck. Maybe use pytest.parametrize?
    threshold = 5
    add_cosmicrays(ccd_data, scale, threshold, ncrays=NCRAYS)
    error = ccd_data.data*0.0+DATA_SCALE
    data, crarr = cosmicray_median(ccd_data.data, error_image=error,
                                   thresh=5, mbox=11, rbox=0, gbox=5)
    data = np.ma.masked_array(data, crarr)
    assert crarr.sum() > NCRAYS
    assert abs(data.std() - scale) < 0.1


def test_cosmicray_median_rbox():
    ccd_data = ccd_data_func(data_scale=DATA_SCALE)
    scale = DATA_SCALE  # yuck. Maybe use pytest.parametrize?
    threshold = 5
    add_cosmicrays(ccd_data, scale, threshold, ncrays=NCRAYS)
    error = ccd_data.data*0.0+DATA_SCALE
    data, crarr = cosmicray_median(ccd_data.data, error_image=error,
                                   thresh=5, mbox=11, rbox=21, gbox=5)
    assert data[crarr].mean() < ccd_data.data[crarr].mean()
    assert crarr.sum() > NCRAYS


def test_cosmicray_median_background_deviation():
    ccd_data = ccd_data_func(data_scale=DATA_SCALE)
    with pytest.raises(TypeError):
        cosmicray_median(ccd_data.data, thresh=5, mbox=11,
                         error_image='blank')


def test_background_deviation_box():
    with NumpyRNGContext(123):
        scale = 5.3
        cd = np.random.normal(loc=0, size=(100, 100), scale=scale)
    bd = background_deviation_box(cd, 25)
    assert abs(bd.mean() - scale) < 0.10


def test_background_deviation_box_fail():
    with NumpyRNGContext(123):
        scale = 5.3
        cd = np.random.normal(loc=0, size=(100, 100), scale=scale)
    with pytest.raises(ValueError):
        background_deviation_box(cd, 0.5)


def test_background_deviation_filter():
    with NumpyRNGContext(123):
        scale = 5.3
        cd = np.random.normal(loc=0, size=(100, 100), scale=scale)
    bd = background_deviation_filter(cd, 25)
    assert abs(bd.mean() - scale) < 0.10


def test_background_deviation_filter_fail():
    with NumpyRNGContext(123):
        scale = 5.3
        cd = np.random.normal(loc=0, size=(100, 100), scale=scale)
    with pytest.raises(ValueError):
        background_deviation_filter(cd, 0.5)
