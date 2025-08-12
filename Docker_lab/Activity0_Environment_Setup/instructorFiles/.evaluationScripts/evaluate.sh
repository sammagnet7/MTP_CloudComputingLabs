#!/bin/bash
#
# evaluate.sh
# ------------
# This script is executed automatically during lab evaluation.
# It sets up the lab directory contents into the autograder workspace,
# runs the grading script, and then cleans up.
#

# Path to instructor-provided evaluation scripts
INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"

# Path to student lab directory containing submitted files
LAB_DIRECTORY="../labDirectory"

# Save the current working directory so we can return later
ptcd=$(pwd)

# Navigate to instructor's evaluation scripts directory
cd "$INSTRUCTOR_SCRIPTS" || {
    echo "ERROR: Failed to navigate to $INSTRUCTOR_SCRIPTS"
    exit 1
}

# List all files/folders in the lab directory
list_of_files="$(ls "$LAB_DIRECTORY")"

# Copy lab submission files into the autograder directory
# (These are the files to be tested)
cp -r "$LAB_DIRECTORY"/* autograder/

# Move into the autograder directory to run grading scripts
cd ./autograder/ || {
    echo "ERROR: Failed to navigate to autograder directory."
    exit 1
}

# Adjust permissions for all copied files (read/write/execute for everyone)
chmod -R 777 $list_of_files

# Run the main grading script
./grader.sh

# Remove the copied student files from autograder after grading
rm -r $list_of_files

# Return to the original directory
cd "$ptcd" || exit 0
