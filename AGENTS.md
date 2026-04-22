# Repository Guidelines
所有回答使用中文
使用奥卡姆剃刀原则，我只需要最精准的内容
## Project Structure & Module Organization
This repository is currently minimal. The root contains a single empty file, `会议内容`, and no detected `src/`, `tests/`, or build configuration files yet. Keep new code organized by purpose: place implementation code under a dedicated source directory such as `src/` or a language-specific package folder, and place tests in `tests/` or the matching convention for the language you add. Store project notes and non-code assets in clearly named top-level directories instead of mixing them into the root.

## Build, Test, and Development Commands
No build or test commands are defined yet. Before contributing, inspect the current state with simple shell checks such as `ls -la` and `find . -maxdepth 2 -type f`. Once Git is initialized, use `git status` to confirm your change set before opening a review. If you introduce a toolchain, add its primary local commands here, for example `make test`, `pytest`, or `npm test`, and keep them reproducible from the repository root.

## Coding Style & Naming Conventions
Match the conventions of the language you introduce rather than inventing mixed styles. Use consistent indentation within each file, prefer descriptive names, and keep filenames predictable, such as `graph_builder.py`, `train_model.js`, or `test_graph.py`. Avoid one-off scripts in the root unless they are entrypoints with clear names.

## Testing Guidelines
Every new feature or bug fix should include automated tests when practical. Keep tests close to the code they validate, use names that describe behavior, and cover both expected paths and obvious failures. If a module cannot be tested yet, note the gap in the pull request description.

## Commit & Pull Request Guidelines
No local Git history is available, so use a simple imperative commit style such as `Add GraphSAGE training scaffold` or `Document repository layout`. Keep pull requests small, explain the purpose, list any new commands or directories, and include sample output or screenshots when the change affects visible behavior.

## Current State
This guide reflects the repository as of April 22, 2026: a minimal workspace with no established build system, CI, or test framework. Update this file when those foundations are added.
