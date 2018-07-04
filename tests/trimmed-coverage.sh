#!/bin/bash

## Pass text through trimmed-coverage.sh and get the number of */@/# errors for
## your pair.
##
## USAGE: cat <your text> | apertium-des<txt|html|xml|...> | ./trimmed-coverage.sh <lang1-lang2>

set -e -u

## Translation direction:
SL_TL=$1
## This file is kept even after the script is ended:
NEEDED=/tmp/corpus-stat-all-NEEDED.txt
## Percent (of * and @ error-free translated text) goal we aim
COVGOAL="95.0"
source "$(dirname $0)"/config.sh

if test -t 0 ; then
    echo "Usage:" 1>&2
    echo "\$ bzcat $LANG1.txt.bz2 | apertium-destxt | ./$0 $LANG1-$LANG2" 1>&2
    exit 1
fi

cd "$(dirname $0)"

transfout=$(mktemp -t trimmed-coverage.XXXXXXXXX)
genout=$(mktemp -t trimmed-coverage.XXXXXXXXX)
sorted=$(mktemp -t trimmed-coverage.XXXXXXXXX)

TODOstripwords="the The of oblast in In it if ki any will his this who we right 
                new their kraj that OfNm you www com org Ob http px inst also na 
                on one One On och till und with which were can when was"


### Do the translation:
# ${PIPE} TODO fix this so that translation commands are taken from the config.sh instead

apertium "${SL_TL}-transfer2" -f none -d .. | apertium-cleanstream -n | tee "$transfout" | lt-proc -g "../${SL_TL}.autogen.bin" | lt-proc -p "../${SL_TL}.autopgen.bin" > "$genout"

### Calculate stuff:
# Make sorting and printf the same regardless of locale (has to be set after apertium commands):
export LC_ALL='C'

numwords=$(grep -cF '^' "$transfout")
numstar=$(grep -cF '^*' "$transfout")
numat=$(grep -cF '^@' "$transfout")
numhash=$(grep -c '^#' "$genout") # Note: this one's a regex, the above are not

numknown_upto_ana=$(calc -p "$numwords - $numstar")
numknown_upto_bi=$(calc  -p "$numwords - $numstar - $numat")
numknown_upto_gen=$(calc -p "$numwords - $numstar - $numat - $numhash")

numNEEDED=$(calc -p "round($numwords * ($COVGOAL/100) - $numknown_upto_bi)")

pad () { printf "%*d" ${#numwords} "$1"; }
pct_of_words () { printf "% 5.1f" $(calc -p "round( $1 / $numwords * 1000)/10"); }
echo "Number of tokenised words in the corpus:         $(pad $numwords)"
echo "Number of tokenised words unknown to analyser:   $(pad $numstar)  — $(pct_of_words $numstar) % of tokens had *"
echo "                          unknown to bidix:      $(pad $numat)  — $(pct_of_words $numat) % of tokens had @" 
echo "     w/transfer errors or unknown to generator:  $(pad $numhash)  — $(pct_of_words $numhash) % of tokens had #"
echo ""
echo "Error-free coverage of analyser only:            $(pad $numknown_upto_ana)  — $(pct_of_words $numknown_upto_ana) % of tokens had no *"
echo "Error-free coverage of analyser and bidix:       $(pad $numknown_upto_bi)  — $(pct_of_words $numknown_upto_bi) % of tokens had no */@"
echo "Error-free coverage of the full translator:      $(pad $numknown_upto_gen)  — $(pct_of_words $numknown_upto_gen) % of tokens had no */@/#"
echo ""
echo "Top unknown words in the corpus:"
grep -F '^*' "$transfout" | sort -f | uniq -c | sort -gr | tee "$sorted" | head -10
echo ""
if [[ $numNEEDED -gt 0 ]]; then
    echo "Tokens NEEDED to get $COVGOAL % bidix-trimmed coverage (no */@/#): $numNEEDED"
    echo "Storing corresponding wordlist in $NEEDED"
else
    echo "Goal of $COVGOAL % bidix-trimmed coverage reached"'!'
fi

<"$sorted" awk -vn="$numNEEDED" '{print $0; t += $1; if( t > n ) exit; } END {print t}' > "$NEEDED"


# Try uncommenting this to see words that didn't pass through transfer alright:
paste "$transfout" "$genout"
# This is the full list of unknown words:
#cat "$sorted"

rm -f "$transfout" "$genout" "$sorted"
