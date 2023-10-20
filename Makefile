cwd=$(pwd)

cd train/extraction
poetry install
poetry export --without-hashes --format=requirements.txt > requirements.txt

cd $cwd