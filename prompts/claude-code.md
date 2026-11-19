# Your first Claude Code session

Use these once your team has a GitHub repository with your data in it and Claude Code open on it (see the
set-up slides). They follow the same six parts, shortened: in Claude Code the AI can read your files, so you
describe the files less and the reader and the decision more.

## cc-1 | cc | 1 | Orient: before writing any code

```
ROLE
You are a data analyst joining our hackathon team.

CONTEXT
We have 2.5 days to build a dashboard that helps [name the reader] decide
[name the decision]. Our data is in the data/ folder.

TASK
Read every file in data/ and tell us: what each file contains, the time span,
the problems you see, and three questions this data could answer for our
reader. Do not write any code yet.
```

## cc-2 | cc | 2 | Plan: agree the plan before the build

```
TASK
Propose a plan for a one-screen dashboard that answers: [your question].
List the numbers you will compute (with formulas), the charts (one line each,
saying why that chart), and the checks you will run. Wait for our approval
before writing code.
```

## cc-3 | cc | 3 | Build: one stage at a time

```
TASK
Build stage 1 of the plan only: compute the numbers and print them in a
table. Save the code in analysis/ and explain each step in a comment. Then
stop so we can check the numbers.
```

## cc-4 | cc | 4 | Publish: get a link to share

```
TASK
Put the finished dashboard in docs/index.html as one self-contained file,
commit it with a clear message, and push. Then tell us how to turn on
GitHub Pages for the docs/ folder so the judges can open it from a link.
```

## cc-5 | cc | 5 | Challenge: before the pitch

```
ROLE
You are a sceptical judge at the hackathon.

TASK
Open docs/index.html and the code that produced it. List the three numbers
you would question first and recompute each one from the raw data. Then tell
us, in two sentences, what our dashboard does not show that the reader would
need.
```
