# Releasing SAILS

- Check out the latest release of the CLDF dataset.
- Recreate the database:
  ```shell script
  $ sails-app initdb --doi "10.5281/zenodo.3608862" --repos ~/venvs/cldf/sails/
  ```
- Redeploy the app.
