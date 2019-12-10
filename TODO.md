# TODOs

* Functions for converting distances to degrees of visual angle.
  * We will need some way of storing and using the necessary parameters, such as screen dimensions, viewing distance, etc.
  * These could be stored as attributes of the `GazeData` object.
  * But `pandas` makes storing custom attributes difficult.
* A method to the `GazeData` class that returns saccades.
* Functions for gaze coordinate smoothing.
  * `scipy` and `pandas` have some ready-made smoothing algorithms.
  * But one difficulty is taking into account the *time* column.
  * A method to the `GazeData` class that accepts these functions as arguments.
* A sequence-like class that groups multiple `GazeData` objects as trials in an experiment.
  * This class should store the metadata for the experiment, such as screen dimensions, time units, etc.
  * Functions for reading the various text eyetracking data formats into such objects.
    * Base these on the example data files in *tests/data*.
