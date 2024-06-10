# fl_param_checker

A tool to help find plugin parameter indexes to assist with MIDI Controller Script development.

## Installation

To install this as a standalone script, use the following instructions.

1. Download and copy this entire project
   to your `Image-Line/FL Studio/Settings/Hardware` folder.

2. Restart FL Studio, then in the MIDI settings, assign a free MIDI device to
   the "Param Checker" device. Ensure that the device has an input and output
   port assigned.

## Integrating with your own device

To include this code within your own script, use the following instructions.

1. If you're using Git, add this as a git submodule.
   `$ git submodule add git@github.com:MaddyGuthridge/fl_param_checker.git [output folder]/fl_param_checker`

   Otherwise, copy this entire folder into your code (make sure to include the
   LICENSE file).

2. Ensure that the module's `idleCallback()` function is called during your
   script's `OnIdle` code somewhere.

3. Optionally, import the `pluginParamCheck()` function to your main
   `device_*.py` file so that it can be easily called from FL Studio's script
   output window.

## Usage

1. Open the script output window, and call the `pluginParamCheck()` function
   with the index of the plugin you wish to inspect. For example, to inspect
   the first generator on the channel rack, call `pluginParamCheck(0)`, or to
   inspect the first slot of the first (non-master) mixer track, call
   `pluginParamCheck(1, 0)`.

2. Tweak the plugin parameter you wish to find the info on.

3. The parameter index will be printed. If multiple values change (eg if the
   plugin links more than one parameter together), all of them will be printed.

4. Repeat as necessary.

It is also possible to listen for parameter tweaks infinitely, by specifying
the `keep_alive` parameter as `True`. If the checker is listening indefinitely,
it can be stopped by calling `pluginParamCheck()` with no arguments.

## Known Issues

Closing FL Studio or reloading the script while it is listening for parameter
tweaks will cause FL Studio to freeze. It eventually does start responding
again, but only after a minute or so depending on how long you've been
listening for changes for.
