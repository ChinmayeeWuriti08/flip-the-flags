# FlipTheFlags

**Entry point:** `gemini_reason_sample.py`


FlipTheFlags is a Gemini powered developer tool that analyzes feature flags in real codebases and explains which ones are dangerous, obsolete, or need cleanup and why.
Feature flags are often introduced for temporary rollouts, but over time they accumulate technical debt. FlipTheFlags helps engineers answer a critical question:

#### “Which feature flags should I worry about right now, and why?”

## What FlipTheFlags Does: 
FlipTheFlags scans a repository to identify feature flags and analyze how they are used across the codebase.
Each flag is classified into one of three categories:

1. Danger : Flags that control critical runtime behavior and pose high risk

2. Needs Fixing : Flags with unresolved or unclear intent

3. Obsolete / Remove : Flags that are hardcoded and no longer provide runtime control

For every flag, FlipTheFlags generates a concise, human readable explanation written like a senior engineer’s code review comment. 
It also reports how many lines of code 
depend on each flag to help engineers understand potential blast radius before making changes.

## How Gemini Is Used
FlipTheFlags uses the Gemini 3 API as a reasoning engine rather than a rule based analyzer. Gemini reasons over code context and derived signals to infer original intent,
understand how the codebase evolved, and explain why a flag is risky or unnecessary today.
To ensure reliability during API rate limits, the tool includes a deterministic local reasoning fallback that still produces meaningful classifications.

## How to Run

`python gemini_reason.py`

## How to Use FlipTheFlags


### Prerequisites
- Python 3.9 or higher
  
- A valid Gemini API key set as an environment variable

` setx GEMINI_API_KEY "YOUR_API_KEY" `
##### Step 1: Clone the repository

` git clone https://github.com/ChinmayeeWuriti08/flip-the-flags.git `


` cd flip-the-flags `

##### Step 2: Run the demo on the included sample repository


` python gemini_reason.py `


This runs FlipTheFlags on the included sample_repo, which contains representative feature flags used in the demo video.

##### Step 3: Run on a real codebase

Provide the path to any Python project as a command-line argument.

` python gemini_reason.py path/to/your/codebase `

Example:

` python gemini_reason.py real_repo/flask_realworld/conduit `


A small sample repository with feature flags is included for demonstration.

## Design Principles

1. No automatic refactoring or code modification

2. No enforcement or certainty claims

3. Focus on surfacing risk and context, not “fixing” code

4. Explanations over metrics

FlipTheFlags is designed to support engineering judgment, not replace it.

## Demo Repositories
FlipTheFlags was tested using small sample repositories and publicly available open source projects, including the official Flask tutorial application.
These repositories are used solely for demonstration and evaluation purposes.

## Limitations :

1. Static analysis only (no runtime tracing)

2. Dependency counts are approximate

3. Flag detection is language limited in the current version

4. Gemini API usage is subject to rate limits; when limits are reached, the tool falls back to deterministic local reasoning to maintain consistent output.

## Future Work:

1. Support for additional languages and configuration based flags

2. CI/CD integration for pull request feedback

3. Historical analysis of flag risk over time

4. Improved dependency and execution path analysis
