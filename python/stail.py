#!/usr/bin/env python
#
# Copyright 2011-2015 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Tails a realtime search using the export endpoint and prints results to
   stdout."""

import sys

from pprint import pprint

from splunklib.client import connect
from splunklib.results import JSONResultsReader

import utils


def main():
    usage = "usage: %prog <search>"
    opts = utils.parse(sys.argv[1:], {}, ".env", usage=usage)

    if len(opts.args) != 1:
        utils.error("Search expression required", 2)
    search = opts.args[0]

    service = connect(**opts.kwargs)

    try:
        result = service.get(
            "search/jobs/export",
            search=search,
            earliest_time="rt",
            latest_time="rt",
            search_mode="realtime",
            output_mode="json")
        print(result.body)

        for result in JSONResultsReader(result.body):
            if result is not None:
                print(pprint(result))

    except KeyboardInterrupt:
        print("\nInterrupted.")


if __name__ == "__main__":
    main()
