# CI Path Filter

A command-line tool that decides which CI/CD pipelines should run based on the files changed in a commit. It reads named filters (defined as glob patterns in a YAML file), checks them against a list of changed files, and outputs which filters matched in a `.env` format that a CI system can read.

The point is to avoid running every pipeline on every change. If someone only touches the docs, there's no reason to run the backend build.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py <config.yaml> <output.env> <changed_file> [more_files ...]
```

Example:

```bash
python3 main.py filters.yaml output.env app/src/main/Payment.kt README.md
```

This checks the two changed files against every filter and writes the results to `output.env`:

```
backend=true
docs=true
```

## Filter config

Filters live in a YAML file. Each filter has a name and a list of glob patterns. A pattern starting with `!` is an exclusion.

```yaml
filters:
  backend:
    - "app/src/**/*.kt"
    - "!app/src/test/**"
  docs:
    - "README.md"
    - "docs/**/*.md"
```

A filter is `true` if at least one changed file matches one of its include patterns and does not match any of its exclude patterns.

## How it works

The code is split into small modules, each doing one job:

- `config_parser.py` — reads and validates the YAML
- `glob_matcher.py` — matches one file path against one glob pattern
- `filter_evaluator.py` — runs the include/exclude logic for each filter
- `output_writer.py` — writes the results as a `.env` file
- `main.py` — the CLI that ties it all together

## Design decisions

- **I translate globs to regex myself instead of using a globbing library.** The spec defines specific behavior for `*`, `**`, and `!`, so I wanted to implement exactly that and keep the tool dependency-light. If the pattern grammar got bigger, I'd reach for a library like `pathspec`.
- **Error handling lives at the boundaries, not in the core logic.** I handle failures where input comes from outside my control — reading the config file, writing the output file. The internal matching logic isn't wrapped in try/except, because those inputs are already validated by then, and defensive handling there would just hide bugs. Correctness of the core is covered by the tests instead.
- **The tool exits with a non-zero code on failure.** A CI system reads exit codes to decide if a step passed. If the tool hit a bad config but exited 0, the pipeline would treat it as success and keep going with wrong data. Exiting non-zero makes the pipeline fail correctly.
- **Output is lowercase `true`/`false`.** CI and shell comparisons are usually case-sensitive, so the output has to match exactly what the consumer expects, not Python's capitalized booleans.
- **Matching is case-sensitive**, which lines up with how file paths work on typical Unix systems.

## Assumptions

- A filter with only exclude patterns and no includes matches nothing, so it's `false`.
- If no files changed, every filter is `false`.
- The config file is expected to have a top-level `filters` section (the tool errors clearly if it doesn't).

## Limitations & possible improvements

- Supports `*`, `**`, and `!` exclusion as the spec asks for. Other glob features like `?`, character classes (`[a-z]`), and brace expansion (`{js,ts}`) aren't handled, but they'd be natural extensions of the regex translation.
- Everything runs in memory. For a very large set of changed files, patterns could be compiled once and reused for a bit more speed.

## Running the tests

```bash
python3 -m pytest tests/ -v
```

The tests cover the glob matcher (segment rules, `*` vs `**`, literal dots) and the filter evaluator (include/exclude precedence, empty inputs, and multiple filters).