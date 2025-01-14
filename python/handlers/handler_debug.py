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

"""Example of a debug request handler that wraps the default request handler
   and prints debugging information to stdout."""

import os
import sys
from pprint import pprint
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import splunklib.binding as binding
import splunklib.client as client
import python.utils as utils


def handler():
    default = binding.handler()

    def request(url, message, **kwargs):
        response = default(url, message, **kwargs)
        print("%s %s => %d (%s)" % (
            message['method'], url, response['status'], response['reason']))
        return response

    return request


opts = utils.parse(sys.argv[1:], {}, ".env")
service = client.connect(handler=handler(), **opts.kwargs)
pprint([app.name for app in service.apps])
