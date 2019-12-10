# -*- coding: utf-8 -*-
"""Module providing classes for representing gaze coordinates.
"""

import pandas
import plotnine

from .geometry import acceleration
from .geometry import center
from .geometry import rotate
from .geometry import velocity
from .tools import check_shape
from .tools import _blockmanager_to_array


#%% Constants

INIT_COLUMNS = ['time', 'x', 'y']

RAW_DATA_COLUMNS = ['x_raw', 'y_raw']


#%% Main class

class GazeData(pandas.DataFrame):
    """Table of gaze data.

    A :class:`pandas.DataFrame` \
    with some extra methods for processing gaze data. \
    Most methods wrap functions from :mod:`.geometry`.
    """

    # pandas.DataFrame treats attributes as column names.
    # (This is one of the minor irritations of working with pandas;
    # it doesn't stick to *one* correct and intuitive method of indexing.)
    # So we must declare custom attributes here
    # to avoid them being treated as columns.
    # (Not yet implemented, but just in case.)
    # https://pandas.pydata.org/pandas-docs/stable/development/extending.html#define-original-properties
    # _internal_names = pandas.DataFrame._internal_names + []
    # _internal_names_set = set(_internal_names)

    def __new__(cls, data=None, *args, **kwargs):

        # When a new instance of the custom class is requested,
        # this can be for two different reasons:
        # (1) A completely new instance.
        # (2) A new instance from a subset of an existing instance.

        # We can detect (2) with the following clause.
        # But this is unfortunately not part of the pandas public API,
        # so we may have to watch out for changes in later pandas versions.
        # https://github.com/pandas-dev/pandas/blob/master/pandas/core/internals/managers.py
        if isinstance(data, pandas.core.internals.BlockManager):

            # A subset might still be a full valid table of gaze data,
            # if it contains the 3 essential columns 'time', 'x', and 'y'.
            # If so, we initialize an instance of the custom class.
            if all((col in list(data.items)) for col in INIT_COLUMNS):
                return super().__new__(cls)

            # Otherwise we initialize a standard pandas DataFrame.
            # This needs the array form of the data.
            return pandas.DataFrame(_blockmanager_to_array(data), columns=list(data.items))

        return super().__new__(cls)

    def __init__(self, data=None, *args, **kwargs):
        """:param data: Gaze data with shape *(n, 3)*, \
        where *n* is the number of gaze samples, \
        and columns are *time*, *x gaze position*, *y gaze position*.
        :type data: :class:`numpy.ndarray` \
        or convertible to :class:`numpy.ndarray`
        """

        # If a copy or view is explicitly requested, respect this.
        # Otherwise ensure we get a copy.
        if 'copy' not in kwargs:
            kwargs['copy'] = True

        # But if we are dealing with a valid subset (see above),
        # we want to preserve the columns of the subset.
        if isinstance(data, pandas.core.internals.BlockManager):
            kwargs['columns'] = list(data.items)

        # Otherwise if we are initializing from a pandas DataFrame,
        # we want to preserve the columns only if they are valid,
        # and reset the data to a bare array if not.
        elif isinstance(data, pandas.DataFrame):
            if all((col in data) for col in INIT_COLUMNS):
                kwargs['columns'] = data.columns
            else:
                data = check_shape(data, (None, 3))

        # Set new column names if none have been allocated so far.
        if 'columns' not in kwargs:
            kwargs['columns'] = INIT_COLUMNS

        super().__init__(data=data, *args, **kwargs)

    # To allow subsets of the custom class to preserve their type,
    # we need to override the constructor that subsetting calls.
    # Otherwise it will still call pandas.DataFrame().
    # https://pandas.pydata.org/pandas-docs/stable/development/extending.html#override-constructor-properties
    @property
    def _constructor(self):
        return GazeData

    def _save_raw_coords(self):

        if all((col not in self) for col in RAW_DATA_COLUMNS):
            self[RAW_DATA_COLUMNS] = self[['x', 'y']]

    def center(self, origin):
        """Center gaze coordinates.

        See :func:`.geometry.center`.
        """

        self._save_raw_coords()

        self[['x', 'y']] = center(self[['x', 'y']], origin)

    def rotate(self, theta, origin=(0., 0.)):
        """Rotate gaze coordinates.

        See :func:`.geometry.rotate`.
        """

        self._save_raw_coords()

        self[['x', 'y']] = rotate(self[['x', 'y']], theta, origin)

    def get_velocities(self):
        """Calculate velocity of gaze coordinates.

        Velocities are added as a new column.

        See :func:`.geometry.velocity`.
        """

        self['velocity'] = velocity(self[['time', 'x', 'y']])

    def get_accelerations(self):
        """Calculate acceleration of gaze coordinates.

        Accelerations are added as a new column. \
        If necessary, a column of velocities is also added.

        See :func:`.geometry.acceleration`.
        """

        if 'velocity' not in self:
            self.get_velocities()

        self['acceleration'] = acceleration(self['time'], self['velocity'])

    def detect_saccades(self, func, **kwargs):
        """Mark samples as part of a saccade.

        Function `func` is used to create a new boolean column \
        called 'saccade', which marks samples as part of a saccade. \
        `func` should take a :class:`Gazedata` table \
        as its first input argument, \
        and return a boolean array of length equal to \
        the number of rows in the table.

        Additional keyword arguments are passed on to `func`.

        See :mod:`.saccadedetection` for some ready-made \
        saccade detection algorithms.

        :param func: Algorithm for detecting saccades.
        :type func: function
        """

        self['saccade'] = func(self, **kwargs)

    def plot(self, reverse_y=False, show_raw=False, saccades=False, filename=None, verbose=False, **kwargs):
        """Plot gaze coordinates.

        Plotting is done with :mod:`plotnine` because it is good.

        Additional keyword arguments are passed on to \
        :meth:`plotnine.ggplot.save`

        :param reverse_y: Many eyetracking systems \
        use a coordinate system in which the *y* axis points downward. \
        This argument reverses the y axis so that the plot \
        matches such a system visually.
        :type reverse_y: bool
        :param show_raw: If transformations have been applied, \
        the GazeData object will have saved the raw coordinates. \
        This argument additionally displays the raw data, \
        for comparison before and after transformation.
        :type show_raw: bool
        :param saccades: Whether to plot saccades. \
        If saccade detection has been applied, \
        saccades are shown in red. \
        Otherwise this argument is ignored.
        :type saccades: bool
        :param filename: File to save image to. \
        By default, no image file is saved.
        :type filename: str
        :param verbose: Passed on to :meth:`plotnine.ggplot.save` \
        but with a less annoying default value.
        :type verbose: bool
        :return: Plot object. Can be further customized \
        by adding plot elements from :mod:`plotnine`.
        :rtype: :class:`plotnine.ggplot`
        """

        # There seem to be some complex problems
        # using a subclass of pandas.DataFrame with plotnine,
        # so as a simple fix, create a dataframe for plotting.
        df = pandas.DataFrame(self)

        fig = (plotnine.ggplot(df, plotnine.aes(x='x', y='y'))
               + plotnine.coord_equal())  # noqa: W503

        if reverse_y:
            fig = fig + plotnine.scale_y_continuous(trans='reverse')

        if show_raw:
            fig = fig + plotnine.geom_line(plotnine.aes(x='x_raw', y='y_raw'),
                                           linetype='dashed')

        fig = fig + plotnine.geom_line()

        if saccades and ('saccade' in self):
            fig = fig + plotnine.geom_line(data=df[df['saccade']],
                                           color='red')

        if filename:
            fig.save(filename, verbose=verbose, **kwargs)

        return fig
