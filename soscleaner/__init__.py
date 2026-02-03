# SOSCleaner - Sensitive data obfuscation tool
# Copyright (C) 2013  Jamie Duncan (jduncan@redhat.com)
# License: GPLv2+

"""
SOSCleaner - Obfuscate sensitive data in sosreports and data files.

This package provides tools to consistently obfuscate sensitive information
(IPs, hostnames, MACs, usernames, keywords) in large datasets like Red Hat
sosreports while maintaining data relationships for debugging purposes.
"""

from soscleaner.soscleaner import SOSCleaner

__version__ = '0.5.0'
__author__ = 'Jamie Duncan'
__email__ = 'jduncan@redhat.com'
__all__ = ['SOSCleaner', '__version__']
