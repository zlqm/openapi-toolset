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


django_plugin
---------------

write api doc in CBV(class-based-view) docstring and genereate openapi doc for project.

.. code:: bash

    # genereate openapi doc
    $ python demo/manage.py make_openapi_doc -f test.yaml
    # preview genereated openapi doc
    $ python demo/manage.py serve_openapi_doc -f test.yaml
    erving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
