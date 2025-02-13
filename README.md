psychopy_tobii_controller_plugins
====================================

psychopy_tobii_controller is a helper module to use tobii_research package with PsychoPy.

Disclaimer: psychopy_tobii_controller is unofficial. It is NOT affiliated with Tobii.


## Licence

GPLv3 (https://github.com/hsogo/psychopy_tobii_controller_plugins/blob/master/LICENCE)

## Author

Hiroyuki Sogo (https://github.com/hsogo)

## Requirements

PsychoPy (http://www.psychopy.org/)
tobii_research (https://pypi.python.org/pypi/tobii-research)
psychopy_tobii_controller (https://github.com/hsogo/psychopy_tobii_controller/)

## Samples

Basic usage of Builder components of tobii_controller is demonstrated in these samples.

- ptc_init: Initialize tobii_controller. This component works in any routine.
- ptc_cal: Run calibration. Calibration is performed at the beginning of the routine where this component is placed.  More preceisely, this component is equivalent to add calibration codes to "begin routine" of the Code component.
- ptc_rec: Record gaze data in the routine where this component is placed.
- ptc_message: Insert event during recording. ptc_rec component should be placed in the same routine.
- ptc_getpos: Get the latest gaze position. Gaze position is stored in a variable with the same name as the 'Name' property of this component.  ptc_rec component should be placed in the same routine.

### builder_sample01.psyexp (for 1.2.0 or earlier)

This sample is for version 1.2.0 or earlier of psychopy_tobii_controller.

In these versions, Builder components are in **ptc_components** directory.
Copy this directory anywhere you have write permissions and add this directory to *component foloders* of PsychoPy Preferences.
For example, if you copy ptc_components directory to 'C:/Users/foo/Documents', add 'C:/Users/foo/Documents/ptc_components' to *components folder* and restart PsychoPy.  *components folder* is in 'Builder' tab of PsychoPy Preference dialog.

### builder_sample02.psyexp (for 1.3.0 or later)

This sample is for version 1.3.0 or later of psychopy_tobii_controller.

From version 1.3.0, Builder components are installed as plugins.  Adding 'psychopy-tobii-controller' to 'startup plugins' of the PsychoPy Preference Panel, the components appear in the Components pane.


