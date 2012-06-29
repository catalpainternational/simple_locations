from setuptools import setup

setup(
    name='simple_locations',
    version='1.0',
    license="",

    install_requires = [
        "",

],

    description="The common location package used for catalpa's projects.",
    long_description=open('README.md').read(),
    author='Anders Hofstee, Nicoas Hoibian',
    author_email='a.hofstee@catalpainternational.org',

    url='https://github.com/catalpainternational/simple_locations',
    include_package_data=True,

    packages=['simple_locations'],
    package_data={'simple_locations':['README.md']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)