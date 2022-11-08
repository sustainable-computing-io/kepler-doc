Steps to build documentation

1. Add `.rst` files in docs/source

2. Build html

```sh
cd docs
make html
```
3. Test 
```sh
cd source
sphinx-build . -W -b linkcheck -d ../_build/doctrees ../html

```
