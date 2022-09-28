"""
# FL Plugin Param Checker

Provides a simple interface for finding the indexes of plugin parameters.

Refer to README.md for usage.

This code is free and open source under the MIT license. Refer to the LICENSE
file for details.
"""

import plugins


# Target plugin
target: 'tuple[int, ...] | None' = None

# Param dictionary to store previous values in
params: dict[int, float] = {}

# Tick number to improve performance
tick = 0
TICK_FREQUENCY = 10


def pluginParamCheck(index: int, slot_index: 'int | None'):
    """
    Start a check for parameter indexes on the given plugin
    """
    global target
    t = (index,) if slot_index is None else (index, slot_index)
    # Check that the plugin actually exists
    if not plugins.isValid(*t):
        print("[FL Param Checker]")
        print(f"Can't check for parameter changes on plugin at index `{t}`")
        print("")
        print("Please check that the a plugin exists at this index, and")
        print("remember that FL Studio requires group indexes on the channel")
        print("rack.")
        return

    # Otherwise, let's track that plugin
    target = t


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
    print("Found tweaked parameters")
    for i in changed_indexes:
        name = plugins.getParamName(i, *target)
        print(f"{i:4}: {name}")

    params.clear()
    target = None
