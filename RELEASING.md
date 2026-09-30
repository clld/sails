# Releasing SAILS

```shell
git clone https://github.com/clld/sails
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
pg_dump -xO sails > sails.sql
zip sails.sql.zip sails.sql
rm sails.sql
```


