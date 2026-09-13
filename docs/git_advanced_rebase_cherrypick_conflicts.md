# Advanced Git CLI Guide: Rebase, Cherry-Pick & Merge Conflict Resolution

This guide explains **Git Rebase**, **Git Cherry-Pick**, and how to resolve **Merge Conflicts** using the Git CLI in your terminal.

---

## 🎯 1. Git Merge vs Git Rebase

### Option A: `git merge` (Preserves History with a Merge Commit)
Creates a new "Merge Commit" that ties two branches together.

```text
      A---B---C (feature)
     /         \
D---E-----------F (main, merge commit)
```

### Option B: `git rebase` (Re-applies Commits for a Linear History)
Moves your feature branch commits so they sit directly **on top of** the latest `main` commit.

```text
                  A'---B'---C' (feature rebased onto main)
                 /
D---E-----------F (main)
```

#### Why use `git rebase`?
1. Keeps Git history clean, linear, and easy to read (`git log --oneline`).
2. Avoids cluttered "Merge branch 'main' into feature" commits.

#### How to Rebase via Git CLI:
```bash
# 1. Switch to your feature branch
git checkout feature/new-calculator-feature

# 2. Rebase onto latest main
git rebase main
```

---

## 🍒 2. Git Cherry-Pick

### What is `git cherry-pick`?
`git cherry-pick <commit-hash>` allows you to copy a **single specific commit** from another branch into your current branch, without merging the entire branch.

```text
Branch A:  C1 --- C2 --- C3 (Fix critical bug) --- C4
                            │
                            ▼ (cherry-pick C3)
Branch B:  D1 --- D2 --- C3'
```

#### How to Cherry-Pick via Git CLI:
```bash
# 1. Find the commit hash from another branch
git log --oneline feature/experimental

# Output:
# a1b2c3d Add discount calculation logic
# e4f5g6h Experimental broken code

# 2. Switch to main (or target branch)
git checkout main

# 3. Cherry-pick only the good commit
git cherry-pick a1b2c3d
```

---

## ⚔️ 3. Understanding Merge Conflicts

A **Merge Conflict** happens when Git cannot automatically determine which code to keep because **two different commits modified the exact same line(s) of code** in a file.

### What Conflict Markers Look Like inside a file:

```python
<<<<<<< HEAD (Current Branch / Yours)
def add(a, b):
    return a + b
=======
def add(a, b):
    return round(a + b, 2)
>>>>>>> feature/formatting (Incoming Branch / Theirs)
```

- **`<<<<<<< HEAD`**: Start of your current branch's code.
- **`=======`**: The divider separating the conflicting changes.
- **`>>>>>>> <branch_or_commit>`**: End of incoming code being merged or rebased.

---

## 🛠️ Step-by-Step Conflict Resolution via Terminal CLI

### Step 1: Identify Conflicting Files
When a rebase or merge halts, run:
```bash
git status
```
Git will list files under `Unmerged paths:` (e.g. `both modified: src/calculator.py`).

### Step 2: Open File & Edit Conflict Markers
Open the file in your code editor. Delete the markers (`<<<<<<<`, `=======`, `>>>>>>>`) and keep the correct code.

**Before:**
```python
<<<<<<< HEAD
    return a + b
=======
    return round(a + b, 2)
>>>>>>> feature/formatting
```

**After (Resolved):**
```python
    return round(a + b, 2)
```

### Step 3: Stage the Resolved File
```bash
git add src/calculator.py
```

### Step 4: Continue the Operation

- **If resolving during a Rebase:**
  ```bash
  git rebase --continue
  ```
- **If resolving during a Merge:**
  ```bash
  git merge --continue
  # (or git commit)
  ```
- **If resolving during a Cherry-Pick:**
  ```bash
  git cherry-pick --continue
  ```

> [!TIP]
> If you ever get stuck or want to cancel a rebase/cherry-pick and go back to safety, run:
> - `git rebase --abort`
> - `git cherry-pick --abort`
> - `git merge --abort`
