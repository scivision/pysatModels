"""
Supports loading data from files generated using the Gemini3D model.
Gemini3D HDF5 files have multiple dimensions for most variables.
The PyGemini project is at https://www.github.com/gemini3d/pygemini

Properties
----------
platform
    'pygemini'
name
    'gemini3d'
tag
    None supported
inst_id
    None supported

"""

import datetime as dt
import functools
import os
import requests
import warnings

import pysat

logger = pysat.logger

# ----------------------------------------------------------------------------
# Instrument attributes

platform = "pygemini"
name = "gemini3d"
tags = {
    "": "pygemini output file",
    "test": "Standard output of pygemini for benchmarking",
}
inst_ids = {"": ["", "test"]}

# specify using xarray (not using pandas)
pandas_format = False

# ----------------------------------------------------------------------------
# Instrument test attributes

_test_dates = {
    "": {tag: dt.datetime(2012, 2, 20, 5, 0, 0) for tag in tags.keys()}
}
_test_download = {"": {"": False, "test": True}}

# ----------------------------------------------------------------------------
# Instrument methods


def init(self):
    """Initializes the Instrument object with instrument specific values.

    Runs once upon instantiation.

    Parameters
    ----------
    self : pysat.Instrument
        This object

    """

    self.acknowledgements = (
        "The Gemini3D model and PyGemini interface "
        "were developed by Matthew Zettergren and "
        "Michael Hirsch under NSF CAREER and NASA "
        "HDEE funding along with PI Joshua Semeter "
        "and Co-I Jeffrey Klenzing."
    )
    self.references = ""
    logger.info(self.acknowledgements)

    return


# Required method
def clean(self):
    """Method to return Gemini3D data cleaned to the specified level

    Cleaning level is specified in inst.clean_level and pysat
    will accept user input for several strings. The clean_level is
    specified at instantiation of the Instrument object, though it may be
    updated to a more stringent level and re-applied after instantiation.
    The clean method is applied after default every time data is loaded.

    Note
    ----
    'clean' All parameters should be good, suitable for statistical and
            case studies
    'dusty' All paramers should generally be good though same may
            not be great
    'dirty' There are data areas that have issues, data should be used
            with caution
    'none'  No cleaning applied, routine not called in this case.

    """

    logger.info("Cleaning not supported for Gemini3D")

    return


# ----------------------------------------------------------------------------
# Instrument functions
#
# Use local and default pysat methods

# Set the list_files routine
fname = ("{year:04d}{month:02d}{day:02d}_"
         "{hour*3600 + minute*60 + second:05d}.{microsecond:06d}.h5")
supported_tags = {"": {"": fname, "test": fname}}
list_files = functools.partial(
    pysat.instruments.methods.general.list_files, supported_tags=supported_tags
)


def load(fnames, tag=None, inst_id=None, **kwargs):
    """Loads pygemini data using xarray.

    This routine is called as needed by pysat. It is not intended
    for direct user interaction.

    Parameters
    ----------
    fnames : array-like
        iterable of filename strings, full path, to data files to be loaded.
        This input is nominally provided by pysat itself.
    tag : string ('')
        tag name used to identify particular data set to be loaded.
        This input is nominally provided by pysat itself.
    inst_id : string ('')
        Instrument ID used to identify particular data set to be loaded.
        This input is nominally provided by pysat itself.
    **kwargs : extra keywords
        Passthrough for additional keyword arguments specified when
        instantiating an Instrument object. These additional keywords
        are passed through to this routine by pysat.

    Returns
    -------
    data : xarray.Dataset
        pysat formatted xarray Dataset
    meta : pysat.Metadata
        Model run meta data

    Note
    ----
    Any additional keyword arguments passed to pysat.Instrument
    upon instantiation are passed along to this routine.

    Examples
    --------
    ::

        inst = pysat.Instrument('pygemini', 'gemini3d')
        inst.load(2012, 2, 20, 5, 0, 0)

    """

    # load data
    data, meta = pysat.utils.load_netcdf4(fnames, pandas_format=False)

    # add time variable for pysat compatibilty
    data["time"] = [
        dt.datetime(2012, 2, 20, 5, 0, 0)
        + dt.timedelta(seconds=int(val * 3600.0))
        for val in data["ut"].values
    ]

    return data, meta


def download(date_array=None, tag=None, inst_id=None, data_path=None, **kwargs):
    """Downloads pygemini test data.

    Parameters
    ----------
    date_array : array-like
        list of datetimes to download data for. The sequence of dates need not
        be contiguous.
    tag : string
        Tag identifier used for particular dataset. This input is provided by
        pysat. (default='')
    inst_id : string
        Instrument ID string identifier used for particular dataset. This input
        is provided by pysat. (default='')
    data_path : string
        Path to directory to download data to. (default=None)
    **kwargs : dict
        Additional keywords supplied by user when invoking the download
        routine attached to a pysat.Instrument object are passed to this
        routine via kwargs.

    Note
    ----
    This routine is invoked by pysat and is not intended for direct use by
    the end user.

    The test object generates the datetime requested by the user, which may not
    match the date of the model run.

    """

    if tag == "test":
        date = date_array[0]
        remote_url = "https://www.zenodo.org/record/"
        remote_path = "4043048/files"

        # Need to tell github to show the raw data, not the webpage version
        fname = "test2dew_fang.zip?download=1"

        # Use pysat-compatible name
        format_str = supported_tags[inst_id][tag]
        saved_local_fname = os.path.join(
            data_path,
            format_str.format(year=date.year, month=date.month, day=date.day),
        )
        remote_path = "/".join(
            (remote_url.strip("/"), remote_path.strip("/"), fname)
        )
        req = requests.get(remote_path)
        if req.status_code != 404:
            open(saved_local_fname, "wb").write(req.content)

    else:
        warnings.warn("Downloads currently only supported for test files.")

    return
