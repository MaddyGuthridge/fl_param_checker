"""
# FL Plugin Param Checker Module

Allows the fl_param_checker library to be used within other devices.

Refer to README.md for usage.

This code is free and open source under the MIT license. Refer to the LICENSE
file for details.

(c) 2022 Maddy Guthridge
"""
__all__ = [
    'idleCallback',
    'pluginParamCheck',
]

from .params import idleCallback, pluginParamCheck
