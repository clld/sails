# Releasing SAILS

```shell
git clone https://github.com/clld/sails
git clone --branch v2014.1 --depth 1 https://github.com/cldf-datasets/sails sails-cldf
cd sails
pip install -e .[test]
```

Recreate the database:
```shell
clld initdb development.ini --cldf ../sails-cldf/cldf/StructureDataset-metadata.json
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 sails > sails.sql.gz
```


