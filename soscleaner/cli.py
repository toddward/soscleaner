#!/usr/bin/env python3
# Copyright (C) 2013  Jamie Duncan (jduncan@redhat.com)

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""SOSCleaner CLI - Command-line interface for sosreport obfuscation."""

from soscleaner.soscleaner import SOSCleaner
import argparse
import os
import sys

__version__ = '0.5.0'


def main():
    """Main entry point for the soscleaner CLI."""
    parser = argparse.ArgumentParser(
        description='SOSCleaner - Obfuscate sensitive data in sosreports',
        usage='%(prog)s [OPTIONS] /path/to/sosreport'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument("-l", "--log_level", dest="loglevel", default='INFO',
                        help="The Desired Log Level (default = INFO) Options are DEBUG, INFO, WARNING, ERROR",
                        metavar="LOGLEVEL")
    parser.add_argument("-d", "--domain", action="append", default=[], dest="domains",
                        help="additional domain to obfuscate (optional). use a flag for each additional domain",
                        metavar="DOMAIN")
    parser.add_argument("-f", "--file", action="append", default=[], dest="files",
                        help="additional files to be analyzed in addition to or in exception of sosreport",
                        metavar="FILES")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, dest='quiet',
                        help="disable output to STDOUT")
    parser.add_argument("-k", "--keyword", action="append", default=[], dest="keywords",
                        help="additional keywords to obfuscate. use multiple times for multiple keywords",
                        metavar="KEYWORD")
    parser.add_argument("-K", "--keywords_file", action="store", dest="keywords_file",
                        help="line-delimited list of keywords to obfuscate",
                        metavar="KEYWORDS_FILE")
    parser.add_argument("-H", "--hostname-path", action="store", default="hostname", dest="hostname_path",
                        help="optional path to hostname file.",
                        metavar="HOSTNAMEPATH")
    parser.add_argument("-n", "--network", action="append", default=[], dest="networks",
                        help="networks to be obfuscated (optional). by default it looks through known routes to generate a list from a sosreport",
                        metavar="NETWORK")
    parser.add_argument("-u", "--user", action="append", default=[], dest="users",
                        help="additional usernames to obfuscate in the sosreport or dataset - one user per flag",
                        metavar="USER")
    parser.add_argument("-U", "--users-file", action="store", dest="users_file",
                        help="line-delimited list of users to obfuscate",
                        metavar="USERS_FILE")
    parser.add_argument("-o", "--output-dir", action="store", default="/tmp", dest="report_dir",
                        help="Directory to store soscleaner obfuscated sosreport or dataset",
                        metavar="DIRECTORY")
    parser.add_argument("-m", "--macs", action="store_true", default=False, dest='obfuscate_macs',
                        help="enable MAC address obfuscation")
    parser.add_argument('sosreport', nargs='?', default=None,
                        help='Path to sosreport tarball or directory')

    options = parser.parse_args()
    if not options.sosreport and not options.files:  # we don't have an sosreport
        parser.print_help()
        sys.exit(1)

    cleaner = SOSCleaner(quiet=options.quiet)

    sosreport = None
    if options.sosreport:
        if os.path.isfile(options.sosreport) or os.path.isdir(options.sosreport):
            sosreport = options.sosreport
        else:
            print("ERROR: No presence of an existing file to sanitize detected")
            sys.exit(1)

    cleaner.clean_report(options, sosreport)


if __name__ == '__main__':
    main()
