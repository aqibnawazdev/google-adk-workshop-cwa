#!/bin/bash
# create-checkpoints.sh - Create workshop checkpoint branches
#
# This script creates checkpoint branches that allow participants to catch up
# if they fall behind during the workshop. Each checkpoint contains the complete
# working code up to that exercise.
#
# IMPORTANT: Run this from the repository root after completing all exercises.
# Workshop instructors should run this before delivering the workshop.
#
# Usage:
#   ./workshop-materials/scripts/create-checkpoints.sh
#
# The script creates 4 checkpoint branches:
#   - checkpoint/exercise-1: Basic agent working (start of Exercise 2)
#   - checkpoint/exercise-2: Function calling working (start of Exercise 3)
#   - checkpoint/exercise-3: RAG integration working (start of Exercise 4)
#   - checkpoint/exercise-4: Complete implementation

set -e  # Exit on error

echo "Creating workshop checkpoint branches..."
echo "========================================"
echo ""
echo "This script creates checkpoint branches from main."
echo "Participants can use these to catch up if they fall behind."
echo ""

# Check we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Ensure we're on main with latest code
echo "Switching to main branch..."
git checkout main
git pull origin main 2>/dev/null || echo "  (No remote to pull from - continuing)"
echo ""

# Function to create checkpoint branch
create_checkpoint() {
    local branch_name=$1
    local description=$2
    local exercise_num=$3

    echo "Creating $branch_name..."

    # Delete local branch if exists
    git branch -D "$branch_name" 2>/dev/null || true

    # Create new branch from main
    git checkout -b "$branch_name"

    # Push to remote (if remote exists)
    if git remote | grep -q origin; then
        git push -u origin "$branch_name" --force 2>/dev/null && \
            echo "  Pushed to remote" || \
            echo "  (Could not push to remote - continuing)"
    else
        echo "  (No remote configured - skipping push)"
    fi

    # Return to main
    git checkout main > /dev/null 2>&1

    echo "  [OK] $branch_name created"
    echo "       - $description"
    echo "       - Use: git checkout $branch_name"
    echo ""
}

# Create all checkpoints
# Note: All checkpoints point to main (complete implementation)
# This works because the workshop is progressive - each exercise builds
# on the previous. The documentation in CHECKPOINTS.md explains which
# files to focus on for each exercise.

create_checkpoint "checkpoint/exercise-1" "Basic agent working" 1
create_checkpoint "checkpoint/exercise-2" "Function calling tools working" 2
create_checkpoint "checkpoint/exercise-3" "RAG integration working" 3
create_checkpoint "checkpoint/exercise-4" "State management working (complete)" 4

echo "========================================"
echo "[DONE] All checkpoint branches created!"
echo ""
echo "Participants can catch up with:"
echo "  git checkout checkpoint/exercise-2"
echo ""
echo "To see all checkpoints:"
echo "  git branch -a | grep checkpoint"
echo ""
echo "Branch summary:"
echo "  checkpoint/exercise-1 -> Start of Exercise 2 (basic agent complete)"
echo "  checkpoint/exercise-2 -> Start of Exercise 3 (function calling complete)"
echo "  checkpoint/exercise-3 -> Start of Exercise 4 (RAG complete)"
echo "  checkpoint/exercise-4 -> Complete implementation"
