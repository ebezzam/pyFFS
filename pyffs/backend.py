# #############################################################################
# backend.py
# ==========
# Authors :
# Eric Bezzam [ebezzam@gmail.com]
# #############################################################################

"""
Methods for identifying the appropriate backend between `numpy` and `cupy`.

Code is heavily inspired by `PyLops` library: https://github.com/PyLops/pylops/blob/master/pylops/utils/backend.py
"""

import os
from importlib import util
import numpy as np
from scipy import fftpack as fftpack


cupy_enabled = util.find_spec("cupy") is not None and int(os.getenv("CUPY_PYFFS", 1)) == 1
if cupy_enabled:
    import cupy as cp


def get_module(backend="numpy"):
    """
    Returns correct numerical module based on backend string.

    Parameters
    ----------
    backend : :obj:`str`, optional
        Backend used for computations (``numpy`` or ``cupy``).

    Returns
    -------
    mod : :obj:`func`
        Module to be used to process arrays (:mod:`numpy` or :mod:`cupy`).
    """
    if backend == "numpy":
        xp = np
    elif backend == "cupy":
        xp = cp
    else:
        raise ValueError("backend must be `numpy` or `cupy`")
    return xp


def get_module_name(mod):
    """
    Returns name of numerical module based on input numerical module.

    Parameters
    ----------
    mod : :obj:`func`
        Module to be used to process array (:mod:`numpy` or :mod:`cupy`).

    Returns
    -------
    backend : :obj:`str`, optional
        Backend used for dot test computations (``numpy`` or ``cupy``).
    """
    if mod == np:
        backend = "numpy"
    elif mod == cp:
        backend = "cupy"
    else:
        raise ValueError("module must be `numpy` or `cupy`")
    return backend


def get_backend():
    if cupy_enabled:
        return cp
    else:
        return np


def get_array_module(x):
    """
    Returns correct numerical module based on input.

    Parameters
    ----------
    x : :obj:`numpy.ndarray` or :obj:`cupy.ndarray`
        Array

    Returns
    -------
    mod : :obj:`func`
        Module to be used to process array (:mod:`numpy` or :mod:`cupy`)
    """
    if cupy_enabled:
        return cp.get_array_module(x)
    else:
        return np


def fftn(x, axes=None):
    """
    Applies correct fftn module based on input.

    Parameters
    ----------
    x : :obj:`numpy.ndarray` or :obj:`cupy.ndarray`
        Array
    axes : tuple
        Dimension of `x` along which to perform FFT.

    Returns
    -------
    mod : :obj:`func`
        Module to be used to process array (:mod:`numpy` or :mod:`cupy`)
    """

    if get_array_module(x) == np:
        return fftpack.fftn(x, axes=axes)
    else:
        return cp.fft.fftn(x, axes=axes)


def ifftn(x, axes=None):
    """
    Apply correct ifftn module based on input.

    Parameters
    ----------
    x : :obj:`numpy.ndarray` or :obj:`cupy.ndarray`
        Array
    axes : tuple
        Dimension of `x` along which to perform IFFT.

    Returns
    -------
    mod : :obj:`func`
        Module to be used to process array (:mod:`numpy` or :mod:`cupy`)
    """

    if get_array_module(x) == np:
        return fftpack.ifftn(x, axes=axes)
    else:
        return cp.fft.ifftn(x, axes=axes)