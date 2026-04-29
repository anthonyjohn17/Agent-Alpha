---

## name: clean-up
description: >-
  Reads a markdown context or specification document end-to-end, flags
  second-person and overly reader-specific phrasing, and rewrites passages in
  a generalized, documentation-ready tone while preserving structure and core
  meaning. Use when cleaning context.md (any filename), design notes, skill
  bases, or any long-form doc the user wants neutralized for reuse as shared
  context.

# Clean-up (context documents)

## Purpose

Normalize long-form markdown so it reads as **shared reference material** rather than a chat transcript or personal note. The file may be named anything (for example `context.md`, `context-gpt.md`, `notes.md`).

## When to apply

Use this skill when the user asks to:

- clean up, neutralize, or generalize a context or spec document
- remove second-person or overly specific tone from markdown
- prepare a document as a **base context** for skills, agents, or teams

## Non-goals

- Do not change code blocks unless the user asked to edit those regions; treat fenced code as literal unless cleanup is clearly about prose inside quotes.

## Mandatory workflow

1. **Read the entire file first** using the full path the user provides. Do not rely on excerpts, search snippets, or partial reads to decide edits.
2. **Build a mental map**: headings hierarchy, sections that are prompts vs. answers vs. appendices, lists, tables, and fenced blocks.
3. **Scan for tone issues** (see checklist below). Note line ranges or section titles, not isolated sentences without context.
4. **Rewrite in place** (or produce a single coherent replacement document) so that:
  - core claims, lists, and technical content stay intact
  - phrasing becomes generalized and clear
5. **Sanity pass**: no new contradictions; headings still match body; links and code fences unchanged unless intentionally edited.

## Detection checklist

Flag and fix patterns such as:


| Pattern                                   | Example                                    | Direction                                                                                            |
| ----------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Direct address                            | "you should", "your repo"                  | Third person or imperative without "you": "the repository", "run", "ensure"                          |
| Chat framing                              | "let's", "I want", "okay so"               | Remove; state intent as requirement or fact                                                          |
| Over-specific scenario tied to one reader | "your 10 repos", "when you push to GitHub" | Generalize: "multiple repositories", "before publication" unless the doc must stay scenario-specific |
| Subjective hype                           | "genuinely powerful", "love this"          | Neutral capability language                                                                          |
| Mixed audience                            | tutorial voice inside a spec               | Align with spec voice for the whole file, or isolate quoted examples                                 |


**Keep** second-person inside:

- quoted user prompts labeled as verbatim input
- explicit "Example (user message)" callouts where fidelity matters

If unsure whether a line is verbatim user text, **preserve** it and add a short note in chat rather than rewriting.

## Rewrite rules

1. **Preserve structure**: keep `#` / `##` hierarchy and meaningful section order unless the user asked to reorganize.
2. **Preserve meaning**: do not delete requirements, constraints, or definitions; rephrase only.
3. **Prefer**:
  - present tense, active or neutral constructions
  - "the document", "the skill", "the repository", "the workflow"
  - plural or indefinite subjects where appropriate ("reviewers", "operators")
4. **Avoid**:
  - "we" / "you" unless the document is intentionally instructional *to* a single reader and the user requested that voice
  - vague demonstratives without antecedent ("this", "that") after edits; replace with concrete nouns
5. **Lists and checklists**: keep items; tighten wording to parallel structure.
6. **Tables**: keep columns and facts; reword cells only for tone, not for new claims.

## Quality bar

Before finishing:

- Entire source file was read end-to-end at least once before edits.
- No remaining second-person unless intentionally preserved in quotes/examples.
- Core technical content and document structure unchanged in substance.
- Prose is consistent in voice across sections.

