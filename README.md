# Build and install the parser

git clone --depth=1 https://github.com/tree-sitter/tree-sitter-c.git
mv ./tree-sitter-c ./vendor

python setup.py sdist
pip install dist/c_inspectors-0.1.tar.gz
