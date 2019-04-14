#
# ----------------------------------------------------------------------------------------------------
#
# Copyright (c) 2015, Oracle and/or its affiliates. All rights reserved.
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

import sys, inspect, re, bisect
from collections import OrderedDict
from os.path import join
import mx

class MxCompatibility500(object):
    @staticmethod
    def version():
        return mx.VersionSpec("5.0.0")

    def supportsLicenses(self):
        return False

    def licenseAttribute(self):
        return 'licence'

    def licensesAttribute(self):
        return 'licences'

    def defaultLicenseAttribute(self):
        return 'defaultLicence'

    def supportedMavenMetadata(self):
        return []

    def supportsRepositories(self):
        return False

    def newestInputIsTimeStampFile(self):
        '''
        Determines if the 'newestInput' parameter of BuildTask.needsBuild()
        is a TimeStampFile or a simple time stamp (i.e. a float).
        '''
        return False

    def getSuiteOutputRoot(self, suite):
        return suite.dir

    def mavenDeployJavadoc(self):
        return False

    def mavenSupportsClassifier(self):
        return False

    def checkstyleVersion(self):
        return '6.0'

    def checkDependencyJavaCompliance(self):
        """
        Determines if a project must have a higher or equal Java compliance level
        than a project it depends upon.
        """
        return False

    def improvedImportMatching(self):
        return False

    def verifySincePresent(self):
        return []

    def moduleDepsEqualDistDeps(self):
        """
        Determines if the constituents of a module derived from a distribution are
        exactly the same as the constituents of the distribution.
        """
        return False

    def useDistsForUnittest(self):
        """
        Determines if Unittest uses jars from distributions for testing.
        """
        return False

    def excludeDisableJavaDebuggging(self):
        """
        Excludes the misspelled class name.
        """
        return False

    def makePylintVCInputsAbsolute(self):
        """
        Makes pylint input paths discovered by VC absolute.
        """
        return False

    def disableImportOfTestProjects(self):
        """
        Requires that test projects can only be imported by test projects.
        """
        return False

    def useJobsForMakeByDefault(self):
        """
        Uses -j for make by default, can be prevented using `single_job` attribute on the project.
        """
        return False

    def overwriteProjectAttributes(self):
        """
        Attributes from the configuration that are not explicitly handled overwrite values set by the constructor.
        """
        return True

    def requireJsonifiableSuite(self):
        return False

    def supportSuiteImportGitBref(self):
        return True

    def enforceTestDistributions(self):
        return False

    def deprecateIsTestProject(self):
        return False

    def filterFindbugsProjectsByJavaCompliance(self):
        """
        Should selection of projects to analyze with FindBugs filter
        out projects whose Java compliance is greater than 8.
        """
        return False

    def addVersionSuffixToExplicitVersion(self):
        return False

    def __str__(self):
        return str("MxCompatibility({})".format(self.version()))

    def __repr__(self):
        return str(self)

    def jarsUseJDKDiscriminant(self):
        """
        Should `mx.JARDistribution` use the jdk version used for the build as a `Dependency._extra_artifact_discriminant`
        to avoid collisions of build artifacts when building with different JAVA_HOME/EXTRA_JAVA_HOMES settings.
        """
        return False

    def check_package_locations(self):
        """
        Should `canonicalizeprojects` check whether the java package declarations and source location match.
        """
        return False

    def check_checkstyle_config(self):
        """
        Should sanity check Checkstyle configuration for a project.
        """
        return False

    def verify_multirelease_projects(self):
        """
        Should multi-release projects be verified (see mx.verifyMultiReleaseProjects).
        """
        return False

    def spotbugs_version(self):
        """
        Which version of findbugs/spotbugs should be used?
        """
        return "3.0.0"

class MxCompatibility520(MxCompatibility500):
    @staticmethod
    def version():
        return mx.VersionSpec("5.2.0")

    def supportsLicenses(self):
        return True

    def supportedMavenMetadata(self):
        return ['library-coordinates', 'suite-url', 'suite-developer', 'dist-description']

class MxCompatibility521(MxCompatibility520):
    @staticmethod
    def version():
        return mx.VersionSpec("5.2.1")

    def supportsRepositories(self):
        return True

class MxCompatibility522(MxCompatibility521):
    @staticmethod
    def version():
        return mx.VersionSpec("5.2.2")

    def licenseAttribute(self):
        return 'license'

    def licensesAttribute(self):
        return 'licenses'

    def defaultLicenseAttribute(self):
        return 'defaultLicense'

class MxCompatibility533(MxCompatibility522):
    @staticmethod
    def version():
        return mx.VersionSpec("5.3.3")

    def newestInputIsTimeStampFile(self):
        return True

class MxCompatibility555(MxCompatibility533):
    @staticmethod
    def version():
        return mx.VersionSpec("5.5.5")

    def getSuiteOutputRoot(self, suite):
        return join(suite.dir, 'mxbuild')

class MxCompatibility566(MxCompatibility555):
    @staticmethod
    def version():
        return mx.VersionSpec("5.6.6")

    def mavenDeployJavadoc(self):
        return True

class MxCompatibility5616(MxCompatibility566):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.6.16")

    def checkstyleVersion(self):
        return '6.15'

class MxCompatibility59(MxCompatibility5616):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.9.0")

    def verifySincePresent(self):
        return ['-verifysincepresent']

class MxCompatibility5200(MxCompatibility59):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.20.0")

    def checkDependencyJavaCompliance(self):
        return True

    def improvedImportMatching(self):
        return True

class MxCompatibility5344(MxCompatibility5200):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.34.4")

    def moduleDepsEqualDistDeps(self):
        return True

class MxCompatibility5590(MxCompatibility5344):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.59.0")

    def useDistsForUnittest(self):
        return True

class MxCompatibility5680(MxCompatibility5590):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.68.0")

    def excludeDisableJavaDebuggging(self):
        return True

class MxCompatibility51104(MxCompatibility5680):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.110.4")

    def makePylintVCInputsAbsolute(self):
        return True

class MxCompatibility51120(MxCompatibility51104):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.113.0")

    def disableImportOfTestProjects(self):
        return True


class MxCompatibility51150(MxCompatibility51120):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.115.0")

    def useJobsForMakeByDefault(self):
        return True


class MxCompatibility51247(MxCompatibility51150):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.124.7")

    def overwriteProjectAttributes(self):
        return False

class MxCompatibility51330(MxCompatibility51247):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.133.0")

    def requireJsonifiableSuite(self):
        return True

class MxCompatibility51380(MxCompatibility51330):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.138.0")

    def supportSuiteImportGitBref(self):
        return False

class MxCompatibility51400(MxCompatibility51380):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.140.0")

    def enforceTestDistributions(self):
        return True

    def deprecateIsTestProject(self):
        return True

class MxCompatibility51492(MxCompatibility51400):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.149.2")

    def filterFindbugsProjectsByJavaCompliance(self):
        return True

class MxCompatibility51760(MxCompatibility51492):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.176.0")

    def addVersionSuffixToExplicitVersion(self):
        return True

class MxCompatibility5181(MxCompatibility51760):#pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.181.0")

    def jarsUseJDKDiscriminant(self):
        return True

class MxCompatibility5194(MxCompatibility5181):  # pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.194.0")

    def check_package_locations(self):
        return True

class MxCompatibility51950(MxCompatibility5194):  # pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.195.0")

    def mavenSupportsClassifier(self):
        return True

class MxCompatibility51951(MxCompatibility51950):  # pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.195.1")

    def check_checkstyle_config(self):
        return True

class MxCompatibility52061(MxCompatibility51951):  # pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.206.1")

    def verify_multirelease_projects(self):
        return True

class MxCompatibility52102(MxCompatibility52061):  # pylint: disable=too-many-ancestors
    @staticmethod
    def version():
        return mx.VersionSpec("5.210.2")

    def spotbugs_version(self):
        return "3.1.11"

def minVersion():
    _ensureCompatLoaded()
    return list(_versionsMap)[0]

def getMxCompatibility(version):
    """:rtype: MxCompatibility500"""
    if version < minVersion():  # ensures compat loaded
        return None
    keys = list(_versionsMap.keys())
    return _versionsMap[keys[bisect.bisect_right(keys, version)-1]]

_versionsMap = OrderedDict()

def _ensureCompatLoaded():
    if not _versionsMap:

        def flattenClassTree(tree):
            root = tree[0][0]
            assert isinstance(root, type), root
            yield root
            if len(tree) > 1:
                assert len(tree) == 2
                rest = tree[1]
                assert isinstance(rest, list), rest
                for c in flattenClassTree(rest):
                    yield c

        classes = []
        regex = re.compile(r'^MxCompatibility[0-9a-z]*$')
        for name, clazz in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            m = regex.match(name)
            if m:
                classes.append(clazz)

        previousVersion = None
        for clazz in flattenClassTree(inspect.getclasstree(classes)):
            if clazz == object:
                continue
            assert previousVersion is None or previousVersion < clazz.version()
            previousVersion = clazz.version()
            _versionsMap[previousVersion] = clazz()
