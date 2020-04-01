# Copyright 2015-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License").
# You may not use this file except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# Python module containing example query routing table function.
# Configure path/name to this file in [pgbouncer] section of ini file.
# Ex:
#    routing_rules_py_module_file = /etc/pgbouncer/routing_rules.py


# ROUTING TABLE
# ensure all dbkey values are defined in [database] section of the pgbouncer ini file
# Test by calling routing_rules() with sample queries, and validating dbkey values returned
routingtable = {
	'route' : [{
			'usernameRegex' : '.*',
			'queryRegex' : '.*tablea.*',
			'dbkey' : 'dev.1'
		}, {
			'usernameRegex' : '.*',
			'queryRegex' : '.*tableb.*',
			'dbkey' : 'dev.2'
		}
	],
	'default' : None
}


# ROUTING FN - CALLED FROM PGBOUNCER-RR - DO NOT CHANGE NAME
# IMPLEMENTS REGEX RULES DEFINED IN ROUTINGTABLE OBJECT
# RETURNS FIRST MATCH FOUND
#
# xact_start and query_start is two fields of pg_stat_activity
# xact_start is transaction start time, and query_start is query start time.
# They can help you to distinguish whether query in a transaction or not.
import re
def routing_rules(username, query, xact_start, query_start):
	# While xact_start is NOT equal to query_start means query in the transaction zone.
	if xact_start != query_start:
		return None
	for route in routingtable['route']:
		u = re.compile(route['usernameRegex'])
		q = re.compile(route['queryRegex'])
		if u.search(username) and q.search(query):
			return route['dbkey']
	return routingtable['default']

if __name__ == "__main__":
    print "test for tablea:" + routing_rules("master", "select * from tablea;")
    print "test for tableb:" + routing_rules("master", "select * from tableb;")



