# TeachHinglish

> Universal AI-powered lecture script generation engine for downstream lecture-generation systems.

TeachHinglish is a **lecture script generation engine**, not a video-generation system.

It generates subject-aware, education-level-aware teaching scripts that can be consumed by downstream lecture/video generation software. A JEE, GATE, NEET, school, B.Tech, M.Tech, university, or professional-learning application can use TeachHinglish as its **script-generation layer**.

---

## What TeachHinglish Does

TeachHinglish accepts a teaching request containing:

- topic
- subject
- education level
- exam or learning goal
- language
- teaching style

The request is processed through a graph-based teaching workflow:

```text
Teaching Request
      |
      v
   Planner
      |
      v
   Knowledge
      |
      v
    Prompt
      |
      v
   Teacher / LLM
      |
      v
   Validator
      |
      +---- PASS ----> Teaching Script
      |
      +---- FAIL ----> Retry Generation
```

The current implementation uses LangGraph for workflow orchestration.

### Current capabilities

- structured teaching planning
- subject-aware teaching guidance
- education-level-aware generation
- English, Hindi, and Hinglish support
- configurable teaching style
- Gemini-based LLM generation
- content validation
- structure validation
- topic coverage validation
- mathematical validation
- validation retry flow
- FastAPI HTTP API

The current repository has a verified test suite covering these components.

---

# What TeachHinglish Does Not Do

TeachHinglish intentionally stops at **validated teaching-script generation**.

It does not currently perform:

- video generation
- avatar generation
- text-to-speech
- voice cloning
- lip synchronization
- animation rendering
- Manim rendering
- slide rendering
- subtitle rendering
- video editing
- FFmpeg composition
- final MP4 generation

Those responsibilities belong to the downstream lecture/video generation application.

This separation is intentional.

---

# Supported Subjects

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

Subjects are deliberately independent of examinations.

For example:

- `physics` can be used for Class 11, Class 12, JEE, NEET, or general learning.
- `computer_science` can be used for B.Tech, M.Tech, GATE, university, or professional learning.
- `digital_logic` can be used for B.Tech, GATE, or other engineering education.

---

# Supported Education Levels

```text
class_6
class_7
class_8
class_9
class_10
class_11
class_12

jee
neet
gate

btech
mtech
university
professional
general
```

`exam_goal` is free-form and can contain values such as:

```text
jee
neet
gate
board examination
semester examination
competitive examination
conceptual understanding
interview preparation
advanced learning
```

---

# Languages

Supported languages:

| Language | Identifier |
|---|---|
| Hinglish | `hinglish` |
| Hindi | `hindi` |
| English | `english` |

Default:

```text
hinglish
```

Hinglish generation is designed to use natural Hindi-English mixing while preserving technical terminology, formulas, equations, units, and code accurately.

---

# Teaching Styles

| Style | Identifier |
|---|---|
| Conceptual | `conceptual` |
| Exam-focused | `exam_focused` |
| Deep theory | `deep_theory` |
| Conversational | `conversational` |

---

# Subject-Aware Teaching

TeachHinglish does not treat every subject identically.

Each subject has a subject profile containing:

- display name
- subject description
- teaching approach
- required teaching elements

For example, Physics can emphasize:

```text
concepts
physical intuition
laws
derivations
formulas
numerical problem solving
assumptions and conditions
common mistakes
```

Mathematics can emphasize mathematical reasoning, formulas, proofs, and problem solving.

History can emphasize chronology, causes, consequences, and historical relationships.

Computer Science can emphasize algorithms, systems, implementation concepts, examples, and technical reasoning.

This subject-specific guidance is injected into the teaching prompt before LLM generation.

---

# Teaching Workflow

The current graph contains these stages:

## 1. Planner

Creates a structured teaching plan containing:

- learning objectives
- prerequisites
- concepts
- examples
- teaching sequence

The planner is subject-aware and uses the subject registry to guide the plan.

## 2. Knowledge

Loads subject/context information required for generation.

## 3. Prompt

Builds the final teaching prompt using:

- student profile
- subject profile
- subject context
- structured teaching plan
- opening style
- teaching requirements

## 4. Teacher

Uses the configured LLM provider to generate the teaching script.

The current provider infrastructure supports Gemini.

## 5. Validator

Validates the generated script.

Current validation includes:

- basic/content validation
- structure validation
- topic coverage validation
- mathematical validation
- validation pipeline behavior

## 6. Retry

When validation fails, the workflow can regenerate the script subject to the configured retry limit.

The goal is:

```text
Generate
   |
   v
Validate
   |
   +---- PASS ----> Final Script
   |
   +---- FAIL ----> Regenerate
```

---

# API

TeachHinglish exposes a FastAPI application.

Current public HTTP endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health/readiness check |
| `POST` | `/v1/teach` | Generate a teaching script |

The FastAPI application also exposes the standard interactive API documentation generated by FastAPI when the server is running.

---

## API Base URL

For local development:

```text
http://127.0.0.1:8000
```

Therefore:

```text
GET  http://127.0.0.1:8000/health
POST http://127.0.0.1:8000/v1/teach
```

---

# API: Health Check

## Request

```http
GET /health
```

## Response

```json
{
  "status": "ok"
}
```

Example PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/health" `
  -Method Get
```

Expected result:

```text
status
------
ok
```

This endpoint can be used by the downstream lecture-generation application to verify that TeachHinglish is running before submitting a lecture-generation job.

---

# API: Generate Teaching Script

## Request

```http
POST /v1/teach
Content-Type: application/json
```

The request body is a `TeachingRequest`.

## Request Schema

```json
{
  "topic": "string",
  "subject": "physics",
  "education_level": "class_11",
  "exam_goal": "string or null",
  "language": "hinglish",
  "style": "conceptual"
}
```

### Fields

| Field | Required | Description |
|---|---|---|
| `topic` | Yes | Topic to teach. 1–500 characters. |
| `subject` | Yes | One of the supported subject identifiers. |
| `education_level` | Yes | Target learner level. |
| `exam_goal` | No | Examination or learning objective. |
| `language` | No | `hinglish`, `hindi`, or `english`. Defaults to `hinglish`. |
| `style` | No | Teaching style. Defaults to `conceptual`. |

---

## Example: JEE Physics

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

## Example: GATE Computer Science

```json
{
  "topic": "Binary Search Tree",
  "subject": "computer_science",
  "education_level": "gate",
  "exam_goal": "gate",
  "language": "hinglish",
  "style": "exam_focused"
}
```

## Example: B.Tech Digital Logic

```json
{
  "topic": "Boolean Algebra",
  "subject": "digital_logic",
  "education_level": "btech",
  "exam_goal": "semester examination",
  "language": "english",
  "style": "deep_theory"
}
```

---

# API Response

The endpoint returns a `TeachingResponse`.

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

The `teaching_script` is the primary artifact that should be passed to downstream lecture-generation software.

---

# API Error Handling

FastAPI/Pydantic validates incoming requests.

Invalid values for enumerated fields such as:

```text
subject
education_level
language
style
```

will be rejected by request validation.

An invalid request should therefore be treated as a request/input error by the downstream application.

Provider failures, timeouts, rate limits, and production-grade API error handling are still part of the hardening roadmap.

---

# Interactive API Documentation

After starting the API, FastAPI provides interactive documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema is available at:

```text
http://127.0.0.1:8000/openapi.json
```

The `/docs` page can be used to manually test `/health` and `/v1/teach`.

---

# Using TeachHinglish in Lecture Video Generation Software

TeachHinglish is designed to sit **before** the video-generation pipeline.

A downstream lecture-generation system can use this architecture:

```text
                 DOWNSTREAM LECTURE SYSTEM
                 =========================

User / Job
    |
    | topic + subject + level + goal
    v
+----------------------+
| TeachHinglish        |
| Script Generation    |
+----------+-----------+
           |
           | validated teaching_script
           v
+----------------------+
| Lecture Parser /     |
| Script Processor     |
+----------+-----------+
           |
           v
+----------------------+
| Storyboard Generator |
+----------+-----------+
           |
           +------------------+
           |                  |
           v                  v
     Teacher / Voice      Visuals / Slides
           |                  |
           +--------+---------+
                    |
                    v
             Video Composition
                    |
                    v
                Final MP4
```

The important boundary is:

```text
TeachHinglish
      |
      | validated educational script
      v
Lecture Video Generator
```

TeachHinglish should not need to know whether the downstream application uses:

- an avatar
- a real teacher image
- text-to-speech
- voice cloning
- Manim
- PowerPoint
- HTML slides
- a whiteboard
- animation
- FFmpeg
- another video engine

---

# Recommended Downstream Integration

A lecture-generation application should create a lecture job containing at least:

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

Then submit the request to:

```text
POST /v1/teach
```

The downstream application receives:

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

The downstream system then stores the script and continues with its own pipeline.

---

# Example Downstream Pipeline

For a complete lecture/video generation system:

```text
1. User selects topic
        |
        v
2. Create lecture job
        |
        v
3. POST /v1/teach
        |
        v
4. Receive teaching_script
        |
        v
5. Save approved script
        |
        v
6. Parse script into lecture sections
        |
        v
7. Generate storyboard
        |
        +-------------------+
        |                   |
        v                   v
   Voice generation     Visual generation
        |                   |
        +---------+---------+
                  |
                  v
           Teacher/avatar
                  |
                  v
            Composition
                  |
                  v
              Subtitles
                  |
                  v
              Final MP4
```

---

# Why the Separation Matters

The downstream video system should not ask an LLM again:

> "How should Newton's Second Law be taught?"

TeachHinglish should already make that educational decision.

The downstream system should instead ask:

> "How do I visually and audibly render this approved teaching script?"

This creates a clean separation:

| Responsibility | TeachHinglish | Downstream Video System |
|---|---:|---:|
| Understand teaching request | Yes | No |
| Subject-aware planning | Yes | No |
| Education-level adaptation | Yes | No |
| Teaching sequence | Yes | No |
| Teaching script | Yes | No |
| Content validation | Yes | No |
| Mathematical validation | Yes | No |
| Storyboard rendering | No | Yes |
| Voice generation | No | Yes |
| Avatar/lip sync | No | Yes |
| Animation | No | Yes |
| Slides | No | Yes |
| Video composition | No | Yes |
| Final MP4 | No | Yes |

---

# Example Integration Code

A downstream Python application can call TeachHinglish using HTTP.

```python
import requests

request = {
    "topic": "Newton's Second Law",
    "subject": "physics",
    "education_level": "class_11",
    "exam_goal": "jee",
    "language": "hinglish",
    "style": "conceptual",
}

response = requests.post(
    "http://127.0.0.1:8000/v1/teach",
    json=request,
    timeout=300,
)

response.raise_for_status()

lecture = response.json()

script = lecture["teaching_script"]

print(script)
```

The downstream application can then pass `script` to its storyboard, voice, animation, and video-generation stages.

---

# Example PowerShell Integration

```powershell
$body = @{
    topic = "Newton's Second Law"
    subject = "physics"
    education_level = "class_11"
    exam_goal = "jee"
    language = "hinglish"
    style = "conceptual"
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/v1/teach" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$response.teaching_script
```

---

# Running TeachHinglish

## Requirements

- Python `>= 3.13`
- `uv`
- Gemini API configuration for real LLM generation

## Clone

```powershell
git clone https://github.com/ambuj1211/TeachHinglish.git
cd TeachHinglish
```

## Install

```powershell
uv sync
```

## Check Python

```powershell
uv run python --version
```

## Start API

```powershell
uv run fastapi dev src/teachhinglish/api/app.py
```

The API is then available at:

```text
http://127.0.0.1:8000
```

---

# API Tests

Run API integration tests:

```powershell
uv run pytest tests/integration/test_api.py -v
```

Run the complete test suite:

```powershell
uv run pytest
```

---

# Project Structure

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
|       |   +-- base.py
|       |   +-- teaching.py
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
|   +-- unit/
|
+-- pyproject.toml
+-- uv.lock
+-- README.md
```

---

# Technology Stack

- **Python 3.13+**
- **FastAPI** — HTTP API
- **Pydantic** — request/response models
- **LangGraph** — workflow orchestration
- **Google GenAI** — Gemini provider
- **SymPy** — mathematical expression support and validation
- **pytest** — testing
- **pytest-asyncio** — asynchronous testing
- **uv** — dependency and environment management

---

# Current Status

TeachHinglish is under active development.

The current foundation includes:

- FastAPI API
- request/response models
- 12 subject definitions
- multiple education levels
- language configuration
- teaching-style configuration
- subject-specific teaching profiles
- structured teaching planner
- knowledge/context stage
- prompt construction
- Gemini provider infrastructure
- LangGraph workflow
- teaching-script generation
- content validation
- structure validation
- topic coverage validation
- mathematical validation
- validation retry flow
- unit tests
- integration tests

The current development checkpoint has a verified full test suite.

At the latest checkpoint, the repository's complete suite contains **92 passing tests**.

TeachHinglish is usable as a **development-stage script-generation service** for a lecture video-generation application, but it is not yet a production-hardened service.

---

# Roadmap

## Phase 1 — Core Workflow Stabilization

- improve state contracts
- improve node boundaries
- improve error handling
- improve retry behavior
- keep provider abstraction clean

## Phase 2 — Lecture Script Contract

Develop a stable downstream-friendly lecture representation containing concepts such as:

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

The current `/v1/teach` response still returns the teaching script as a single string.

## Phase 3 — Generation Quality

Improve:

- coherence
- pedagogy
- level appropriateness
- subject appropriateness
- teaching style adherence
- lecture pacing
- natural spoken language
- exam alignment

## Phase 4 — Domain-Aware Teaching

Strengthen teaching behavior across all supported subject domains.

## Phase 5 — Correctness and Validation

Expand validation to detect:

- factual inconsistencies
- incorrect mathematical reasoning
- incorrect substitutions
- arithmetic errors
- unit inconsistencies
- contradictory statements
- missing topic coverage
- unsupported claims
- structural problems

## Phase 6 — Evaluation Framework

Build a representative evaluation dataset across:

- all supported subjects
- multiple education levels
- multiple teaching styles
- English
- Hindi
- Hinglish
- exam-focused use cases

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

Automated tests alone are not sufficient to prove educational quality.

## Phase 7 — Production Hardening

- authentication
- API error handling
- provider failures
- retries
- timeout handling
- rate-limit handling
- structured logging
- observability
- configuration management
- performance improvements
- security
- deployment configuration
- stable API contracts

## Phase 8 — Downstream Integration

Provide stable interfaces for:

- JEE lecture-generation systems
- GATE lecture-generation systems
- NEET lecture-generation systems
- school-learning systems
- B.Tech/M.Tech educational systems
- university lecture systems
- professional education systems

---

# Design Principles

### 1. Script generation is the core responsibility

TeachHinglish generates educational scripts.

Final lecture/video generation belongs to downstream systems.

### 2. Domain independent

The engine must not become permanently coupled to JEE, GATE, NEET, or any single examination.

### 3. Subject aware

Different subjects require different teaching approaches.

### 4. Education-level aware

A Class 8 explanation and a GATE explanation should not use the same depth, terminology, prerequisites, or examples.

### 5. Validation first

Generated educational content should be validated instead of blindly accepting raw LLM output.

### 6. Downstream friendly

The output should eventually contain enough semantic structure for downstream systems to render lectures without rediscovering the teaching logic.

### 7. Extensible

New subjects, providers, validators, curricula, teaching styles, and consumers should be possible without redesigning the engine.

---

# Development Workflow

Before creating a checkpoint:

```powershell
uv run pytest
git status
git --no-pager diff --check
git --no-pager diff
git add <files>
git commit -m "..."
git push origin main
```

Focused commits are preferred for meaningful milestones.

---

# Important Production Note

The current API is suitable for integrating and testing the **script-generation stage** of a lecture-generation system.

For production deployment, the API should first receive stronger:

- authentication
- request limits
- timeout handling
- provider failure handling
- structured error responses
- observability
- stable versioning
- deployment configuration

Therefore:

```text
Current stage
    |
    v
Development / integration use
    |
    v
Not yet production-hardened
```

---

# License

License information will be added when the project license is finalized.
