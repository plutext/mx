#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
#
# Copyright (c) 2018, 2018, Oracle and/or its affiliates. All rights reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# This code is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 only, as
# published by the Free Software Foundation.
#
# This code is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# version 2 for more details (a copy is included in the LICENSE file that
# accompanied this code).
#
# You should have received a copy of the GNU General Public License version
# 2 along with this work; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Please contact Oracle, 500 Oracle Parkway, Redwood Shores, CA 94065 USA
# or visit www.oracle.com if you need additional information or have any
# questions.
#
# ----------------------------------------------------------------------------------------------------

from __future__ import print_function

import os, tempfile
from argparse import ArgumentParser, REMAINDER
from os.path import exists, expanduser, join, isdir, isfile, realpath, dirname, abspath

# Temporary imports and (re)definitions while porting mx from Python 2 to Python 3
import sys
if sys.version_info[0] < 3:
    def input(prompt=None):                    # pylint: disable=redefined-builtin
        return raw_input(prompt)               # pylint: disable=undefined-variable
    from StringIO import StringIO
else:
    from io import StringIO

def is_valid_jdk(jdk):
    """
    Determines if `jdk` looks like a valid JDK directory.

    :return: True if there's a ``java`` executable in ``jdk/bin``
    """
    java_exe = join(jdk, 'bin', 'java')
    if not exists(java_exe):
        java_exe += '.exe'
    return isfile(java_exe) and os.access(java_exe, os.X_OK)

def find_system_jdks():
    """
    Returns a set of valid JDK directories by searching standard locations.
    """
    bases = [
        '/Library/Java/JavaVirtualMachines',
        '/usr/lib/jvm',
        '/usr/java',
        '/usr/jdk/instances',
        r'C:\Program Files\Java'
    ]
    jdks = set()
    for base in bases:
        if isdir(base):
            for n in os.listdir(base):
                jdk = join(base, n)
                mac_jdk = join(jdk, 'Contents', 'Home')
                if isdir(mac_jdk):
                    jdk = mac_jdk
                if is_valid_jdk(jdk):
                    jdks.add(realpath(jdk))
    return jdks

def get_suite_env_file(suite_dir=None):
    for n in os.listdir(suite_dir or '.'):
        if n.startswith('mx.'):
            suite_py = join('.', n, 'suite.py')
            if exists(suite_py):
                return abspath(join(suite_dir or '.', n, 'env'))
    return None

def get_setvar_format(shell):
    if shell == 'csh':
        return 'setenv %s %s'
    if shell == 'fish':
        return 'set -x %s %s'
    return 'export %s=%s'

def get_PATH_sep(shell):
    if shell == 'fish':
        return ' '
    return os.pathsep

def get_shell_commands(args, jdk, extra_jdks):
    setvar_format = get_setvar_format(args.shell)
    shell_commands = StringIO()
    print(setvar_format % ('JAVA_HOME', jdk), file=shell_commands)
    if extra_jdks:
        print(setvar_format % ('EXTRA_JAVA_HOMES', os.pathsep.join(extra_jdks)), file=shell_commands)
    path = os.environ.get('PATH').split(os.pathsep)
    if path:
        jdk_bin = join(jdk, 'bin')
        old_java_home = os.environ.get('JAVA_HOME')
        replace = join(old_java_home, 'bin') if old_java_home else None
        if replace in path:
            path = [e if e != replace else jdk_bin for e in path]
        else:
            path.append(jdk_bin)
        print(setvar_format % ('PATH', get_PATH_sep(args.shell).join(path)), file=shell_commands)
    return shell_commands.getvalue().strip()

def apply_selection(args, jdk, extra_jdks):
    print('JAVA_HOME=' + jdk)
    if extra_jdks:
        print('EXTRA_JAVA_HOMES=' + os.pathsep.join(extra_jdks))

    if args.shell_file:
        with open(args.shell_file, 'w') as fp:
            print(get_shell_commands(args, jdk, extra_jdks), file=fp)
    else:
        env = get_suite_env_file(args.suite_path)
        if env:
            with open(env, 'a') as fp:
                print('JAVA_HOME=' + jdk, file=fp)
                if extra_jdks:
                    print('EXTRA_JAVA_HOMES=' + os.pathsep.join(extra_jdks), file=fp)
            print('Updated', env)
        else:
            print()
            print('To apply the above environment variable settings, eval the following in your shell:')
            print()
            print(get_shell_commands(args, jdk, extra_jdks))

if __name__ == '__main__':
    parser = ArgumentParser(prog='select_jdk', usage='%(prog)s [options] [<primary jdk> [<secondary jdk>...]]' + """
        Selects values for the JAVA_HOME, EXTRA_JAVA_HOMES and PATH environment variables based on
        the explicitly supplied JDKs or on system JDKs plus previously selected JDKs (cached in ~/.mx/jdk_cache).

        If the -s/--shell-source option is given, settings appropriate for the current shell are written to
        the given file such that it can be eval'ed in the shell to apply the settings. For example, in ~/.config/fish/config.fish:

            if test -x (dirname (which mx))/select_jdk.py
                function select_jdk
                    set tmp_file (mktemp)
                    eval (dirname (which mx))/select_jdk.py -s $tmp_file $argv
                    source $tmp_file
                    rm $tmp_file
                end
            end

        or in ~/.bashrc:

            if [ -x $(dirname $(which mx))/select_jdk.py ]; then
                function select_jdk {
                    TMP_FILE=select_jdk.$$
                    eval $(dirname $(which mx))/select_jdk.py -s $TMP_FILE "$@"
                    source $TMP_FILE
                    rm $TMP_FILE
                }
            fi

        In the absence of -s, if the current directory looks like a suite, the mx.<suite>/env file is
        created/updated with the selected values for JAVA_HOME and EXTRA_JAVA_HOMES.

        Otherwise, the settings are printed such that they can applied manually.
    """)

    shell_or_env = parser.add_mutually_exclusive_group()
    shell_or_env.add_argument('-s', '--shell-file', action='store', help='write shell commands for setting env vars to <path>', metavar='<path>')
    shell_or_env.add_argument('-p', '--suite-path', help='directory of suite whose env file is to be updated', metavar='<path>')
    parser.add_argument('--shell', action='store', help='shell syntax to use for commands', metavar='<format>', choices=['sh', 'fish', 'csh'])
    parser.add_argument('jdks', nargs=REMAINDER, metavar='<primary jdk> [<secondary jdk>...]')

    args = parser.parse_args()

    if args.shell is None:
        shell = os.environ.get('SHELL')
        if shell.endswith('fish'):
            args.shell = 'fish'
        elif shell.endswith('csh'):
            args.shell = 'csh'
        else:
            args.shell = 'sh'

    jdk_cache_path = join(expanduser('~'), '.mx', 'jdk_cache')
    if len(args.jdks) != 0:
        invalid_jdks = [a for a in args.jdks if not is_valid_jdk(a)]
        if invalid_jdks:
            raise SystemExit('Following JDKs appear to be invalid (java executable not found):\n' + '\n'.join(invalid_jdks))
        with open(jdk_cache_path, 'a') as fp:
            for jdk in args.jdks:
                print(jdk, file=fp)
        apply_selection(args, args.jdks[0], args.jdks[1:])
    else:
        jdks = find_system_jdks()
        if exists(jdk_cache_path):
            with open(jdk_cache_path) as fp:
                jdks.update((line.strip() for line in fp.readlines() if is_valid_jdk(line.strip())))

        sorted_jdks = sorted(jdks)
        print("Current JDK Settings:")
        for name in ['JAVA_HOME', 'EXTRA_JAVA_HOMES']:
            jdk = os.environ.get(name, None)
            if jdk:
                if jdk in sorted_jdks:
                    jdk = '{} [{}]'.format(jdk, sorted_jdks.index(jdk))
                print('{}={}'.format(name, jdk))
        choices = list(enumerate(sorted_jdks))
        if choices:
            _, tmp_cache_path = tempfile.mkstemp(dir=dirname(jdk_cache_path))
            with open(tmp_cache_path, 'w') as fp:
                for index, jdk in choices:
                    print('[{}] {}'.format(index, jdk))
                    print(jdk, file=fp)

            os.rename(tmp_cache_path, jdk_cache_path)
            choices = {str(index):jdk for index, jdk in choices}
            jdks = [choices[n] for n in input('Select JDK(s) (separate multiple choices by whitespace)> ').split() if n in choices]
            if jdks:
                apply_selection(args, jdks[0], jdks[1:])
