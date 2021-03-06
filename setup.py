from setuptools import setup, find_packages


setup(
    name='simple_locations',
    version='2.77',
    license="BSD",

    description="The common location package used for catalpa's projects.",
    long_description=open('README.md').read(),
    author='Anders Hofstee, Nicoas Hoibian',
    author_email='engineering@catalpa.io',
    url='https://github.com/catalpainternational/simple_locations',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['django-mptt>=0.11.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
