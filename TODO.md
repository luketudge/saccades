# TODOs

* Functions for saccade metrics.
* A function for the 'velocity peak' saccade detection algorithm.
* Functions for gaze coordinate smoothing.
  * `scipy` and `pandas` have some ready-made smoothing algorithms. But one difficulty is taking into account the *time* column.
  * A method to the `GazeData` class that accepts these functions as arguments.
* A sequence-like class that groups multiple `GazeData` objects as trials in an experiment.
  * Functions for reading the various text eyetracking data formats into such objects.
    * Base these on the example data files in *tests/data*.
