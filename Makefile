cwd=$(pwd)

cd train
poetry install

cd $cwd

cd train/extraction
poetry install
poetry export --without-hashes --format=requirements.txt > requirements.txt
copy requirements.txt ./docker-context/

cd $cwd