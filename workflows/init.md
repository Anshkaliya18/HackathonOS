# HackathonOS — INIT Workflow

**Operation**: INIT  
**Purpose**: Initialize HackathonOS for a new hackathon project. Creates the `.hackathon/` directory and `project-state.md` inside the hackathon project's repository, not in the skill directory.

## When to Use

Use INIT when:
- Starting a new hackathon project
- `.hackathon/` does not exist in the current project repository
- You want to reset or re-initialize project state

## Workflow Steps

### Step 1: Confirm Project Location

Verify the current working directory is the hackathon project's repository root. Look for signs of a project:
- `package.json`, `requirements.txt`, `pyproject.toml`, or similar
- Source code directories
- README or documentation

If no project repository is detected, ask the user to confirm the project root before proceeding.

### Step 2: Collect Hackathon Information

Ask the user for the following. If the user does not know a value, record it as `UNKNOWN` — never guess:

1. **Hackathon name** — What hackathon are you participating in?
2. **Deadline** — When is the submission deadline? (date and time, with timezone if known)
3. **Problem statement** — What is the problem you're trying to solve?
4. **Hackathon rules / judging criteria** — What are the rules and how will projects be judged? Include criteria weights if known.
5. **Target users** — Who is the product for?
6. **Submission requirements** — What must be submitted (repo link, demo video, PPT, etc.)?

### Step 3: Create Configuration Templates Safely

From the verified target project root, run `core/configuration/manager.py init` with `--project-root` set to that root. This creates missing configuration templates, adds minimal `.gitignore` protections, records the known project path, and preserves every existing file. Do not run INIT against the HackathonOS framework repository.

Create `.env` only when local overrides or credentials are needed. If created, derive it from `.env.example` after confirming it is ignored by Git. Never write credentials into JSON, Markdown, command output, or evidence.

### Step 4: Create `.hackathon/` Directory

Create `.hackathon/` in the project repository root:

```
.hackathon/
└── project-state.md
```

### Step 5: Write `project-state.md`

Copy `templates/project-state.md` into `.hackathon/project-state.md` and fill in the known values from Step 2. All unknown values remain `UNKNOWN`.

Set:
- `Phase` = "Understand Rules"
- `State last updated` = current UTC date/time
- All collected hackathon information
- All unknown fields = `UNKNOWN`

### Step 6: Confirm Initialization

Report back to the user:
- Confirmation that `.hackathon/project-state.md` was created
- Summary of what was recorded
- Summary of what is still `UNKNOWN`
- The recommended next action (typically STATUS or beginning the "Understand Rules" phase)

## Example Output

```
HackathonOS initialized for "TechCrunch Disrupt 2026".

Created: .hackathon/project-state.md

Recorded:
  - Hackathon name: TechCrunch Disrupt 2026
  - Deadline: 2026-11-15T23:59:00 UTC
  - Problem statement: [as provided]
  - Judging criteria: [as provided]

Still UNKNOWN:
  - Target users
  - Submission requirements
  - Tech stack
  - Selected idea

Next: Run /hackathonos status to see current state, or continue with problem analysis.
```

## Validation

After INIT completes:
- [ ] `.hackathon/` directory exists in project repo
- [ ] `.hackathon/project-state.md` exists
- [ ] All user-provided values are recorded accurately
- [ ] All unknown values are marked `UNKNOWN` (not invented)
- [ ] `Phase` is set to "Understand Rules"
- [ ] State was NOT written into the skill installation directory
- [ ] Existing files and values were preserved
- [ ] `.env` remains ignored by Git and contains no committed credentials
