"""
# FL Plugin Param Checker

Provides a simple interface for finding the indexes of plugin parameters.

Refer to README.md for usage.

This code is free and open source under the MIT license. Refer to the LICENSE
file for details.

(c) 2022 Miguel Guthridge
"""

import plugins


# Target plugin
target: 'tuple[int] | tuple[int, int] | None' = None

# Whether to keep listening, even when we find a plugin
daemon = False

# Param dictionary to store previous values in
params: dict[int, float] = {}

# Tick number to improve performance
tick = 0
TICK_FREQUENCY = 10


def startListening(t: "tuple[int] | tuple[int, int]", keep_alive: bool):
    """
    Start listening for parameter tweaks
    """
    global target, daemon
    target = t
    daemon = keep_alive

    name = plugins.getPluginName(*target)
    # Get the user's name of the plugin
    if len(t) == 1:
        user_name = plugins.getPluginName(t[0], -1, True)
    else:
        track, slot = t  # type: ignore
        user_name = plugins.getPluginName(track, slot, True)
    # If the user's name is the same, don't show it, otherwise, format it
    # nicely
    if name == user_name:
        user_name = ""
    else:
        user_name = f" ('{user_name}')"
    print(f"Listening for parameter tweaks on '{name}'{user_name}...")
    if keep_alive:
        print("Listening indefinitely. Call pluginParamCheck() with no args to"
              " stop")
    print()


def stopListening():
    """
    Stop listening for parameter tweaks
    """
    global target
    target = None
    params.clear()
    print("Stopped listening for parameter tweaks")
    print()


def pluginParamCheck(
    index: "int | None" = None,
    slot_index: "int | None" = None,
    keep_alive: bool = False,
):
    """
    Start a check for parameter indexes on the given plugin
    """
    global target, daemon
    print("[FL Param Checker]")
    # If we're given no args, disable listening if possible
    if index is None:
        if target is not None:
            stopListening()
            return ""
        else:
            print("To start listening for parameter tweaks, call ")
            print("pluginParamCheck() with the index of the plugin as the")
            print("args. For example:")
            print("    pluginParamCheck(0)  # start listening to channel 1 on "
                  "the channel rack")
            print("    pluginParamCheck(1, 5)  # start listening slot 4 of "
                  "track 1 on the mixer")
            print("To listen for changes indefinitely, use the flag "
                  "keep_alive=True in your call, for example:")
            print("    pluginParamCheck(0, keep_alive=True")
            return ""

    # Otherwise, start listening
    t: 'tuple[int] | tuple[int, int]' = (
        (index,)
        if slot_index is None
        else (index, slot_index)
    )
    # Check that the plugin actually exists
    if not plugins.isValid(*t):
        print(f"Can't check for parameter changes on plugin at index `{t}`")
        print()
        print("Please check that the a plugin exists at this index, and")
        print("remember that FL Studio requires group indexes on the channel")
        print("rack.")
        print()
        return ""

    # If we've already got a target, stop listening to that
    if target is not None:
        stopListening()

    # Start listening to the new target
    startListening(t, keep_alive)
    return ""


def idleCallback():
    """
    Call this function while the script is idle. When checking for parameters
    is active, it will check for changes in parameters.
    """
    global tick, target
    # Do nothing if we're not checking for changes
    if target is None:
        return

    tick += 1

    # Only check for parameter updates every few ticks, as it is a costly
    # operation
    if tick % TICK_FREQUENCY:
        return

    changed_indexes: list[int] = []

    # Check each param for changes
    for i in range(plugins.getParamCount(*target)):
        val = plugins.getParamValue(i, *target)
        # If the value is present and has changed
        if params.get(i, val) != val:
            changed_indexes.append(i)
        params[i] = val

    if not len(changed_indexes):
        return

    print("[FL Param Checker]")
    print(f"Found tweaked parameter{'s' if len(changed_indexes) != 1 else ''}")
    for i in changed_indexes:
        name = plugins.getParamName(i, *target)
        print(f"{i:4}: {name}")

    print()
    if not daemon:
        stopListening()
