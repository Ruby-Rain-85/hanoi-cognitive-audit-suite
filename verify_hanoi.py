# Import pandas to parse and update Excel files
import pandas as pd
import sys

# Define the validation function accepting input file, output file, and disk count
def validate_hanoi_experiment(
    input_file: str, output_file: str, num_discs: int = 8
):
    # Read the Excel spreadsheet into a pandas DataFrame
    df = pd.read_excel(input_file)

    # Detect whether a human check column exists in the spreadsheet
    has_human_check = "Human Check" in df.columns

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

    # Iterate through every row in the DataFrame using index idx and row data
    for idx, row in df.iterrows():
        # Begin try block to handle malformed, non-numeric cell contents
        try:
            # Convert the source peg value to an integer
            source = int(row["From"])

            # Convert the target peg value to an integer
            dest = int(row["To"])

            # Convert the claimed moving disk to an integer
            claimed_disc = int(row["Disk"])

        # Catch data conversion errors from unexpected text or empty cells
        except (ValueError, TypeError):
            # Mark the move as illegal due to invalid input
            prog_validation.append("Illegal")

            # Document the non-numeric data issue
            failure_reasons.append("Non-integer peg or disk data")

            # Check if human comparison is active
            if has_human_check:
                # Flag comparison as an error
                human_matches.append("ERROR")

            # Advance to the next spreadsheet row
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

    # Append the programmatic validation column to the DataFrame
    df["Programmatic Validation"] = prog_validation

    # Append the failure reason column to the DataFrame
    df["Validation Failure Reason"] = failure_reasons

    # Append human comparison column only when human check data exists
    if has_human_check:
        # Assign comparison column
        df["Programmatic Match Human"] = human_matches

    # Write the modified DataFrame to the output Excel path
    df.to_excel(output_file, index=False)

    # Compute total rows evaluated
    total_moves = len(df)

    # Compute optimal move count using 2^n - 1
    optimal_moves = (2**num_discs) - 1

    # Count illegal moves found
    illegal_count = prog_validation.count("Illegal")

    # Output verification summary
    print("--- Validation Summary ---")
    print(f"Total Moves Analyzed: {total_moves}")
    print(f"Optimal Move Target (2^{num_discs} - 1): {optimal_moves}")
    print(f"Illegal Moves Detected: {illegal_count}")

    # Output discrepancy count only if human check was performed
    if has_human_check:
        discrepancy_count = human_matches.count("DISCREPANCY")
        print(f"Discrepancies vs Human Check: {discrepancy_count}")
    else:
        print("Human Check Column: Not present (Automated mode)")

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
            else f"verified_{input_file.split('.')[0]}.xlsx"
        )
        num_discs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    else:
        # Default fallback if no arguments are provided
        input_file = "Copy of hanoi_moves_checkedGpt4oLeahWilson.xlsx"
        output_file = "hanoi_moves_programmatically_verified.xlsx"
        num_discs = 8

    validate_hanoi_experiment(
        input_file=input_file, output_file=output_file, num_discs=num_discs
    )