"""
Module to run tests on SciImgStack class
Requires files in Development suite
"""
import os

import pytest
import numpy as np

from pypeit.spectrographs.util import load_spectrograph
from pypeit.images import buildimage
from pypeit.images import pypeitimage
from pypeit import flatfield
from pypeit.tests.tstutils import data_path


kast_blue = load_spectrograph('shane_kast_blue')
kast_par = kast_blue.default_pypeit_par()
keck_nires = load_spectrograph('keck_nires')


@pytest.fixture
def shane_kast_blue_sci_files():
    return [os.path.join(os.getenv('PYPEIT_DEV'), 
                         'RAW_DATA', 'shane_kast_blue', 
                         '600_4310_d55',
                         ifile) for ifile in ['b27.fits.gz', 
                                              'b28.fits.gz']]

@pytest.fixture
def nires_sci_files():
    return [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 
                         'keck_nires', 'ABBA_wstandard', ifile)
            for ifile in ['s190519_0060.fits']]


@pytest.fixture
def nires_bg_files():
    return [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 
                         'keck_nires', 'ABBA_wstandard', ifile)
            for ifile in ['s190519_0059.fits']]


def test_proc_diff(nires_sci_files, nires_bg_files):
    """
    Run on near-IR frames
    """
    # Setup
    det = 1
    bpm = np.zeros((2048,1024), dtype=int)
    pixelflat = np.ones(bpm.shape, dtype=float)
    nires_par = keck_nires.default_pypeit_par()

    # Sci image
    flatImages = flatfield.FlatImages(pixelflat_norm=pixelflat)
    nires_par['scienceframe']['process']['use_illumflat'] = False
    nires_par['scienceframe']['process']['use_specillum'] = False
    sciImg = buildimage.buildimage_fromlist(keck_nires, det, nires_par['scienceframe'],
                                            nires_sci_files, bias=None, bpm=bpm,
                                            flatimages=flatImages)
    # Bg image
    bgImg = buildimage.buildimage_fromlist(keck_nires, det, nires_par['scienceframe'],
                                           nires_bg_files, bias=None, bpm=bpm,
                                           flatimages=flatImages)
    # Difference
    sciImg = sciImg.sub(bgImg)
    # Test
    assert isinstance(sciImg, pypeitimage.PypeItImage)



