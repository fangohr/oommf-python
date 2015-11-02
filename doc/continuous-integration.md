# Continuous integration

[![Build and test state Travis](https://travis-ci.org/fangohr/oommf-python.svg?branch=master)](https://travis-ci.org/fangohr/oommf-python) [![Build and test state Circle CI](https://circleci.com/gh/fangohr/oommf-python.svg?style=svg)](https://circleci.com/gh/fangohr/oommf-python)

We used continuous integration on travis CI and circle CI to automatically execute the tests in this repository.

To do this, we need an executable version of OOMMF. Tests are run through 'make test' in the top directory.

## OOMMF on travis CI
[![Build Status](https://travis-ci.org/fangohr/oommf-python.svg?branch=master)](https://travis-ci.org/fangohr/oommf-python)

OOMMF on our [travis build](https://travis-ci.org/fangohr/oommf-python) is compiled from source, using version 1.2.0.5. See `.travis.yml` for details.

## OOMMF on circle CI
[![Circle CI](https://circleci.com/gh/fangohr/oommf-python.svg?style=svg)](https://circleci.com/gh/fangohr/oommf-python)

[OOMMF on the Circle CI system](https://circleci.com/gh/fangohr/oommf-python) is installed via an Anaconda package, using version 1.2.0.6. See `circle.yml' for details.

