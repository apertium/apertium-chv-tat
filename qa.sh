#!/bin/bash

# Takes the basename of the test scrpt in /test-scripts as an argument,
# an additional argument if the test requires it, and runs the test.
#
# Usage: ./qa.sh t1x
#        ./qa.sh testvoc reg

if [ $# -eq 0 ]
then
    testToRun=all.test
else
    testToRun=$1.test
fi

bash "test-scripts/$testToRun" "$2"
