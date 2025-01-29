# Python_DLMDSPWP01

## Overview
This project implements an **Ideal Function Selector** that selects the best-fitting ideal function based on the least squared deviation from a given training dataset.

## Features
- Reads training and ideal function data.
- Computes the least squared deviation.
- Selects the best ideal functions based on minimum deviation.
- Test input test data to evaluate whether it fits with selected four ideal functions
- Supports unit testing.

## Setup

### 1. Create and Activate Virtual Environment
First, create a virtual environment to manage dependencies:
```sh
python3 -m venv vir_env
```
Then activate it:
On Linux or Mac:
```sh
source vir_env/bin/activate
```
On Windows:
```sh
vir_env\Scripts\activate
```
or
```sh
.\vir_env\Scripts\Activate
```

### 2. Install dependency packages
```sh
pip install -r requirements.txt
```

## Run the task solver program

### 1. Execute the program to solve the assignment
```sh
cd task_solver
python main.py
```
### 2. Check the result in output folder

## Run the unittest
To run all tests:
```sh
cd task_solver
python -m unittest discover -s tests
```
