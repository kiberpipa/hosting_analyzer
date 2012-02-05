================
Hosting analyzer
================

How to install
==============

Install::

    $ virtualenv --no-site-packages pipautils
    $ cd pipautils
    $ bin/activate
    $ pip install fabric
    $ git clone git://github.com/kiberpipa/hosting_analyzer.git

How to use
==========

Please read the discription of the functions with::

    $ fab -l

First get the configuration files from server with::

    $ fab get_confs

Then run::

    $ fab check_domains
