#!/bin/bash

# A script to run the "lite" ("one-word-per-each-paradigm-") testvoc.
#
# Assumes the pair is compiled.
# Extracts lexical units from compressed text files in languages/apertium-chv/
# tests/morphotactics/ and passes them through the translator (=INCONSISTENCY
# script).
# Produces 'testvoc-summary.chv-tat.txt' file using the INCONSISTENCY_SUMMARY script.
#
# TODO: Generate stats about each file (e.g. N1.txt), not just about the category (e.g. nouns).
#
# Usage: [TMPDIR=/path/to/tmpdir] ./testvoc.sh

INCONSISTENCY=tests/testvoc/standard/inconsistency.sh
INCONSISTENCY_SUMMARY=tests/testvoc/standard/inconsistency-summary.sh

if [ -z $TMPDIR ]; then
	TMPDIR="/tmp"
fi

export TMPDIR

function extract_lexical_units {
    sort -u | cut -f2 -d':' | \
    sed 's/^/^/g' | sed 's/$/$ ^.<sent>$/g'
}

#-------------------------------------------------------------------------------
# Chuvash->Tatar testvoc
#-------------------------------------------------------------------------------

PARDEF_FILES=../../apertium-languages/apertium-chv/tests/morphotactics/*.txt.gz

echo "==Chuvash->Tatar==========================="

echo "" > $TMPDIR/chv-tat.testvoc

for file in $PARDEF_FILES; do
    zcat $file | extract_lexical_units |
    $INCONSISTENCY chv-tat >> $TMPDIR/chv-tat.testvoc
done

$INCONSISTENCY_SUMMARY $TMPDIR/chv-tat.testvoc chv-tat
