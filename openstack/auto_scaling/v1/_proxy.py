# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import proxy2
from openstack.auto_scaling.v1 import config as _config
from openstack.auto_scaling.v1 import group as _group
from openstack.auto_scaling.v1 import policy as _policy


class Proxy(proxy2.BaseProxy):
    def configs(self, **query):
        """Retrieve a generator of configs
        :param dict query: Optional query parameters to be sent to limit the
                      resources being returned.
            * ``name``: configuration name
            * ``image_id``: image id
            * ``marker``:  pagination marker
            * ``limit``: pagination limit

        :returns: A generator of config
                  (:class:`~openstack.auto_scaling.v2.config.Config`) instances
        """
        return self._list(_config.Config, paginated=True, **query)

    def create_config(self, **attrs):
        """Create a new config from attributes
        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.auto_scaling.v2.config.Config`,
                           comprised of the properties on the Config class.
        :returns: The results of config creation
        :rtype: :class:`~openstack.auto_scaling.v2.config.Config`
        """
        return self._create(_config.Config, prepend_key=False, **attrs)

    def create_config(self, name, **attrs):
        """Create a new config from config name and instance-config attributes
        :param name: auto scaling config name
        :param dict attrs: Keyword arguments which will be used to create
                a :class:`~openstack.auto_scaling.v2.config.InstanceConfig`,
                comprised of the properties on the InstanceConfig class.
        :returns: The results of config creation
        :rtype: :class:`~openstack.auto_scaling.v2.config.Config`
        """
        instance_config = _config.InstanceConfig.new(**attrs)
        config = _config.Config(name=name, instance_config=instance_config)
        return config.create(self._session, prepend_key=False)

    def get_config(self, config):
        """Get a config
        :param config: The value can be the ID of a config
             or a :class:`~openstack.auto_scaling.v2.config.Config` instance.
        :returns: Config instance
        :rtype: :class:`~openstack.auto_scaling.v2.config.Config`
        """
        return self._get(_config.Config, config)

    def delete_config(self, config, ignore_missing=True):
        """Delete a config

        :param config: The value can be the ID of a config
             or a :class:`~openstack.auto_scaling.v2.config.Config` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the config does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent config.

        :returns: Config been deleted
        :rtype: :class:`~openstack.auto_scaling.v2.config.Config`
        """
        return self._delete(_config.Config, config, ignore_missing=ignore_missing)

    def find_config(self, name_or_id, ignore_missing=True):
        """Find a single config

        :param name_or_id: The name or ID of a config
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the config does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent config.

        :returns: ``None``
        """
        return self._find(_config.Config, name_or_id,
                          ignore_missing=ignore_missing,
                          name=name_or_id)

    def groups(self, **query):
        """Retrieve a generator of groups
        :param dict query: Optional query parameters to be sent to limit the
                      resources being returned.
            * ``name``: group name
            * ``status``: group status, ``INSERVICE``, ``PAUSED``, ``ERROR``
            * ``scaling_configuration_id``: scaling configuration id
            * ``marker``:  pagination marker, known as ``start_number``
            * ``limit``: pagination limit

        :returns: A generator of group
                  (:class:`~openstack.auto_scaling.v2.group.Group`) instances
        """
        return self._list(_group.Group, paginated=True, **query)

    def create_group(self, **attrs):
        """Create a new group from attributes
        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.auto_scaling.v2.group.Group`,
                           comprised of the properties on the Group class.
        :returns: The results of group creation
        :rtype: :class:`~openstack.auto_scaling.v2.group.Group`
        """
        return self._create(_group.Group, prepend_key=False, **attrs)

    def update_group(self, group, **attrs):
        """Create a new group from attributes
        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.auto_scaling.v2.group.Group`,
                           comprised of the properties on the Group class.
        :returns: The results of group creation
        :rtype: :class:`~openstack.auto_scaling.v2.group.Group`
        """
        return self._update(_group.Group, group, prepend_key=False, **attrs)

    def get_group(self, group):
        """Get a group
        :param group: The value can be the ID of a group
             or a :class:`~openstack.auto_scaling.v2.group.Group` instance.
        :returns: Group instance
        :rtype: :class:`~openstack.auto_scaling.v2.group.Group`
        """
        return self._get(_group.Group, group)

    def delete_group(self, group, ignore_missing=True):
        """Delete a group

        :param group: The value can be the ID of a group
             or a :class:`~openstack.auto_scaling.v2.group.Group` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent group.
        """
        return self._delete(_group.Group, group, ignore_missing=ignore_missing)

    def find_group(self, name_or_id, ignore_missing=True):
        """Find a single group

        :param name_or_id: The name or ID of a group
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent group.

        :returns: ``None``
        """
        return self._find(_group.Group, name_or_id,
                          ignore_missing=ignore_missing,
                          name=name_or_id)

    def resume_group(self, group):
        """resume group

        :param group: The value can be the ID of a group
             or a :class:`~openstack.auto_scaling.v2.group.Group` instance.
        """
        group = self._get_resource(_group.Group, group)
        group.resume(self._session)

    def pause_group(self, group):
        """pause group

        :param group: The value can be the ID of a group
             or a :class:`~openstack.auto_scaling.v2.group.Group` instance.
        """
        group = self._get_resource(_group.Group, group)
        group.pause(self._session)

    def policies(self, **query):
        """Retrieve a generator of policies
        :param dict query: Optional query parameters to be sent to limit the
                      resources being returned.
            * ``name``: policy name
            * ``type``: policy type
            * ``scaling_group_id``: scaling group id the policy applied to
            * ``marker``:  pagination marker
            * ``limit``: pagination limit

        :returns: A generator of policy
                  (:class:`~openstack.auto_scaling.v2.policy.Policy`) instances
        """
        return self._list(_policy.Policy, paginated=True, **query)

    def create_policy(self, **attrs):
        """Create a new policy from attributes
        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.auto_scaling.v2.policy.Policy`,
                           comprised of the properties on the Policy class.
        :returns: The results of policy creation
        :rtype: :class:`~openstack.auto_scaling.v2.policy.Policy`
        """
        return self._create(_policy.Policy, prepend_key=False, **attrs)

    def get_policy(self, policy):
        """Get a policy
        :param policy: The value can be the ID of a policy
             or a :class:`~openstack.auto_scaling.v2.policy.Policy` instance.
        :returns: Policy instance
        :rtype: :class:`~openstack.auto_scaling.v2.policy.Policy`
        """
        return self._get(_policy.Policy, policy)

    def delete_policy(self, policy, ignore_missing=True):
        """Delete a policy

        :param policy: The value can be the ID of a policy
             or a :class:`~openstack.auto_scaling.v2.policy.Policy` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the policy does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent policy.

        :returns: Policy been deleted
        :rtype: :class:`~openstack.auto_scaling.v2.policy.Policy`
        """
        return self._delete(_policy.Policy, policy, ignore_missing=ignore_missing)

    def find_policy(self, name_or_id, ignore_missing=True):
        """Find a single policy

        :param name_or_id: The name or ID of a policy
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the policy does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent policy.

        :returns: ``None``
        """
        return self._find(_policy.Policy, name_or_id,
                          ignore_missing=ignore_missing,
                          name=name_or_id)