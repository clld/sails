from setuptools import setup, find_packages


setup(
    name='sails',
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
    install_requires=[
        'clld>=6.0.0',
        'clldmpg>=3.5',
        'sqlalchemy',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
        ],
        'test': [
            'mock',
            'psycopg2',
            'pytest>=3.6',
            'pytest-clld>=1.0',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="sails",
    entry_points={
        'console_scripts': [
            'sails-app=sails.__main__:main',
        ],
        'paste.app_factory': [
            'main = sails:main',
        ],
    },
)
