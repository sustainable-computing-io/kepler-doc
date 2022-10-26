Documentaion for Kepler

```
cd docs
make html

cd source
sphinx-build . -W -b linkcheck -d ../_build doctrees ../html

```
