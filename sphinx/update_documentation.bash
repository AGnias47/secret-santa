#!/bin/bash

# Only activate when refactoring or adding modules
# sphinx-apidoc -f -o source/ ../.

# Run the Sphinx target for generating HTML pages
mkdir -p build
sphinx-build -M html source build

# Rename so directories do not use underscores, which is incompatible with GitHub Pages
cd build/html
mv _sources sources
mv _static static
find . -type f -exec sed -i 's/_sources/sources/g' {} \;
find . -type f -exec sed -i 's/_static/static/g' {} \;
cd ../..

# Replace current docs with newly generated docs
rm -rf ../docs
mv build/html ../docs

