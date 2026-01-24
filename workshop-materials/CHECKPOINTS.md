# Workshop Checkpoint Branches

## Overview

If you fall behind during the workshop, you can use checkpoint branches to catch up to the current exercise. Each checkpoint contains the complete working code up to that point, allowing you to continue with the rest of the workshop.

**Don't worry about falling behind!** The checkpoints are here specifically to help you keep learning. It's better to catch up and continue than to stay stuck.

## Available Checkpoints

| Checkpoint | What's Working | When to Use |
|------------|----------------|-------------|
| `checkpoint/exercise-1` | Basic ADK agent | Start of Exercise 2 |
| `checkpoint/exercise-2` | Function calling tools | Start of Exercise 3 |
| `checkpoint/exercise-3` | RAG integration | Start of Exercise 4 |
| `checkpoint/exercise-4` | State management | Complete implementation |

## How to Catch Up

### Step 1: Save your current work (optional)

If you want to save your progress to look at later:

```bash
git stash
```

This saves your work temporarily. You can get it back after the workshop.

### Step 2: Switch to checkpoint

Replace `exercise-2` with the checkpoint you need:

```bash
git checkout checkpoint/exercise-2
```

**Example scenarios:**
- Stuck in Exercise 2? Use `git checkout checkpoint/exercise-2` to start fresh with Exercise 2 complete
- Need to skip to Exercise 4? Use `git checkout checkpoint/exercise-3` to have Exercises 1-3 complete

### Step 3: Continue with the workshop

You now have working code from previous exercises. Open the next exercise notebook and continue with the instructor.

### Step 4: Restore your work later (optional)

After the workshop, if you want your original work back:

```bash
git checkout main
git stash pop
```

## What Each Checkpoint Contains

### checkpoint/exercise-1

**Use this to start Exercise 2**

Files ready to use:
- `01-hello-agent.ipynb`: Basic agent complete
- `reference-implementation/agent.py`: Basic agent definition

What you can do:
- Your agent responds to basic queries
- You understand agent configuration (model, name, description, instruction)

### checkpoint/exercise-2

**Use this to start Exercise 3**

Files ready to use:
- Everything from exercise-1, plus:
- `02-tools-functions.ipynb`: Function calling complete
- `reference-implementation/tools.py`: `search_flights()` and `search_hotels()` functions

What you can do:
- Your agent can search for flights and hotels
- You understand how agents call functions

### checkpoint/exercise-3

**Use this to start Exercise 4**

Files ready to use:
- Everything from exercise-2, plus:
- `03-rag-knowledge.ipynb`: RAG integration complete
- `reference-implementation/rag_tools.py`: Destination knowledge retrieval
- `reference-implementation/hybrid_agent.py`: Hybrid coordinator pattern

What you can do:
- Your agent can retrieve destination information from knowledge base
- You understand the tools vs RAG decision framework

### checkpoint/exercise-4

**Complete workshop implementation**

Files ready to use:
- Complete implementation of all exercises
- `04-sessions-state.ipynb`: State management complete
- `reference-implementation/state_utils.py`: Preference management utilities

What you can do:
- Your agent remembers user preferences across conversation turns
- Full travel assistant functionality working

## Troubleshooting

### "Your local changes would be overwritten"

Your uncommitted changes conflict with the checkpoint. Options:

**Option 1: Save your work first (recommended)**
```bash
git stash
git checkout checkpoint/exercise-2
```

**Option 2: Discard your work**
```bash
git checkout .
git checkout checkpoint/exercise-2
```

Note: Option 2 permanently deletes your changes. Only use if you don't need them.

### "branch already exists"

Delete the local branch first, then checkout:

```bash
git branch -D checkpoint/exercise-2
git checkout checkpoint/exercise-2
```

### Can't find the checkpoint branch

Make sure you have the latest branches from the repository:

```bash
git fetch origin
git checkout checkpoint/exercise-2
```

### "You are in 'detached HEAD' state"

This is normal! You can still run all the code. If you want to make changes, create a new branch:

```bash
git checkout -b my-exercise-work
```

### Changes not showing in notebook

After switching branches, you may need to:
1. Restart the Colab runtime: Runtime > Restart runtime
2. Re-run the setup cells at the top of the notebook

## Quick Reference

| I need to... | Command |
|--------------|---------|
| Save my work temporarily | `git stash` |
| Jump to exercise 2 start | `git checkout checkpoint/exercise-2` |
| Jump to exercise 3 start | `git checkout checkpoint/exercise-3` |
| Jump to exercise 4 start | `git checkout checkpoint/exercise-4` |
| Get my saved work back | `git stash pop` |
| See all checkpoints | `git branch -a \| grep checkpoint` |

## For Instructors

### Creating Checkpoint Branches

Before delivering the workshop, create the checkpoint branches:

```bash
./workshop-materials/scripts/create-checkpoints.sh
```

This script:
1. Creates all 4 checkpoint branches from main
2. Pushes them to the remote repository
3. Handles existing branches gracefully

### Recommended Checkpoint Announcements

During the workshop, announce checkpoints at these moments:

- **After Exercise 1:** "If you didn't get your basic agent working, you can catch up now with `git checkout checkpoint/exercise-1`"
- **After Exercise 2:** "If function calling isn't working, catch up with `git checkout checkpoint/exercise-2`"
- **After Exercise 3:** "If RAG isn't working, catch up with `git checkout checkpoint/exercise-3`"

### Helping Stuck Participants

If a participant is stuck:

1. First, try to help them debug their code
2. If time is short, suggest the checkpoint: "Let's catch you up so you don't miss the next exercise"
3. Remind them they can review their original code after the workshop with `git stash pop`
