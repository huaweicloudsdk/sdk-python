The RDS API
===========

For details on how to use rds, see :doc:`/users/guides/rds`

.. automodule:: openstack.rds.v1._proxy

The RDS Class
--------------------

The rds high-level interface is available through the ``rds``
member of a :class:`~openstack.connection.Connection` object.
The ``rds`` member will only be added if the service is detected.

Datastore Version Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: openstack.rds.v1._proxy.Proxy

   .. automethod:: openstack.rds.v1._proxy.Proxy.datastore_versions

Instance Operations
^^^^^^^^^^^^^^^^^^^
.. autoclass:: openstack.rds.v1._proxy.Proxy

   .. automethod:: openstack.rds.v1._proxy.Proxy.instances
   .. automethod:: openstack.rds.v1._proxy.Proxy.get_instance
   .. automethod:: openstack.rds.v1._proxy.Proxy.delete_instance
   .. automethod:: openstack.rds.v1._proxy.Proxy.create_instance
   .. automethod:: openstack.rds.v1._proxy.Proxy.resize_instance
   .. automethod:: openstack.rds.v1._proxy.Proxy.resize_instance_volume
   .. automethod:: openstack.rds.v1._proxy.Proxy.restart_instance
   .. automethod:: openstack.rds.v1._proxy.Proxy.restore_instance
   .. automethod:: openstack.rds.v1._proxy.Proxy.set_instance_params
   .. automethod:: openstack.rds.v1._proxy.Proxy.reset_instance_params
   .. automethod:: openstack.rds.v1._proxy.Proxy.list_instance_errorlog
   .. automethod:: openstack.rds.v1._proxy.Proxy.list_instance_slowlog

Flavor Operations
^^^^^^^^^^^^^^^^^
.. autoclass:: openstack.rds.v1._proxy.Proxy

   .. automethod:: openstack.rds.v1._proxy.Proxy.flavors
   .. automethod:: openstack.rds.v1._proxy.Proxy.get_flavor

Backup Operations
^^^^^^^^^^^^^^^^^
.. autoclass:: openstack.rds.v1._proxy.Proxy

   .. automethod:: openstack.rds.v1._proxy.Proxy.backups
   .. automethod:: openstack.rds.v1._proxy.Proxy.create_backup
   .. automethod:: openstack.rds.v1._proxy.Proxy.delete_backup
   .. automethod:: openstack.rds.v1._proxy.Proxy.create_backup_policy
   .. automethod:: openstack.rds.v1._proxy.Proxy.get_backup_policy

Parameters Operations
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: openstack.rds.v1._proxy.Proxy

   .. automethod:: openstack.rds.v1._proxy.Proxy.parameters
   .. automethod:: openstack.rds.v1._proxy.Proxy.get_parameter
