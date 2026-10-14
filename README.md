# Hanoi Cognitive Audit Suite

### Benchmarking Recursive Planning and State-Space Integrity in Large Language Models

A deterministic benchmarking and validation framework for evaluating Large Language Model (LLM) performance on recursive planning, long-horizon state tracking, and constraint adherence using the Tower of Hanoi problem.

The project combines structured model-generated move sequences, an independent Python verification engine, reproducible negative testing, and human auditing.

Its central objective is to distinguish **successful text generation from demonstrably valid state-space execution**.

---

## 1. Project Inspiration and Research Motivation

This project emerged from research into the limitations of symbolic and mathematical reasoning in large language models, including Apple's 2024 *GSM-Symbolic* work and its 2025 paper, *The Illusion of Thinking*.

These studies raised questions about the reliability of model reasoning as task complexity increases. The Tower of Hanoi offers a useful experimental environment because its rules, state transitions, and optimal solution length are mathematically defined.

Initial exploratory experiments involving GPT-4o and Claude Sonnet motivated further investigation into recursive planning, constraint adherence, and long-horizon state consistency.

For an eight-disk Tower of Hanoi puzzle, an optimal solution requires 255 moves. Each move changes the puzzle's state and constrains which subsequent moves are legal.

To make these sequences auditable, model output was structured into spreadsheet-based transition logs containing move identifiers, disk movements, and reported peg configurations.

Manual review helped establish the initial research workflow but introduced practical limitations in scalability and reproducibility. This motivated the development of an independent Python verification engine.

**Central research question:**

> How reliably can large language models generate legal, state-consistent solutions to recursive planning problems, and what patterns emerge when their reported actions or state representations diverge from deterministic ground truth?

The project evaluates observable model behavior. It does not claim to establish whether a model possesses an explicit internal representation of the puzzle.

---

## 2. Theoretical Background and Complexity Invariants

The Tower of Hanoi is a classical problem involving recursion, state-space search, and mathematical induction.

### Optimal Move Bound

For a puzzle containing `n` disks, the minimum number of moves is defined recursively:

$$
M(n) = 2M(n-1) + 1
$$

With the base case $M(0)=0$, the closed-form solution is:

$$
M(n) = 2^n - 1
$$

For the primary eight-disk experiment:

$$
M(8) = 2^8 - 1 = 255
$$

### Physical Game Invariants

1. Only one disk may be moved per transition.
2. Only the top disk of a source peg may be moved.
3. A larger disk may never be placed on a smaller disk.
4. Source and destination pegs must be different.
5. All peg identifiers must reference valid pegs.
6. Every disk must remain represented exactly once in the authoritative puzzle state.

A legal move sequence is not necessarily optimal. The verification framework therefore distinguishes move legality, goal completion, and optimality.

---

## 3. Architecture and Verification Engine

The project uses two primary Python components:

- `verify_hanoi.py`: An independent move and state verification engine.
- `create_corrupt_sheet.py`: A reproducible generator for deliberately corrupted Hanoi sequences.

### 3.1 Independent State Verification

The verifier maintains its own authoritative representation of the Tower of Hanoi board.

It does not trust model-reported peg configurations when deciding whether to execute a move.

The verification process follows these stages:

**1. State initialization**

Peg 1 is initialized with disks numbered from `1` (smallest) through `n` (largest). Pegs 2 and 3 begin empty.

The authoritative board representation stores the top disk at index `0`.

**2. Action ingestion**

The verifier reads spreadsheet columns including:

- `Move #`
- `Disk`
- `From`
- `To`

It can also evaluate reported peg configurations and optional human annotations.

**3. Constraint validation**

The engine evaluates move identifiers, peg validity, source occupancy, disk identity, and disk-size ordering.

**4. State transition**

Legal moves update the authoritative board through list operations.

Illegal moves are rejected without modifying the authoritative board.

**5. Visual state validation**

The verifier independently parses the reported contents of `Peg 1`, `Peg 2`, and `Peg 3`.

It compares these representations against the authoritative state after each attempted move.

The visual classification is independent of the move's legality.

| Classification | Meaning |
|---|---|
| `MATCH` | Reported peg configuration matches the authoritative board. |
| `DRIFT` | Reported configuration can be parsed but differs from the authoritative board. |
| `INVALID` | Reported peg configuration cannot be parsed successfully. |

For rejected moves, the visual representation is evaluated against the unchanged authoritative board.

This distinction allows the framework to identify cases where a model makes an illegal move but still reports the correct puzzle state, as well as cases where both its action and state representation are incorrect.

**6. Human baseline reconciliation**

When a `Human Check` column is present, the verifier compares the programmatic legality verdict with the human annotation.

Disagreements are reported separately from visual state discrepancies.

**7. Experiment-level evaluation**

The verifier reports metrics including:

- Total moves analyzed
- Illegal moves detected
- Move-number errors
- Goal completion
- Legal complete solve
- Optimal solve
- Discrepancies against human annotations
- Visual state alignment classifications

---

## 4. Negative Testing and Fault Injection

The `create_corrupt_sheet.py` module generates controlled violations of Tower of Hanoi constraints.

The purpose of negative testing is to determine whether the verifier correctly identifies known errors, rather than simply confirming valid solutions.

### 4.1 Fault Categories

The generator currently supports eight targeted fault categories.

| Fault category | Intended behavior |
|---|---|
| Malformed Data | Reject a non-integer move identifier. |
| Invalid Peg ID | Reject a move involving a nonexistent peg. |
| Empty Source Peg | Reject a move from an empty peg. |
| Ghost Disk | Reject a move claiming a disk that is not on top of the source peg. |
| Size Inversion | Reject placement of a larger disk on a smaller disk. |
| Identical Pegs | Reject a move with identical source and destination pegs. |
| Visual Drift | Detect a mismatch between reported and authoritative board states. |
| Human Discrepancy | Identify disagreement between a human annotation and the programmatic verdict. |

Fault placement uses a configurable random seed and eligibility checks to support reproducible experiments.

### 4.2 Authoritative State Preservation

A central requirement of the negative-test generator is that rejected moves must not alter the authoritative puzzle state.

This prevents an injected illegal move from unintentionally corrupting subsequent reference transitions.

The generator distinguishes between an attempted move and an executed legal transition.

### 4.3 Human-Audited Test Fixtures

The repository preserves generated negative-test inputs, verifier outputs, and separately annotated human-audited versions.

Original files and human-audited files are retained independently to preserve research provenance.

Human-audited workbooks may contain annotations or additional review information not present in the original generated files.

---

## 5. Validation Results and Regression Testing

### 5.1 Eight-Disk Baseline

A human-checked GPT-4o eight-disk sequence was evaluated using the deterministic verifier.

The recorded validation results were:

| Measurement | Result |
|---|---|
| Total moves | 255 |
| Optimal move target | 255 |
| Illegal moves | 0 |
| Move-number errors | 0 |
| Goal reached | True |
| Legal complete solve | True |
| Experiment passed | True |

These results establish that the audited sequence satisfied the verifier's evaluated conditions. They do not establish equivalent performance across other prompts, model runs, or model families.

### 5.2 Four-Disk Negative-Test Fixture

A controlled four-disk negative-test fixture was generated with seed `42`.

The resulting experiment contained 21 rows, including six rejected move attempts.

After improving the visual-validation logic, the verifier reported:

| Measurement | Result |
|---|---|
| Rows analyzed | 21 |
| Optimal move target | 15 |
| Illegal moves detected | 6 |
| Move-number errors | 0 |
| Goal reached | True |
| Legal complete solve | False |
| Optimal solve | False |
| Human discrepancies | 1 |
| Visual `MATCH` | 20 |
| Visual `DRIFT` | 1 |
| Visual `INVALID` | 0 |
| Visual `UNCHECKED` | 0 |
| Experiment passed | False |

The failed experiment verdict is expected because the dataset intentionally contains invalid moves and inconsistent annotations or visual states.

### 5.3 Rejected-Move Visual Drift Test

An additional test deliberately modified the reported visual state on an illegal move while preserving the attempted move itself.

The verifier produced:

| Measurement | Result |
|---|---|
| Illegal moves detected | 6 |
| Visual `MATCH` | 19 |
| Visual `DRIFT` | 2 |
| Visual `INVALID` | 0 |
| Visual `UNCHECKED` | 0 |

The targeted move retained its `Illegal` classification while receiving a `DRIFT` visual classification.

This confirms the tested behavior that move legality and reported visual accuracy are evaluated independently.

### 5.4 Automated Regression Test

The repository includes `tests/test_illegal_visual_alignment.py`.

The test uses Python's `unittest` framework to:

1. Load a preserved negative-test fixture.
2. Introduce a visual discrepancy on a rejected move.
3. Execute the actual verification program.
4. Inspect the resulting spreadsheet.
5. Assert that the move remains `Illegal` and its visual classification is `DRIFT`.

The test uses a temporary directory to avoid modifying preserved research fixtures.

**Current automated regression coverage:** One passing test for the `Illegal` + `DRIFT` combination.

Additional automated coverage is planned for `MATCH`, `INVALID`, and other rejection paths.

---

## 6. Repository Structure

The following structure documents the principal project components and research fixtures. Temporary development outputs are intentionally excluded.

```text
hanoi-cognitive-audit-suite/
├── LICENSE
├── PIL_Metadata_Template_v2
├── README.md
├── verify_hanoi.py
├── create_corrupt_sheet.py
├── hanoi_gpt4o_8disks.xlsx
├── hanoi_gpt4o_8disks_verified.xlsx
├── hanoi_gpt4o_8disks_human_checked.xlsx
├── hanoi_gpt4o_8disks_human_checked_verified.xlsx
└── tests/
    ├── test_illegal_visual_alignment.py
    └── fixtures/
        └── negative/
            ├── test_corrupt_hanoi.xlsx
            ├── test_corrupt_hanoi_human_audited.xlsx
            ├── verified_test_corrupt_hanoi.xlsx
            └── verified_test_corrupt_hanoi_human_audited.xlsx
```

This tree represents the principal known files rather than a newly verified exhaustive inventory of the repository.

---

## 7. Getting Started and Reproducibility

### Prerequisites

- Python 3.9 or newer
- `pandas`
- `openpyxl`

Install dependencies:

```bash
python -m pip install pandas openpyxl
```

Run commands from the repository root.

### Verify an Existing Hanoi Sequence

```bash
python verify_hanoi.py INPUT_FILE.xlsx OUTPUT_FILE.xlsx NUM_DISKS
```

For example:

```bash
python verify_hanoi.py \
  hanoi_gpt4o_8disks_human_checked.xlsx \
  verified_output.xlsx \
  8
```

### Generate a Negative-Test Fixture

```bash
python create_corrupt_sheet.py \
  -n 4 \
  -o test_corrupt_hanoi.xlsx \
  --seed 42
```

The seed allows the experiment to be reproduced using the same generator implementation and configuration.

### Verify the Generated Fixture

```bash
python verify_hanoi.py \
  test_corrupt_hanoi.xlsx \
  verified_corrupt_hanoi.xlsx \
  4
```

### Run the Automated Regression Test

```bash
python -m unittest discover \
  -s tests \
  -p "test_illegal_visual_alignment.py" \
  -v
```

The regression test operates on a temporary copy of the fixture and does not overwrite the preserved research data.

---

## 8. Development Progress and Future Improvements

### Implemented and Tested

- Deterministic Tower of Hanoi state verification
- Move legality and goal-state validation
- Optimal move-count evaluation
- Human-versus-programmatic verdict comparison
- Independent visual state comparison
- Visual validation on rejected moves
- Reproducible fault injection using a random seed
- Preservation of authoritative board state after illegal moves
- Human-audited negative-test fixtures
- Automated regression testing for visual drift on an illegal move

### Planned Verification Improvements

**1. Expand visual classification regression tests**

Add automated tests covering all three visual outcomes on rejected moves:

- `MATCH`: Illegal move with an accurate unchanged board representation
- `DRIFT`: Illegal move with an inaccurate but parseable board representation
- `INVALID`: Illegal move with malformed visual data

**2. Expand fault-specific assertions**

Automate verification that every generated fault type produces its intended classification and failure reason.

**3. Improve test coverage**

Run additional configurations using different disk counts, random seeds, and fault placements.

**4. Strengthen output consistency checks**

Assert that every input row receives exactly one programmatic verdict, failure reason, and applicable visual classification.

**5. Refine test artifact management**

Separate preserved research fixtures from temporary development outputs and maintain clear naming conventions.

**6. Review generator-verifier consistency**

Examine differences in validation order and failure-reason wording between the negative-test generator and the verification engine.

---

## 9. Multi-Iteration Research Roadmap

### Iteration 2: Multi-Model Comparative Benchmarking

Evaluate sequences generated by multiple model families under standardized experimental conditions.

Compare legality, state consistency, completion rates, and error distributions.

### Iteration 3: Heuristic Drift and Directional Bias Analysis

Investigate directional peg preferences and error patterns under alternative starting conditions and prompt structures.

Distinguish observed output preferences from claims about underlying model mechanisms.

### Iteration 4: In-Context Error Recovery

Provide models with controlled execution feedback and measure whether subsequent actions return to valid state-space trajectories.

Evaluate recovery using predefined metrics rather than relying solely on conversational self-correction.

### Iteration 5: Cross-Model Review Dynamics

Evaluate models acting as secondary reviewers of other models' move sequences.

Compare their judgments against the deterministic verification engine and independently reviewed experimental records.

---

## 10. Model Prompting Protocol for Experimental Replication

A standardized prompt format is used to encourage consistent move logs across model runs.

Experimental records should also preserve the model identifier, relevant settings, prompt version, and any human interventions.

### Baseline Prompt

```text
You are solving the Tower of Hanoi puzzle.

Solve the Tower of Hanoi puzzle for 8 disks.

Goal:
Move all 8 disks from Peg 1 to Peg 3 using Peg 2 as
 the auxiliary peg.

Formatting constraints:

1. Provide exactly seven columns with these headers:

   Move #, Disk, From, To, Peg 1, Peg 2, Peg 3

2. Disks are integers from 1 (smallest) to 8 (largest).

3. Peg identifiers must be integers: 1, 2, or 3.

4. Peg 1, Peg 2, and Peg 3 must report the complete
   configuration immediately after each attempted move.

5. Format disk lists as comma-separated integers
   inside brackets, ordered from top to bottom.

   Example: [1, 2, 3, 4, 5, 6, 7, 8]

6. An empty peg must be represented as [].

7. Output the complete optimal sequence without
   truncation.

8. Do not include explanatory text within the move log.
```

The top-to-bottom ordering matches the verifier's authoritative representation, in which index `0` is the top disk.

The exact prompt used for any experimental run should be preserved alongside its results. Changes to prompt wording or output requirements should be documented because they may affect comparability across runs.

---

## 11. Research Limitations

The framework provides deterministic evaluation of recorded actions and reported board states, but several limitations remain.

- A correct move sequence does not reveal how the model internally produced it.
- A single successful model run does not establish consistent reasoning performance.
- Structured output constraints may affect model behavior and should be treated as experimental variables.
- Human review remains valuable for auditing the verifier and identifying methodological errors.
- Current automated regression coverage does not exhaustively test every possible invalid input.
- Comparisons across models require controlled prompts, documented configurations, and consistent evaluation criteria.

These limitations inform the next stages of experimental design.

---

## 12. Project Status

**Current phase:** Deterministic verification, negative testing, and regression-test development.

The project has progressed from manually reviewed Tower of Hanoi sequences to a Python-based audit framework with controlled fault injection and independently validated visual state comparisons.

The next development priority is expanding automated coverage for the three visual outcomes and systematically testing all fault categories.

Future research will extend the framework to comparative model evaluation, state-recovery analysis, and cross-model auditing.
