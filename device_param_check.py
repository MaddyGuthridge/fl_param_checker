# name=Param Checker
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=288108&p=1771223
"""
# FL Plugin Param Checker Device

A simple device that uses the param checker library.

Refer to README.md for usage.

This code is free and open source under the MIT license. Refer to the LICENSE
file for details.

(c) 2022 Miguel Guthridge
"""

__all__ = [
    'pluginParamCheck',
]

from params import idleCallback, pluginParamCheck


def OnIdle():
    idleCallback()


print()
print("To use the Param Checker device, call ")
print("pluginParamCheck(index) or")
print("pluginParamCheck(index, slot_index)")
print()
