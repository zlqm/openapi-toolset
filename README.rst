################
openapi-toolset
################

Openapi-toolset provides several useful tool to help you use OPENAPI.

*********
Usuage
*********

simple previewer
-----------------

You can simpley preview a openapi doc file with this tool.

.. code:: bash

    usage: simple-openapi-server [-h] [--bind ADDRESS] [--file FILE]
                                 [--port [PORT]]
    
    optional arguments:
      -h, --help            show this help message and exit
      --bind ADDRESS, -b ADDRESS
                            Specify alternate bind address [default: all
                            interfaces]
      --file FILE, -f FILE  OPENAPI doc file [default: openapi.yaml]
      --port [PORT], -p [PORT]
                            Specify alternate port [default: 8000]
