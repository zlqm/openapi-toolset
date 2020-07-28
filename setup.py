import setuptools

setuptools.setup(
    name='openapi_toolset',
    version='1.0',
    author='Abraham',
    author_email='abraham.liu@hotmail.com',
    description='a collection toolset for openapi',
    install_requires=['py-openapi-schema-to-json-schema>=0.0.3'],
    extra_require={
        'django': ['pyyaml', 'jsonschema', 'django']
    },
    include_package_data=True,
    packages=setuptools.find_packages(),
    scripts=[
        'scripts/simple-openapi-server',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
