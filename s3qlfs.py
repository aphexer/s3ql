#!/usr/bin/env python
#
#    Copyright (C) 2008  Nikolaus Rath <Nikolaus@rath.org>
#
#    This program can be distributed under the terms of the GNU LGPL.
#

from optparse import OptionParser
from getpass  import getpass
import s3ql

#
# Parse command line
#
parser = OptionParser(
    usage="%prog  [options] <bucketname> <mountpoint>\n"
          "       %prog --help",
    description="Mounts an amazon S3 bucket as a filesystem")

parser.add_option("--awskey", type="string",
                  help="Amazon Webservices access key to use")
parser.add_option("--debug", action="store_true", default=False,
                  help="Generate debugging output")
parser.add_option("--s3timeout", type="int", default=50,
                  help="Maximum time to wait for propagation in S3 (default: %default)")
parser.add_option("--allow_others", action="store_true", default=False,
                  help="Allow others users to access the filesystem")
parser.add_option("--allow_root", action="store_true", default=False,
                  help="Allow root to access the filesystem")

(options, pps) = parser.parse_args()


#
# Verify parameters
#
if not len(pps) == 2:
    parser.error("Wrong number of parameters")

#
# Read password
#
if options.awskey:
    if sys.stdin.isatty():
        pw = getpass("Enter AWS password: ")
    else:
        pw = sys.stdin.readline().rstrip()
else:
    pw = None

#
# Pass on fuse options
#
fuse_opts = []
if options.allow_others:
    fuse_opts.append("allow_others")
if options.allow_root:
    fuse_opts.append("allow_root")

#
# Activate logging
#
if options.debug:
    debug_enabled = True
else:
    debug_enabled = False


#
# Start server
#
server = s3ql.fs(awskey=options.awskey,
                 bucketname=pps[0],
                 awspass=pw,
                 fuse_options=fuse_opts,
                 mountpoint=pps[1])
server.main()
