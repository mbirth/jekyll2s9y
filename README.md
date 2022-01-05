jekyll2s9y importer
===================

This is a tool to import my Jekyll-based [GitHub Pages](https://pages.github.com) blog/wiki
into [Serendipity](https://s9y.org).


Preparations
------------

Setup Serendipity with an SQLite database. Download the database file to where you also plan to run jekyll2s9y.


Usage
-----

Copy `config.yaml.example` to `config.yaml` and modify according to your needs. Note that
`jekyll_dir` has to point to your Jekyll base directory.

If not done already, update the Python environment:

    pipenv install

Then run the script:

    pipenv run ./jekyll2s9y.py

Now copy the new database file (`s9y_database_output` in the config.yaml) back to your server and overwrite
the old version. Also copy the `uploads` directory containing the media files. Then, in the Serendipity admin
area, edit your configuration and change the permalink for "Entry URL structure" in any way (e.g. add a letter
to the end) to have the permalinks regenerated. Afterwards, you can undo the change again.


Issues
------

If there are two entries where the permalink generation (i.e. stripping all emojis, etc.) results in the same
permalink, only the older one can be accessed.
