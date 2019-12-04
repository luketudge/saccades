# TODOs

* Functions for extracting saccades.
  * These should take a `GazeData` object as argument and return a boolean column saying sample is/isn't a saccade.
  * A method to the `GazeData` class that accepts these functions as arguments.
* Likewise for gaze coordinate smoothing.
  * `scipy` and `pandas` have some ready-made smoothing algorithms.
  * But one difficulty is taking into account the *time* column.
* A sequence-like class that groups multiple `GazeData` objects as trials in an experiment.
  * This class should store the metadata for the experiment, such as screen dimensions, time units, etc.
  * Functions for reading the various text eyetracking data formats into such objects.
    * Base these on the example data files in *tests/data*.
