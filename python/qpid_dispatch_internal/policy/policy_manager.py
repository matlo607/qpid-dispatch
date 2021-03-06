#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License
#

"""

"""

import json
import traceback
from policy_local import PolicyLocal
from ..dispatch import LogAdapter, LOG_INFO, LOG_TRACE, LOG_DEBUG, LOG_ERROR, LOG_WARNING



"""
Entity implementing the glue between the policy engine and the rest of the system.
"""

class PolicyManager(object):
    """

    """

    def __init__(self, agent):
        """
        """
        self._agent = agent
        self._policy_local = PolicyLocal(self)
        self.log_adapter = LogAdapter("POLICY")

    def log(self, level, text):
        info = traceback.extract_stack(limit=2)[0] # Caller frame info
        self.log_adapter.log(level, text, info[0], info[1])

    def _log(self, level, text):
        info = traceback.extract_stack(limit=3)[0] # Caller's caller frame info
        self.log_adapter.log(level, text, info[0], info[1])

    def log_debug(self, text):
        self._log(LOG_DEBUG, text)

    def log_info(self, text):
        self._log(LOG_INFO, text)

    def log_trace(self, text):
        self._log(LOG_TRACE, text)

    def log_error(self, text):
        self._log(LOG_ERROR, text)

    def log_warning(self, text):
        self._log(LOG_WARNING, text)

    def get_agent(self):
        return self._agent

    #
    # Management interface to create a ruleset
    #
    def create_ruleset(self, attributes):
        """
        Create named policy ruleset
        @param[in] attributes: from config
        """
        self._policy_local.create_ruleset(attributes)

    #
    # Management interface to delete a ruleset
    #
    def delete_ruleset(self, id):
        """
        Delete named policy ruleset
        @param[in] id: ruleset name
        """
        self._policy_local.policy_delete(id)

    #
    # Management interface to update a ruleset
    #
    def update_ruleset(self, attributes):
        """
        Update named policy ruleset
        @param[in] id: ruleset name
        """
        self._policy_local.create_ruleset(attributes)

    #
    # Management interface to set the default vhost
    #
    def set_default_vhost(self, name):
        """
        Set default application
        @param name:
        @return:
        """
        self._policy_local.set_default_vhost(name)

    #
    # Runtime query interface
    #
    def lookup_user(self, user, rhost, vhost, conn_name, conn_id):
        """
        Lookup function called from C.
        Determine if a user on host accessing app through AMQP Open is allowed
        according to the policy access rules.
        If allowed then return the policy settings name
        @param[in] user connection authId
        @param[in] rhost connection remote host numeric IP address as string
        @param[in] vhost application user is accessing
        @param[in] conn_name connection name for accounting purposes
        @param[in] conn_id internal connection id
        @return settings user-group name if allowed; "" if not allowed
        """
        return self._policy_local.lookup_user(user, rhost, vhost, conn_name, conn_id)

    def lookup_settings(self, vhost, name, upolicy):
        """
        Given a settings name, return the aggregated policy blob.
        @param[in] vhost: vhost user is accessing
        @param[in] name: user group name
        @param[out] upolicy: map that receives the settings
        @return settings were retrieved or not
        """
        return self._policy_local.lookup_settings(vhost, name, upolicy)

    def close_connection(self, conn_id):
        """
        The connection identifed is closing. Remove it from the connection
        accounting tables.
        @param facts:
        @return: none
        """
        self._policy_local.close_connection(conn_id)
#
#
#
def policy_lookup_user(mgr, user, rhost, vhost, conn_name, conn_id):
    """
    Look up a user in the policy database
    Called by C code
    @param mgr:
    @param user:
    @param rhost:
    @param vhost:
    @param conn_name:
    @return:
    """
    return mgr.lookup_user(user, rhost, vhost, conn_name, conn_id)

#
#
#
def policy_close_connection(mgr, conn_id):
    """
    Close the connection.
    Called by C code
    @param mgr:
    @param conn_id:
    @return:
    """
    mgr.close_connection(conn_id)

#
#
#
def policy_lookup_settings(mgr, vhost, name, upolicy):
    """
    Return settings for <vhost, usergroup> in upolicy map
    @param mgr:
    @param vhost:
    @param name:
    @param upolicy:
    @return:
    """
    return mgr.lookup_settings(vhost, name, upolicy)
