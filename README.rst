Magento 2.2 - Flexible Shopping Store eCommerce Platform
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
   
   - Installed from upstream source code (via git/composer) to /var/www/magento

     **Security note**: Updates to Magento may require supervision so
     they **ARE NOT** configured to install automatically. See below for
     updating Magento.

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

We recommend signing up to `Magento Security Alerts`_ for latest updates.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL: username **root**
-  Adminer: username **adminer**

.. _Magento Security Alerts: https://magento.com/security/sign-up
.. _Magento 1.X upgrade docs: http://devdocs.magento.com/guides/m1x/install/installing_upgrade_details.html
.. _Magento 2 migration guide: http://devdocs.magento.com/guides/v2.2/migration/bk-migration-guide.html

.. _Magento: https://www.magentocommerce.com/
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _Adminer: https://www.adminer.org/
