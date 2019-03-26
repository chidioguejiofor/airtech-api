#!/usr/bin/env bash

echo "Running our bash script"

PYTHON_FILES=$( git diff --cached --name-only --diff-filter=AM | grep --color=never .py$ )

if [ "${PYTHON_FILES[*]}" == "" ];
then
    echo "No python files to lint"
    exit 0
fi

echo "Running Linting with yapf..."
yapf -ir ${PYTHON_FILES[*]}


CHANGED_FILES=$( git diff --name-only ${PYTHON_FILES[*]} )

if [ "${CHANGED_FILES[*]}" == "" ];
then
    echo "Linting did not correct any files"
    echo "Linting checks successful"
    echo "Opening commit window..."
    exit 0
else
    echo "Some changes were made to your file!"
    echo "Check them out and try the commit again!"
    exit 1
fi

