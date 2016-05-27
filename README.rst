Magento 1.9 - Flexible Shopping Store eCommerce Platform
========================================================

`Magento`_ is a feature-rich, professional open-source eCommerce
solution that offers merchants complete flexibility and control over the
look, content, and functionality of their online store.  Features
includes powerful marketing, merchandising and content management.
Magento is designed for scalability and is backed by an extensive
support network.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- Magento configurations:
   
   - Installed from upstream source code to /var/www/magento

     **Security notes**: 
     
     - Updates to Magento may require supervision so they **ARE NOT**
       configured to install automatically. See below for updating
       Magento.

     - Magento 1.9.X **IS NOT** vulnerable to CVE-2016-4010 remote PHP
       code execution vulnerability.
     
   - Hourly cron job for maintenance.

- SSL support out of the box.
- `Adminer`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email from web
  applications (e.g., password recovery)
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

Supervised Manual Magento Update
--------------------------------

For instructions on upgrading Magento 1.X please refer to the `Magento
1.X upgrade docs`_. 

To migrate your site from 1.X to 2.X please refer to `Magento 2 migration guide`_.

We recommend signing up for `Magento Security Alerts`_ for the latest
up-to-date information.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, Adminer: username **root**

.. _Magento Security Alerts: https://magento.com/security
.. _Magento 1.X upgrade docs: http://devdocs.magento.com/guides/m1x/install/installing_upgrade_details.html
.. _Magento 2 migration guide: http://devdocs.magento.com/guides/v2.0/migration/bk-migration-guide.html

.. _Magento: http://www.magentocommerce.com/
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _Adminer: http://www.adminer.org/
