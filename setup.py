from setuptools import setup, find_packages

requires = [
    'clld>=0.28',
    'clldmpg>=0.5',
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
      tests_require=requires,
      test_suite="sails",
      entry_points="""\
      [paste.app_factory]
      main = sails:main
      """,
      )
