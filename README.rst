Magento - Flexible Shopping Store eCommerce Platform
====================================================

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
   - Hourly cron job for maintenance.

- SSL support out of the box.
- `Adminer`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email from web
  applications (e.g., password recovery)
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, Adminer: username **root**


.. _Magento: http://www.magentocommerce.com/
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _Adminer: http://www.adminer.org/
