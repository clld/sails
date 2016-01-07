from setuptools import setup, find_packages

requires = [
    'clld>=1.5.0,<2.0.0',
    'clldmpg>=1.1.1',
]

tests_require = [
    'WebTest',
    'mock==1.0',
]

setup(name='sails',
      version='0.0',
      description='sails',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      test_suite="sails",
      entry_points="""\
      [paste.app_factory]
      main = sails:main
      """)
