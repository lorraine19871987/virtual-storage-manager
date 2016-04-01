#  Copyright 2014 Intel Corporation, All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
BenchmarkCase interface (1.1 extension).
"""

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import six
from vsmclient import base

class BenchmarkCase(base.Resource):
    """"""
    def __repr__(self):
        return "<BENCHMARKCASE: %s>" % self.id

    def delete(self):
        """"""
        self.manager.delete(self)


class BenchmarkCaseManager(base.ManagerWithFind):
    """
    Manage :class:`BENCHMARKCASE` resources.
    """
    resource_class = BenchmarkCase

    def get(self, case_id):
        """
        Get a benchmark_case.

        :param case_id: The ID of the benchmark_case.
        :rtype: :class:`BENCHMARKCASE`
        """
        return self._get("/benchmark_cases/%s" % case_id, "benchmark_case")

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all benchmark_cases.

        :rtype: list of :class:`BENCHMARKCASE`
        """
        if search_opts is None:
            search_opts = {}

        qparams = {}

        for opt, val in six.iteritems(search_opts):
            if val:
                qparams[opt] = val

        # Transform the dict to a sequence of two-element tuples in fixed
        # order, then the encoded string will be consistent in Python 2&3.
        if qparams:
            new_qparams = sorted(qparams.items(), key=lambda x: x[0])
            query_string = "?%s" % urlencode(new_qparams)
        else:
            query_string = ""

        detail = ""
        if detailed:
            detail = "/detail"

        return self._list("/benchmark_cases%s%s" % (detail, query_string),
                          "benchmark_cases")

    def create(self, name, readwrite, blocksize, iodepth, runtime, ioengine,
               clientname, additional_options):
        """
        Create a new benchmark case.

        :param name:
        :param readwrite:
        :param blocksize:
        :param iodepth:
        :param runtime:
        :param ioengine:
        :param clientname:
        :param additional_options:
        :return:
        """

        body = {'benchmark_case':
                    {'name': name,
                     'readwrite': readwrite,
                     'blocksize': blocksize,
                     'iodepth': iodepth,
                     'runtime': runtime,
                     'ioengine': ioengine,
                     'clientname': clientname,
                     'additional_options': additional_options,
                     }}

        return self._create('/benchmark_cases', body, 'benchmark_case')

    def delete(self, benchmark_case):
        self._delete("/benchmark_cases/%s" % base.getid(benchmark_case))

    def run_case(self, case_id, body):
        self.api.client.post("/benchmark_cases/%s/runcase" % case_id, body=body)

    def termintate(self, case_id):
        self.api.client.post("/benchmark_cases/%s/terminate" % case_id)
