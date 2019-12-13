# -*- coding: utf-8 -*-
"""Classes for representing gaze coordinates and saccades.
"""

import functools

import pandas
import plotnine

from .conversions import dva_to_px
from .conversions import px_to_dva
from .geometry import acceleration
from .geometry import center
from .geometry import rotate
from .geometry import velocity
from . import metrics
from .tools import check_shape
from .tools import find_contiguous_subsets
from .tools import _blockmanager_to_dataframe


#%% Constants

ATTRIBUTES = ['time_units',
              'space_units',
              'screen_res',
              'screen_diag',
              'viewing_dist',
              'target']

INIT_COLUMNS = ['time', 'x', 'y']

RAW_DATA_COLUMNS = ['x_raw', 'y_raw']


#%% Main class

class GazeData(pandas.DataFrame):
    """Table of gaze data.

    A :class:`pandas.DataFrame` \
    with some extra methods for processing gaze data. \
    Many methods wrap functions from :mod:`.geometry` \
    and :mod:`.conversions`.
    """

    # pandas.DataFrame treats attributes as column names.
    # (This is one of the minor irritations of working with pandas;
    # it doesn't stick to *one* correct and intuitive method of indexing.)
    # So we must declare custom attributes here
    # to avoid them being treated as columns.
    # https://pandas.pydata.org/pandas-docs/stable/development/extending.html#define-original-properties
    _metadata = ATTRIBUTES

    def __new__(cls, data=None, **kwargs):

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
            return _blockmanager_to_dataframe(data)

        return super().__new__(cls)

    def __init__(self, data=None, **kwargs):
        """Initialize a new table of gaze data.

        :param data: Gaze data with shape *(n, 3)*, \
        where *n* is the number of gaze samples, \
        and columns are *time*, *x gaze position*, *y gaze position*.
        :type data: :class:`numpy.ndarray` \
        or convertible to :class:`numpy.ndarray`
        :param time_units: Units of *time* column.
        :type time_units: str
        :param space_units: Units of *x* and *y* columns. \
        Pass `'dva'` to indicate that no conversion to \
        degrees of visual angle is necessary.
        :type space_units: str
        :param screen_res: *(x, y)* screen resolution, \
        in the same units as *x* and *y* gaze coordinates \
        (usually pixels).
        :type screen_res: tuple
        :param screen_diag: Diagonal size of screen, \
        in the same units as `viewing_dist`.
        :type screen_diag: float
        :param viewing_dist: Distance of eye from screen, \
        in the same units as `screen_diag`.
        :type viewing_dist: float
        :param target: *(x, y)* coordinates of saccade target, if any.
        :type target: tuple
        """

        # Set attributes according to the following priorities:
        # Use values set in the keyword arguments to __init__().
        # Else if initializing from an existing instance, use its attributes.
        # Else None.
        for attr in ATTRIBUTES:
            setattr(self, attr, kwargs.pop(attr, getattr(data, attr, None)))

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

        super().__init__(data=data, **kwargs)

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

    def _check_screen_info(self):

        ok = True
        msg = 'The following necessary attributes have not yet been set:'

        for attr in ['screen_res', 'screen_diag', 'viewing_dist']:
            if getattr(self, attr) is None:
                msg = msg + ' {} '.format(attr)
                ok = False

        if not ok:
            raise AttributeError(msg)

    def reset_time(self):
        """Reset the *time* column.

        The first *time* value is subtracted from all the others \
        so that *time* indicates time since first sample.
        """

        self['time'] = self['time'] - self['time'].iloc[0]

    def px_to_dva(self, px):
        """Convert pixels to degrees of visual angle.

        See :func:`.conversions.px_to_dva`.
        """

        self._check_screen_info()

        return px_to_dva(px,
                         screen_res=self.screen_res,
                         screen_diag=self.screen_diag,
                         viewing_dist=self.viewing_dist)

    def dva_to_px(self, dva):
        """Convert degrees of visual angle to pixels.

        See :func:`.conversions.dva_to_px`.
        """

        self._check_screen_info()

        return dva_to_px(dva,
                         screen_res=self.screen_res,
                         screen_diag=self.screen_diag,
                         viewing_dist=self.viewing_dist)

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

        Values are converted to degrees of visual angle using \
        attributes `screen_res`, `screen_diag`, and `viewing_dist`, \
        unless the attribute `space_units` is `'dva'`, \
        in which case no conversion is performed.

        See :func:`.geometry.velocity`.
        """

        velocities = velocity(self[['time', 'x', 'y']])

        if self.space_units != 'dva':
            velocities = self.px_to_dva(velocities)

        self['velocity'] = velocities

    def get_accelerations(self):
        """Calculate acceleration of gaze coordinates.

        Accelerations are added as a new column. \
        If necessary, a column of velocities is also added.

        See :func:`.geometry.acceleration`.
        """

        if 'velocity' not in self:
            self.get_velocities()

        self['acceleration'] = acceleration(self['time'], self['velocity'])

    def detect_saccades(self, func=None, n=None, **kwargs):
        """Get saccades from gaze data.

        Function `func` is used to detect saccades. \
        `func` should take a :class:`Gazedata` table \
        as its first input argument, \
        and return a boolean array of length equal to \
        the number of rows in the table \
        and which marks samples as being (or not being) \
        part of a saccade. \
        If no function is supplied \
        but saccades have previously been detected, \
        the stored saccades are returned again.

        Additional keyword arguments are passed on to `func`.

        See :mod:`.saccadedetection` for some ready-made \
        saccade detection algorithms.

        :param func: Algorithm for detecting saccades.
        :type func: function
        :param n: Maximum number of saccades to extract. \
        Defaults to extracting all.
        :type n: int
        :return: Subsets of gaze data, each containing one saccade.
        :rtype: list
        :raises KeyError: If no function is supplied, \
        and no 'saccade' column is yet present.
        """

        if func:
            self['saccade'] = func(self, **kwargs)
        elif 'saccade' not in self:
            raise KeyError('Saccade detection function required but not supplied.')

        slices = find_contiguous_subsets(self['saccade'])

        if n is not None:
            slices = slices[:n]

        return [Saccade(self[i]) for i in slices]

    def plot(self, reverse_y=False, show_raw=False, saccades=False,
             filename=None, verbose=False, **kwargs):
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

        fig = (plotnine.ggplot(self, plotnine.aes(x='x', y='y'))
               + plotnine.coord_equal())  # noqa: W503

        if reverse_y:
            fig = fig + plotnine.scale_y_continuous(trans='reverse')

        if show_raw:
            fig = fig + plotnine.geom_line(plotnine.aes(x='x_raw', y='y_raw'),
                                           linetype='dashed')

        fig = fig + plotnine.geom_line()

        if saccades and ('saccade' in self):
            fig = fig + plotnine.geom_line(data=self[self['saccade']],
                                           color='red')

        if filename:
            fig.save(filename, verbose=verbose, **kwargs)

        return fig


#%% Saccade subclass

class Saccade(GazeData):
    """Table of gaze data containing a saccade.

    A subclass of :class:`GazeData`.

    Additional methods calculate saccade metrics \
    using functions from :mod:`.metrics` with the same name.
    """

    @property
    def _constructor(self):
        return Saccade

    # This makes all suitable functions from metrics
    # into methods of the Saccade class.
    def __getattr__(self, name):

        if name in metrics.SACCADE_METRICS:
            return functools.partial(getattr(metrics, name), self)
        else:
            return super().__getattr__(name)
