#!/usr/bin/env bash

black --target-version py38 laser2.py
reorder-python-imports --py38-plus laser2.py
