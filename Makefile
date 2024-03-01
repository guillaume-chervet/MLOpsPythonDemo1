cwd=$(pwd)

cd train
poetry install --no-root

cd $cwd

cd train/extraction
poetry install --no-root

cd train/output
poetry install --no-root
cd $cwd

cd train/output
poetry install --no-root

cd $cwd
