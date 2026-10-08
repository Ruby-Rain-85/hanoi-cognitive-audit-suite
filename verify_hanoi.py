# Import pandas to parse and update Excel files
import pandas as pd
import sys
import re
# Construct filenames without splitting directory names or dotted stems.
from pathlib import Path

# Adds helper function to filter out invalid values before passing them
# to the rest of the code
def parse_integer(value, field_name):
    """Accept whole-number values without silently truncating fractions."""

    # A missing value cannot identify a move, disk, or peg.
    if pd.isna(value):
        raise ValueError(f"{field_name} is missing")

    # Booleans are not identifiers, even though Python treats True as 1.
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be an integer")

    # Convert the scalar to stripped text so Excel integers and floats
    # can be validated using the same rule.
    text = str(value).strip()

    # Accept integer text and decimal text containing only zeroes
    # after the decimal point. Reject fractions and unrelated text.
    if re.fullmatch(r"[+-]?\d+(?:\.0+)?", text) is None:
        raise ValueError(f"{field_name} must be an integer: {value!r}")

    # Remove the optional zero-only decimal portion after validation.
    integer_text = text.split(".", 1)[0]

    # Normalize the validated identifier to a Python integer.
    return int(integer_text)

# Improved def parse_peg_cell to ensure that only correct numerical
# values are used.
def parse_peg_cell(cell_val):
    """Parse a top-to-bottom disk list without repairing malformed text."""

    # Treat a blank spreadsheet cell as an empty peg.
    if pd.isna(cell_val):
        return []

    # Normalize surrounding whitespace.
    text = str(cell_val).strip()

    # Accept the explicit empty-peg formats.
    if text in ("", "[]"):
        return []

    # If either bracket appears, require a complete bracketed list.
    if text.startswith("[") or text.endswith("]"):
        if not (text.startswith("[") and text.endswith("]")):
            raise ValueError(f"Unbalanced peg brackets: {cell_val!r}")

        # Remove the outer brackets before parsing the contents.
        text = text[1:-1].strip()

        # Allow an empty bracketed list containing whitespace.
        if not text:
            return []

    # Require positive integer tokens separated by commas.
    # This rejects signs, fractions, words, and missing entries.
    if re.fullmatch(r"\d+(?:\s*,\s*\d+)*", text) is None:
        raise ValueError(f"Invalid peg list: {cell_val!r}")

    # Preserve the listed order, which represents top to bottom.
    disks = [int(token.strip()) for token in text.split(",")]

    # Disk zero does not exist in this experiment.
    if any(disk < 1 for disk in disks):
        raise ValueError(f"Disk numbers must be positive: {cell_val!r}")

    return disks

# Define the validation function accepting input file, output file, and disk count
def validate_hanoi_experiment(
    input_file: str, output_file: str, num_discs: int = 8
):
    # Validate the configured disk count before constructing the board.
    num_discs = parse_integer(num_discs, "num_discs")

    # A Tower of Hanoi experiment must contain at least one disk.
    if num_discs < 1:
        raise ValueError("num_discs must be at least 1")

    # Read the first worksheet, matching the supplied workbooks.
    df = pd.read_excel(input_file)

    # Require the fields needed to interpret each move.
    required_columns = {"Move #", "Disk", "From", "To"}

    # Identify missing fields before evaluating any rows.
    missing_columns = required_columns - set(df.columns)

    # Stop with a useful explanation if the schema is incomplete.
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    # Detect whether any visual peg columns are present.
    visual_columns = {"Peg 1", "Peg 2", "Peg 3"}
    present_visual_columns = visual_columns.intersection(df.columns)

    # A partial board depiction cannot be checked reliably.
    if present_visual_columns and present_visual_columns != visual_columns:
        missing_visual = visual_columns - present_visual_columns
        raise ValueError(
            f"Missing visual columns: {', '.join(sorted(missing_visual))}"
        ) 

    # Detect whether a human check column exists in the spreadsheet
    has_human_check = "Human Check" in df.columns

    # Detect whether the the spreadsheet contains a visual depiction of
    # the model's perception of the board state
    has_visual_pegs = all(
        col in df.columns for col in ["Peg 1", "Peg 2", "Peg 3"]
    )

    # Initialize the board state with disks 1 through num_discs on Peg 1
    # Peg 1 starts full; Peg 2 and Peg 3 start empty
    # Index 0 represents the top of each peg
    pegs = {1: list(range(1, num_discs + 1)), 2: [], 3: []}

    # Initialize an empty list to record 'Legal' or 'Illegal' for each row
    prog_validation = []

    # Initialize an empty list to store failure reasons for illegal moves
    failure_reasons = []

    # Initialize an empty list to track matches against human reviews if present
    human_matches = []

    # Initialize a list that holds the values indicating if the output
    # is a correct visual match for the internal state of the board
    visual_matches = []

    # Record numbering problems separately from physical move legality.
    move_number_checks = []

    # Track the expected move number independently of DataFrame labels.
    for expected_move, (_, row) in enumerate(df.iterrows(), start=1):

        # Check whether the reported move number matches its row position.
        try:
            reported_move = parse_integer(row["Move #"], "Move #")
            number_check = (
                "MATCH"
                if reported_move == expected_move
                else f"Expected {expected_move}, found {reported_move}"
            )

        # Record missing or malformed move numbers.
        except ValueError as exc:
            number_check = str(exc)

        # Record one numbering result for every row.
        move_number_checks.append(number_check)

        # Validate move identifiers before converting them to integers.
        try:
            source = parse_integer(row["From"], "From")
            dest = parse_integer(row["To"], "To")
            claimed_disc = parse_integer(row["Disk"], "Disk")

        # Record malformed move data without changing the board.
        except ValueError as exc:
            prog_validation.append("Illegal")
            failure_reasons.append(str(exc))

            # Compare the verdict with the human annotation.
            if has_human_check:
                human_val = str(row["Human Check"]).strip().lower()
                human_matches.append(
                    "MATCH" if human_val == "illegal" else "DISCREPANCY"
                )

            # Skip visual comparison when move identifiers are invalid.
            if has_visual_pegs:
                visual_matches.append("UNCHECKED")

            # Evaluate the next row against the unchanged board.
            continue


        # Rule 1: Verify source and destination pegs are valid identifiers (1, 2, or 3)
        if source not in pegs or dest not in pegs:
            # Mark the move as illegal
            prog_validation.append("Illegal")

            # Document invalid peg identifier
            failure_reasons.append(f"Invalid peg ID: {source} -> {dest}")

            # Record match result against human review if column exists
            if has_human_check:
                # Compare verdict with human check
                match = (
                    "MATCH"
                    if str(row["Human Check"]).strip().lower() == "illegal"
                    else "DISCREPANCY"
                )
                human_matches.append(match)

            if has_visual_pegs:
                visual_matches.append("UNCHECKED")

            # Skip board execution
            continue

        # Rule 2: Cannot pull a disk from an empty peg
        if len(pegs[source]) == 0:
            # Mark the move as illegal
            prog_validation.append("Illegal")

            # Document empty source peg
            failure_reasons.append(f"Source peg {source} is empty")

            # Record match result against human review if column exists
            if has_human_check:
                # Compare verdict with human check
                match = (
                    "MATCH"
                    if str(row["Human Check"]).strip().lower() == "illegal"
                    else "DISCREPANCY"
                )
                human_matches.append(match)
            
            # Checks the visual matches, does not check yet
            if has_visual_pegs:
                visual_matches.append("UNCHECKED")

            # Skip board execution
            continue

        # Inspect the disk currently sitting at index 0 (the top) of the source peg
        actual_top_disc = pegs[source][0]

        # Rule 3: Only the top disk can be moved
        if actual_top_disc != claimed_disc:
            # Mark the move as illegal
            prog_validation.append("Illegal")

            # Document that the chosen disk is buried
            failure_reasons.append(
                f"Disc {claimed_disc} is not top disc of peg {source} (Top is {actual_top_disc})"
            )

            # Record match result against human review if column exists
            if has_human_check:
                # Compare verdict with human check
                match = (
                    "MATCH"
                    if str(row["Human Check"]).strip().lower() == "illegal"
                    else "DISCREPANCY"
                )
                human_matches.append(match)

            #Continues to confirm visual column output
            if has_visual_pegs:
                visual_matches.append("UNCHECKED")

            # Skip board execution
            continue

        # Rule 4: Cannot place a larger disk on top of a smaller disk
        if len(pegs[dest]) > 0 and pegs[dest][0] < actual_top_disc:
            # Mark the move as illegal
            prog_validation.append("Illegal")

            # Document the size ordering violation
            failure_reasons.append(
                f"Disc {actual_top_disc} placed on smaller disc {pegs[dest][0]}"
            )

            # Record match result against human review if column exists
            if has_human_check:
                # Compare verdict with human check
                match = (
                    "MATCH"
                    if str(row["Human Check"]).strip().lower() == "illegal"
                    else "DISCREPANCY"
                )
                human_matches.append(match)

            # Continues to confirm visual column
            if has_visual_pegs:
                visual_matches.append("UNCHECKED")

            # Skip board execution
            continue

        # Rule 5: Cannot move a disk to the same peg it currently occupies
        if source == dest:
            # Mark redundant move as illegal
            prog_validation.append("Illegal")

            # Document identical source and destination
            failure_reasons.append(
                f"Source and destination pegs are identical ({source})"
            )

            # Record match result against human review if column exists
            if has_human_check:
                # Compare verdict with human check
                match = (
                    "MATCH"
                    if str(row["Human Check"]).strip().lower() == "illegal"
                    else "DISCREPANCY"
                )
                human_matches.append(match)

            # Continues to confirm visual column
            if has_visual_pegs:
                visual_matches.append("UNCHECKED")

            # Skip board execution
            continue

        # Remove the top disk from the source peg
        moving_disc = pegs[source].pop(0)

        # Place the disk onto index 0 of the destination peg
        pegs[dest].insert(0, moving_disc)

        # Record the move as legal
        prog_validation.append("Legal")

        # Record no failure reason
        failure_reasons.append("None")

        # Record match result against human review if column exists
        if has_human_check:
            # Clean human check text
            human_val = str(row["Human Check"]).strip().lower()
            # Compare legal verdict
            human_matches.append(
                "MATCH" if human_val == "legal" else "DISCREPANCY"
            )

        # 7. Visual State Consistency Check
        # Replaced with code that improves the accuracy
        # of the visual state check, adding three new
        # distinct outcomes; match, drift and invalid

        # Compare the reported post-move board with the simulated board.
        if has_visual_pegs:
            try:
                reported_pegs = {
                    1: parse_peg_cell(row["Peg 1"]),
                    2: parse_peg_cell(row["Peg 2"]),
                    3: parse_peg_cell(row["Peg 3"]),
                }

            # Distinguish malformed visual data from a valid but wrong state.
            except ValueError:
                visual_matches.append("INVALID")

            else:
                visual_matches.append(
                    "MATCH" if reported_pegs == pegs else "DRIFT"
                )

    # Append the programmatic validation column to the DataFrame
    df["Programmatic Validation"] = prog_validation

    # Append the failure reason column to the DataFrame
    df["Validation Failure Reason"] = failure_reasons

    # Append human comparison column only when human check data exists
    if has_human_check:
        # Assign comparison column
        df["Programmatic Match Human"] = human_matches

    # If the visual states of Peg 1, Peg 2, and Peg 3 are correct, 
    # outputs a message
    if has_visual_pegs:
        df["Visual State Match"] = visual_matches

    # Write the modified DataFrame to the output Excel path
    # Include sequence-label findings alongside move and visual findings.
    df["Move Number Check"] = move_number_checks
    
    # Write the DataFrame, including validation results, to the output Excel file.
    # Exclude the pandas row index so it does not become an extra spreadsheet column.
    df.to_excel(output_file, index=False)

    # Compute total rows evaluated
    total_moves = len(df)

    # Compute optimal move count using 2^n - 1
    optimal_moves = (2**num_discs) - 1

    # Count illegal moves found
    illegal_count = prog_validation.count("Illegal")
    # This experiment starts on Peg 1 and targets Peg 3.
    expected_final_board = {
        1: [],
        2: [],
        3: list(range(1, num_discs + 1)),
    }

    # Check the simulated final board, independent of visual claims.
    goal_reached = pegs == expected_final_board

    # Count numbering errors.
    numbering_error_count = sum(
        result != "MATCH" for result in move_number_checks
    )

    # A valid complete solve requires every listed move to be legal.
    legal_complete_solve = illegal_count == 0 and goal_reached

    # An optimal solve must also use the minimum possible move count.
    optimal_solve = legal_complete_solve and total_moves == optimal_moves

    # Require matching visuals when visual columns are provided.
    visual_report_correct = (
        all(result == "MATCH" for result in visual_matches)
        if has_visual_pegs
        else True
    )

    # Combine the physical solve and reporting requirements.
    experiment_passed = (
        optimal_solve
        and numbering_error_count == 0
        and visual_report_correct
    )

    print(f"Experiment Passed: {experiment_passed}")
    # Output verification summary
    print("--- Validation Summary ---")
    print(f"Total Moves Analyzed: {total_moves}")
    print(f"Optimal Move Target (2^{num_discs} - 1): {optimal_moves}")
    print(f"Illegal Moves Detected: {illegal_count}")
    print(f"Move Number Errors: {numbering_error_count}")
    #Added additional information to be displayed
    print(f"Goal Reached on Peg 3: {goal_reached}")
    print(f"Legal Complete Solve: {legal_complete_solve}")
    print(f"Optimal Solve: {optimal_solve}")

    # Output discrepancy count only if human check was performed
    if has_human_check:
        discrepancy_count = human_matches.count("DISCREPANCY")
        print(f"Discrepancies vs Human Check: {discrepancy_count}")
    else:
        print("Human Check Column: Not present (Automated mode)")


    # Output the counts of correct and incorrect visual state cells.
    # Summarize every visual-check outcome.
    if has_visual_pegs:
        drift_count = visual_matches.count("DRIFT")
        invalid_count = visual_matches.count("INVALID")
        unchecked_count = visual_matches.count("UNCHECKED")
        valid_matches = visual_matches.count("MATCH")

        print(
            f"Visual Peg Alignment: {valid_matches} MATCH, "
            f"{drift_count} DRIFT, {invalid_count} INVALID, "
            f"{unchecked_count} UNCHECKED"
        )

    print(f"Output saved to: {output_file}")


# Script entry point
if __name__ == "__main__":
    # Check if the user supplied an input file via command line
    if len(sys.argv) > 1:
        # User provided: python verify_hanoi.py <input_file> [output_file] [discs]
        input_file = sys.argv[1]
        output_file = (
            sys.argv[2]
            if len(sys.argv) > 2
            # If no output path is provided, save beside the input file
            # using its filename stem with a "verified_" prefix and ".xlsx" extension.
            else str(
                Path(input_file).with_name(
                    f"verified_{Path(input_file).stem}.xlsx"
                )
            )
        )
        # Let the validation function apply the same strict integer rule.
        num_discs = sys.argv[3] if len(sys.argv) > 3 else 8
    else:
        # Default fallback if no arguments are provided
        input_file = "Copy of hanoi_moves_checkedGpt4oLeahWilson.xlsx"
        output_file = "hanoi_moves_programmatically_verified.xlsx"
        num_discs = 8

    validate_hanoi_experiment(
        input_file=input_file, output_file=output_file, num_discs=num_discs
    )