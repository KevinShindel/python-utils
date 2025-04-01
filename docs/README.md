# Script using

```shell
python setup.py develop # ничего не генерировать, просто установить локально 
python setup.py bdist_egg # сгенерировать дистрибутив «яйцо», не включать зависимости
python setup.py bdist_wheel # сгенерировать версионированное «колесо», включить зависимости
python setup.py sdist --formats=zip,gztar,bztar,ztar,tar # исходный код
```
# Prepare for testing
    
```shell    
pipenv install -d mypy autopep8 \
  flake8 pytest bandit pydocstyle
```

# Testing using

```shell
python setup.py test
```

## Create a Wheel package

```shell
python setup.py bdist_wheel
```
