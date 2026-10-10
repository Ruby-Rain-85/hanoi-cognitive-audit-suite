# PIL Experiment Metadata | Blank Template v2.0

> **Template status:** Blank, reusable research record. Fill only from documented evidence. Use `Pending`, `Not measured`, `Not applicable`, or `Unknown` rather than assuming a result. Preserve prior metadata and raw artifacts unchanged.

## 1. Experiment identification and verification status

- **Experiment ID:**
- **Experiment title:**
- **Metadata version:** 2.0
- **Metadata author / last updated:**
- **Experiment status:**
- **Raw transcript status:** [ ] Complete  [ ] Partial  [ ] Uncertain
- **Move sequence status:** [ ] Not extracted  [ ] Extracted, unverified  [ ] Human reviewed  [ ] Programmatically verified
- **Final state status:**
- **Token measurement status:**
- **Behavioral annotation status:**
- **Evidence / verification notes:**

## 2. Basic information and task description

- **Model / exact variant as reported:**
- **Platform / interface:**
- **Model version or snapshot (if available):**
- **Experiment date / timezone / date confidence:**
- **Session type:** Single prompt / Multi-turn
- **Task name:** Tower of Hanoi
- **Number of disks (n):**
- **Initial board (top-to-bottom):** Peg 1 = [ ]; Peg 2 = [ ]; Peg 3 = [ ]
- **Target board (top-to-bottom):** Peg 1 = [ ]; Peg 2 = [ ]; Peg 3 = [ ]
- **Expected optimal moves (2^n - 1):**
- **Rule set / deviations from classical rules:**
- **Success criterion specified to model:**

## 3. Conversation context

- **Prior conversation before solution?:**
- **Description of prior context:**
- **Context length method:**
- **Character count:**
- **Estimated / measured context tokens:**
- **Known truncation, omissions, or export issues:**
- **Potential context confounders:**

## 4. Prompt information and experimental conditions

- **Trigger prompt location (file/page/line/turn):**
- **Prompt text artifact / hash:**
- **Prompt style:** Informal / Semi-structured / Structured
- **Instruction set:**
- **Batch size / output formatting requested:**
- **Explicit state reporting required?:**
- **Self-verification requested?:**
- **External verifier feedback supplied?:**
- **Other interventions during session:**
- **Prompt condition ID (for future controlled trials):**

## 5. Response information and instruction adherence

- **Full solution produced?:**
- **Move sequence present?:**
- **Reasoning / explanation included?:**
- **Step-by-step response?:**
- **Model-claimed move total:**
- **Extracted numbered move entries:**
- **Unique sequential move numbers:**
- **Missing / duplicate / restarted move numbers:**
- **Claimed completion / correctness statement (quote + location):**
- **Instruction adherence observations (batching, format, constraints):**
- **Observed interruptions / user corrections:**

## 6. Ground-truth verifier results

> **Current `verify_hanoi.py` outputs:** move legality, failure reasons, move-number checks, human-verdict agreement (optional), visual-state MATCH/DRIFT/INVALID/UNCHECKED (optional), goal reached, legal complete solve, optimal solve, and strict `Experiment Passed`. Preserve these as separate fields. The verifier rejects illegal moves without changing its simulated board.

- **Verifier filename / version / Git commit SHA:**
- **Verification run date:**
- **Input workbook / worksheet / SHA-256:**
- **Output verified workbook / SHA-256:**
- **Disk-count argument:**
- **Sequence / branch audited:**
- **Replay policy:** Reject illegal moves; retain last accepted state (current verifier)
- **Rows analyzed:**
- **Expected optimal move count:**
- **Illegal moves detected:**
- **First rejected move (row, move label, failure reason):**
- **Move-number errors:**
- **Goal reached on Peg 3?:**
- **Legal complete solve?:**
- **Optimal solve?:**
- **Experiment Passed?:**
- **Human-check discrepancies (if column present):**
- **Visual peg alignment: MATCH / DRIFT / INVALID / UNCHECKED counts:**
- **First visual DRIFT (row, move label):**
- **First visual INVALID (row, move label):**
- **Final simulated board (top-to-bottom):**
- **Important distinction:** `Experiment Passed` is a strict composite outcome; do not use it as a substitute for legality, goal, optimality, or state-report accuracy.
- **Validation limitations / unresolved cases:**

## 7. State-space tracking analysis

> **Analysis layer:** Some fields below require postprocessing or extensions to the current verifier; mark `Not measured` until implemented.

- **First physical move violation:**
- **First claimed-state divergence:**
- **State divergence duration (definition / measured value):**
- **Consecutive state-report mismatches:**
- **Legal move rate (denominator and branch scope stated):**
- **Visual-state agreement rate (exclude or report UNCHECKED explicitly):**
- **State divergence preceding move error?:**
- **Post-error state reconstruction notes:**
- **Unobserved / missing states:**
- **Evidence locations:**

## 8. Token usage and accuracy

> **Pending tokenizer implementation.** Token counts from a visible transcript are not automatically equivalent to API-billed tokens or hidden reasoning usage.

- **Tokenizer script / version / Git commit:**
- **Tokenizer encoding / model mapping:**
- **Source text / extraction method:**
- **Counting boundaries and role/message overhead assumptions:**
- **Full visible conversation tokens:**
- **Pre-solution context tokens:**
- **Trigger prompt tokens:**
- **Solution segment tokens:**
- **Tokens before first verified error:**
- **Tokens in recovery episodes:**
- **Tokens per accepted legal move (formula / denominator):**
- **Tokens per completed solution (if applicable):**
- **Accuracy metric paired with token usage:**
- **Limitations / comparability notes:**

## 9. Confidence, self-detection, and correction behavior

> **Behavioral coding requires transcript evidence.** Do not equate certainty language with calibrated probability, or error acknowledgment with successful correction.

- **Correctness / completion claims (exact quote and source location):**
- **Claim verified, contradicted, or indeterminate?:**
- **Confidence language coding rule / category:**
- **Self-detected error?:**
- **First model-acknowledged error (move reference / transcript location):**
- **First independently verified error:**
- **Detection latency (defined in moves or turns):**
- **User-prompted versus spontaneous detection:**
- **Correction attempted?:**
- **Correction verified successful?:**
- **Repeated unsupported correctness claims?:**
- **Alternative interpretations / annotation uncertainty:**

## 10. Heuristic drift and instruction drift

> **Separate constructs:** state-description drift, move-strategy deviation, and instruction/format drift. A single illegal move does not by itself establish heuristic drift.

- **Operational definition used:**
- **Baseline strategy / instructions:**
- **First observable deviation and evidence:**
- **Pattern or persistence of deviation:**
- **State-report drift observed?:**
- **Strategy deviation observed?:**
- **Batch-size / format instruction drift observed?:**
- **Possible confounders:**
- **Coding status:** Not measured / Annotated / Independently reviewed

## 11. Branch and recovery episode register

> **One PIL experiment, multiple labeled branches.** Branches are not independent experimental replicates. A correction must specify whether it replaces earlier moves, resumes from an accepted state, or starts from a reset state.

| Branch ID | Parent / fork point | Transcript location | Starting state source | Move range | Intervention / reason | Verification artifact | Outcome |
|---|---|---|---|---|---|---|---|
| PIL-___-B00 | Original sequence | | | | Initial attempt | | |
| PIL-___-B01 | | | | | | | |

- **Number of branches / correction episodes:**
- **Rules for assigning entries to branches:**
- **Ambiguous or overlapping move labels:**
- **Within-branch token counts / legality / state agreement:**
- **Cross-branch conclusions (with dependence caveat):**

## 12. Observations, interpretations, and limitations

### Direct observations (quote or point to evidence)

-

### Verifier-supported findings

-

### Research interpretations / hypotheses (not established facts)

-

### Alternative explanations and confounders

-

### Known issues / limitations

- [ ] Missing moves or incomplete transcript checked
- [ ] Extraction / transcription integrity checked
- [ ] Branch boundaries reviewed
- [ ] Verifier negative tests completed
- [ ] Token counts reproduced
- [ ] Behavioral coding independently reviewed
- **Additional notes:**

## 13. Artifacts and reproducibility

- **Full conversation transcript:**
- **Prompt file:**
- **Response / move extraction file:**
- **Raw move workbook:**
- **Verified workbook:**
- **Diagram / visuals:**
- **Verifier script / commit:**
- **Tokenizer script / commit:**
- **Behavioral annotation / branch register:**
- **README / methodology reference:**
- **File integrity hashes (where available):**
- **Reproduction command / environment:**
- **Metadata revision history:**

## 14. Future iterations: planned improvements (not current capabilities)

### Verifier improvements

- [ ] Compare reported peg states against the **unchanged accepted state even on rejected moves**; preserve a distinct `UNCHECKED` status only when comparison is genuinely impossible.
- [ ] Record **pre-move and post-move simulated states** for every row to support error tracing.
- [ ] Export **first-error locations**, per-reason counts, and state-divergence runs automatically.
- [ ] Review rule-check precedence (including **same-source-and-destination** cases) so reported failure reasons are consistent and meaningful.
- [ ] Build **branch-aware transcript extraction** to distinguish corrections, resets, and duplicated move labels; never merge overlapping branches into one continuous run.
- [ ] Run systematic **negative tests** for malformed identifiers, illegal moves, malformed visual lists, skipped numbering, missing columns, and edge cases.
- [ ] Consider explicit schema validation for reported boards: disk uniqueness, expected disk set, and descending size order, distinct from mismatch with ground truth.

### Tokenizer improvements

- [ ] Implement reproducible visible-text token counts, document tokenizer version and encoding.
- [ ] Count **prompt, context, solution, and correction episode** segments separately.
- [ ] Report denominators and avoid treating exported text counts as exact model-internal usage.

### Behavioral and experimental-design improvements

- [ ] Define a reproducible **confidence-claim annotation rubric**, with transcript quotes and independent review.
- [ ] Operationalize **self-detection latency**, **recovery success**, **state divergence duration**, and **heuristic / instruction drift**.
- [ ] Compare prompting interventions under controlled conditions with **disk count, model version, context, and evaluation method held fixed** where possible.
- [ ] Separate **task-complexity studies** (vary disks, hold prompt fixed) from **prompt-intervention studies** (hold task fixed, vary prompt).
- [ ] Use repeated trials and report variation; treat exploratory pilots as historical case studies rather than controlled replicates.

### Decision log

- **Priority / owner / target iteration:**
- **Change implemented / commit / date:**
- **Effect on comparability with earlier PIL records:**

---

**Research objectives:** (1) State-space tracking, (2) token usage versus accuracy, (3) confidence claims, prompting interventions, and heuristic/instruction drift. Keep *observations*, *model claims*, *programmatic measurements*, and *interpretations* distinct.