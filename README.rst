Skinnygen
=======

Skinny traffic generator

Installation
------------

To install using `pip`::

    sudo apt-get install python python-pip python-twisted
    sudo pip install -e git+git://github.com/mwicat/sccp.git#egg=sccp
    sudo pip install -e git+git://github.com/mwicat/skinnygen.git#egg=skinnygen

Getting started
---------------

Examples

Register as SEP002155D489A7 with line 333 and autoanswer all incoming calls::

    skinnygen generate --user_handler=idle --call_handler=autoanswer SEP002155D489A7 333

Register as SEP0016464292A0 with line 472 and dial random numbers::

    skinnygen generate --numbers=333 SEP0016464292A0 472
