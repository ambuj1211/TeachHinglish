# TeachHinglish

> Universal AI-powered lecture script generator for downstream lecture-generation systems.

TeachHinglish is a **lecture script generation engine**, not a video-generation system.

Its purpose is to generate accurate, structured, subject-aware educational lecture scripts that can be consumed by different downstream lecture-generation applications. A JEE, GATE, NEET, school, B.Tech, M.Tech, university, professional-learning, or any other lecture-generation application can use TeachHinglish as its script-generation layer.

## What TeachHinglish Does

TeachHinglish accepts a teaching request containing:

- topic
- subject
- education level
- exam or learning goal
- language
- teaching style

It runs the request through a graph-based teaching workflow for planning, knowledge/context preparation, prompt construction, teaching-script generation, and validation.

The long-term goal is to produce scripts that are:

- educationally useful
- subject-aware
- appropriate for the requested learner level
- aligned with the requested goal
- structured for downstream lecture-generation software
- validated for content and mathematical correctness where applicable
- suitable for English, Hindi, or Hinglish delivery

## What TeachHinglish Does Not Do

TeachHinglish intentionally does **not** generate the final lecture media.

Out of scope:

- video generation
- avatar generation
- text-to-speech
- voice cloning
- animation rendering
- slide rendering
- video editing
- lip synchronization
- final media composition

Those capabilities belong to downstream lecture-generation systems.

## Supported Subjects

TeachHinglish currently defines 12 subject domains:

| # | Subject | Identifier |
|---|---|---|
| 1 | Physics | `physics` |
| 2 | Mathematics | `mathematics` |
| 3 | Chemistry | `chemistry` |
| 4 | Biology | `biology` |
| 5 | History | `history` |
| 6 | Civics | `civics` |
| 7 | Geography | `geography` |
| 8 | English Grammar | `english_grammar` |
| 9 | Computer Science | `computer_science` |
| 10 | Engineering Mathematics | `engineering_mathematics` |
| 11 | Digital Logic | `digital_logic` |
| 12 | General | `general` |

These subjects are intentionally **not tied to a particular examination**.

For example, Physics can be used by JEE, NEET, school, or other lecture applications. Computer Science and Digital Logic can be used by GATE, B.Tech, M.Tech, or other applications.

## Supported Education Levels

The current request model supports:

- Class 6
- Class 7
- Class 8
- Class 9
- Class 10
- Class 11
- Class 12
- JEE
- NEET
- GATE
- B.Tech
- M.Tech
- University
- Professional
- General

The `exam_goal` field is intentionally free-form so downstream applications are not restricted to a fixed examination list.

Examples:

```text
jee
neet
gate
conceptual understanding
board examination
university examination
interview preparation
competitive examination
```

## Languages

The current request model supports:

- `hinglish`
- `hindi`
- `english`

Hinglish is the default language.

## Teaching Styles

| Style | Identifier |
|---|---|
| Conceptual | `conceptual` |
| Exam-focused | `exam_focused` |
| Deep theory | `deep_theory` |
| Conversational | `conversational` |

## Architecture

TeachHinglish separates the public API, core engine, graph workflow, providers, prompts, subjects, and validation components.

```text
                         TeachingRequest
                                |
                                v
                    TeacherLanguageEngine
                                |
                                v
                       TeachingState
                                |
                                v
                       +----------------+
                       |    Planner     |
                       +-------+--------+
                               |
                               v
                       +----------------+
                       |   Knowledge    |
                       +-------+--------+
                               |
                               v
                       +----------------+
                       |     Prompt     |
                       +-------+--------+
                               |
                               v
                       +----------------+
                       |    Teacher     |
                       |  LLM provider  |
                       +-------+--------+
                               |
                               v
                       +----------------+
                       |   Validator    |
                       +-------+--------+
                               |
                    +----------+----------+
                    |                     |
                  PASS                  FAIL
                    |                     |
                    v                     v
                   END              retry generation
```

The workflow is implemented with LangGraph.

## Teaching Workflow

The current graph contains these stages:

1. **Planner** — prepares the teaching plan.
2. **Knowledge** — loads subject/context information.
3. **Prompt** — constructs the teaching prompt.
4. **Teacher** — generates the teaching script through the configured LLM provider.
5. **Validator** — validates the generated script.
6. **Retry** — regenerates when validation fails and the retry limit has not been reached.

The current graph allows up to two validation retries before ending.

## Validation

Validation is a core part of TeachHinglish.

Current validation areas include:

- content validation
- structure validation
- topic coverage validation
- mathematical validation
- validation pipeline behavior
- general validator behavior

Mathematical validation is especially important because educational scripts can contain equations, formulas, substitutions, calculations, units, and mathematical reasoning.

The intended generation loop is:

```text
Generate
   |
   v
Validate
   |
   +---- PASS ----> Final script
   |
   +---- FAIL ----> Regenerate with validation feedback
```

Validation will continue to become more rigorous as the project develops.

## API

TeachHinglish currently exposes a FastAPI application.

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Generate a Teaching Script

```http
POST /v1/teach
```

The endpoint accepts a `TeachingRequest` and returns a `TeachingResponse`.

## Example Request

```json
{
  "topic": "Newton's Second Law",
  "subject": "physics",
  "education_level": "class_11",
  "exam_goal": "jee",
  "language": "hinglish",
  "style": "conceptual"
}
```

Example response shape:

```json
{
  "topic": "Newton's Second Law",
  "subject": "physics",
  "education_level": "class_11",
  "exam_goal": "jee",
  "language": "hinglish",
  "style": "conceptual",
  "teaching_script": "..."
}
```

The generated script is the primary artifact intended for downstream lecture-generation software.

## Project Structure

```text
TeachHinglish/
|
+-- src/
|   +-- teachhinglish/
|       |
|       +-- api/
|       |   +-- app.py
|       |
|       +-- core/
|       |   +-- engine.py
|       |   +-- models.py
|       |   +-- settings.py
|       |
|       +-- graph/
|       |   +-- state.py
|       |   +-- workflow.py
|       |   +-- planner.py
|       |   +-- knowledge.py
|       |   +-- prompt.py
|       |   +-- teacher.py
|       |   +-- validator.py
|       |
|       +-- prompts/
|       |   +-- ...
|       |
|       +-- providers/
|       |   +-- base.py
|       |   +-- gemini.py
|       |   +-- gemini_key_resolver.py
|       |
|       +-- subjects/
|       |   +-- registry.py
|       |
|       +-- validation/
|           +-- ...
|
+-- tests/
|   +-- integration/
|   |   +-- test_api.py
|   |   +-- test_teaching_flow.py
|   |
|   +-- unit/
|       +-- ...
|
+-- pyproject.toml
+-- uv.lock
+-- README.md
```

## Technology Stack

- **Python 3.13+**
- **FastAPI** — HTTP API
- **Pydantic** — request/response models
- **LangGraph** — workflow orchestration
- **Google GenAI** — Gemini generation provider
- **SymPy** — mathematical expression support/validation
- **pytest** — testing
- **pytest-asyncio** — asynchronous tests
- **uv** — dependency and environment management

## Requirements

- Python `>= 3.13`
- `uv`
- Gemini API configuration for real LLM generation

## Development Setup

Clone the repository:

```powershell
git clone https://github.com/ambuj1211/TeachHinglish.git
cd TeachHinglish
```

Synchronize the environment:

```powershell
uv sync
```

Check Python:

```powershell
uv run python --version
```

## Running Tests

Run the complete suite:

```powershell
uv run pytest
```

Run API integration tests:

```powershell
uv run pytest tests/integration/test_api.py -v
```

Run the teaching-flow integration test:

```powershell
uv run pytest tests/integration/test_teaching_flow.py -v
```

## Running the API

Start the development server:

```powershell
uv run fastapi dev src/teachhinglish/api/app.py
```

Current endpoints:

```text
GET  /health
POST /v1/teach
```

## Design Principles

### 1. Script generation is the core responsibility

TeachHinglish generates lecture scripts. Final lecture/video generation belongs to downstream systems.

### 2. Domain independent

TeachHinglish must not become a JEE-only, GATE-only, or NEET-only engine.

The same engine should be reusable by any downstream educational application.

### 3. Subject aware

Different subjects require different teaching patterns. Physics, Mathematics, Chemistry, Biology, Computer Science, Digital Logic, History, and other supported subjects should not be treated as identical generation tasks.

### 4. Education-level aware

A Class 8 explanation and a GATE-level explanation may require different terminology, depth, examples, prerequisites, and pacing.

### 5. Validation first

Generated educational content must be checked instead of blindly accepting raw LLM output.

### 6. Downstream friendly

The script should eventually contain enough structure and semantic information for downstream lecture-generation systems to transform it into lectures without having to rediscover the teaching logic.

### 7. Extensible

New subjects, providers, validators, curricula, teaching styles, and downstream consumers should be possible without redesigning the entire engine.

### 8. Test before commit

Development follows:

```text
Implement
   |
   v
Run targeted tests
   |
   v
Run full test suite
   |
   v
Inspect Git diff
   |
   v
Commit
   |
   v
Push checkpoint
```

## Current Status

TeachHinglish is under active development.

The current foundation includes:

- FastAPI API
- request/response models
- 12 subject definitions
- multiple education levels
- language and teaching-style configuration
- Gemini provider infrastructure
- LangGraph-based teaching workflow
- planning stage
- knowledge/context stage
- prompt construction stage
- teaching/generation stage
- validation stage
- validation retry flow
- content validation
- structure validation
- topic coverage validation
- mathematics validation
- unit tests
- integration tests

The latest verified development checkpoint has the complete test suite passing.

Latest checkpoint:

```text
2e6a006 refactor: route teaching through graph workflow
```

Previous checkpoint:

```text
82e96e5 test: cover teach API endpoint
```

The project is not yet production-complete. The current implementation is the foundation for a universal lecture-script engine.

## Roadmap

### Phase 1 — Core Workflow Stabilization

- audit the complete LangGraph flow
- improve state contracts
- improve node boundaries
- improve error handling
- improve retry behavior
- keep provider abstraction clean

### Phase 2 — Lecture Script Contract

Define a stable, downstream-friendly lecture-script contract covering concepts such as:

```text
Lecture metadata
    |
Learning objectives
    |
Prerequisites
    |
Introduction
    |
Concept sequence
    |
Explanations
    |
Examples
    |
Equations / formulas
    |
Worked problems
    |
Common mistakes
    |
Exam / learning insights
    |
Summary
    |
Validation information
```

The exact schema will be designed around downstream lecture-generation requirements.

### Phase 3 — Generation Quality

Improve scripts so they are:

- coherent
- pedagogically ordered
- level appropriate
- subject appropriate
- naturally written
- useful for actual lecture delivery
- consistent with the requested teaching style

### Phase 4 — Domain-Aware Teaching

Strengthen subject-specific generation behavior across all 12 supported subject domains.

### Phase 5 — Correctness and Validation Loop

Expand validation to detect:

- factual inconsistencies
- incorrect mathematical reasoning
- incorrect substitutions
- arithmetic errors
- unit inconsistencies
- contradictory statements
- missing topic coverage
- structural problems
- unsupported claims

Validation failures should provide actionable feedback to the generation stage.

### Phase 6 — Evaluation Framework

Build a representative evaluation dataset across the 12 supported subjects and multiple education levels.

Evaluate:

- factual correctness
- mathematical correctness
- topic coverage
- educational clarity
- structure
- language quality
- Hinglish quality
- level appropriateness
- exam/learning-goal alignment
- consistency

Automated tests are necessary, but they are not sufficient to prove educational quality. A dedicated evaluation framework is therefore part of the roadmap.

### Phase 7 — Production Hardening

- API error handling
- provider failures and retries
- timeout handling
- rate-limit handling
- structured logging
- observability
- configuration management
- performance improvements
- security
- deployment configuration
- stable API contracts

### Phase 8 — Downstream Integration

Provide stable interfaces for downstream applications such as:

- JEE lecture-generation systems
- GATE lecture-generation systems
- NEET lecture-generation systems
- school-learning systems
- B.Tech/M.Tech educational systems
- university lecture systems
- professional education systems
- future educational products

The downstream application determines how the generated script is converted into a final lecture.

## Contributing

When making changes:

1. Keep universal lecture-script generation as the core responsibility.
2. Avoid coupling core functionality to a single examination.
3. Add or update tests with implementation changes.
4. Run targeted tests.
5. Run the complete test suite before creating a checkpoint.
6. Review the Git diff before committing.
7. Use focused Git commits for meaningful milestones.

Example:

```powershell
uv run pytest
git status
git --no-pager diff
git add <files>
git commit -m "..."
git push origin main
```

## License

License information will be added when the project license is finalized.
