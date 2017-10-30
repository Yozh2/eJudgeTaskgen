#!/bin/bash
# UNIX or Linux
# Automatic check system scriprt for offline testing
# NOTE: solutions are in the same dir as html file

# from /contests/c/int dir:  ../checkit.sh c int_ksg sum
# from /contests/c/int dir:  ../checkit.sh c int_ksg sum --make_test

PROGNAME=`basename $0`
TASK_DIR="."
SOLUTION_DIR="."

function usage()
{
	# echo "Usage: $PROGNAME language chapter task_number [--readline]" 1>&2
	echo "Usage: $PROGNAME language chapter task_number [--make_test]" 1>&2
	echo "Example: $PROGNAME c++ arr 00" 1>&2
	exit 0
}
# Check for correct number of parameters
test $# -gt 1 || usage;

case "$1" in 
    "c++")
        GCC="g++"
        EXT="cpp"
        ;;
     "c")
        GCC="gcc"
        EXT="c"
        ;;
esac
shift
 
SUBDIR="$1"
TASKNAME="$2"
MAKE_TEST=$3

TASKID="${SUBDIR}_$2"
DIR="$TASK_DIR/$SUBDIR/$TASKID"
if [ -d  "./$DIR/$TASK_ID" ] ; then 
	# SUBDIR="if", TASKNAME="max", TASK_ID="if_max"  DIR="./if/if_max"
	echo "./$DIR/$TASK_ID"
else 
	# SUBDIR="if/kr3", TASKNAME="max", TASK_ID="max"  DIR="./if/kr3/max"
	DIR="$TASK_DIR/$SUBDIR/$TASKNAME"
	TASKID="$TASKNAME"
fi

PREFIX_BEFORE="_begin"
PREFIX_AFTER="_end"
PREFIX_SOLUTION="_solution"
TMP_DIR="$DIR/tmp"
test -d "$TMP_DIR" || mkdir "$TMP_DIR"

# Assemble C file from multiple files if needed
CFILE="${TMP_DIR}/${TASKID}".$EXT
test -f $CFILE && rm -f $CFILE 
test -f "$DIR/${TASKID}${PREFIX_BEFORE}".$EXT && \
	cp  "$DIR/${TASKID}${PREFIX_BEFORE}".$EXT "$CFILE"
cat "$DIR/${TASKID}${PREFIX_SOLUTION}".$EXT >> "$CFILE"
test -f "$DIR/${TASKID}${PREFIX_AFTER}".$EXT && \
	cat "$DIR/${TASKID}${PREFIX_AFTER}".$EXT >> "$CFILE"

# Compile task before testing
$GCC -Wall -DOFFLINE_BUILD -DAAA -o "$TMP_DIR/$TASKID.exe" "$CFILE"
if test $? -ne 0; then
	# Error message is printed by compiler
	exit 1
fi

# Run all tests
for ID in $DIR/tests/*.dat ; do
	ID=`basename $ID .dat`
	# echo $ID
	echo "======================= TEST $ID"
	if test "$MAKE_TEST" == "--make_test" ; then
		echo "Make test $ID"
		"$TMP_DIR/$TASKID.exe" < "$DIR/tests/$ID.dat" > "$DIR/tests/$ID.ans"
	else 
		"$TMP_DIR/$TASKID.exe" < "$DIR/tests/$ID.dat" | diff -b -B - "$DIR/tests/$ID.ans"
		if test $? -ne 0; then
			# Error message is printed by compiler
			echo "........................FAIL"
			echo "INPUT DATA:"
			cat "$DIR/tests/$ID.dat"
			# exit 1
		else
			echo "....................... OK"
		fi
	fi
done
exit 0

