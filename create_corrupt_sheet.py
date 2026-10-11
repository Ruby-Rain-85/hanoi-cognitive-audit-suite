# Import the argument parser module for handling command-line options
import argparse
# Import random to shuffle target error rows deterministically
import random
# Import pandas to create and export the spreadsheet structure
import pandas as pd

# generates optimal move sets and stores them for later comparison
def generate_optimal_moves(num_disks: int) -> list[tuple[int, int, int]]:
    """
    Generate the optimal Tower of Hanoi move sequence.

    Each move is represented as:
        (disk, source_peg, destination_peg)

    The puzzle starts on Peg 1 and ends on Peg 3.
    """

    # Store the complete sequence of legal moves.
    moves = []

    def solve(n, source, target, auxiliary):
        # Base case: move the smallest remaining disk.
        if n == 1:
            moves.append((1, source, target))
            return

        # Move the smaller disks to the auxiliary peg.
        solve(n - 1, source, auxiliary, target)

        # Move the largest disk in this recursive step.
        moves.append((n, source, target))

        # Move the smaller disks onto the target peg.
        solve(n - 1, auxiliary, target, source)

    solve(num_disks, 1, 3, 2)

    return moves

#
def apply_hanoi_move(
    pegs: dict[int, list[int]],
    disk: int,
    source: int,
    destination: int
) -> tuple[bool, str]:
    """
    Validate and conditionally execute one Tower of Hanoi move.

    Returns:
        (True, "Legal") when the move is accepted.
        (False, reason) when the move is rejected.

    Rejected moves must never modify the board.
    """

    # Rule 1: Source and destination must be valid pegs.
    if source not in pegs or destination not in pegs:
        return False, "Invalid peg ID"

    # Rule 2: Source and destination must differ.
    if source == destination:
        return False, "Identical source and destination"

    # Rule 3: Cannot move a disk from an empty peg.
    if not pegs[source]:
        return False, "Empty source peg"

    # Rule 4: The claimed disk must be the top disk.
    actual_top = pegs[source][0]

    if disk != actual_top:
        return False, "Disk is not the top disk"

    # Rule 5: Cannot place a larger disk on a smaller disk.
    if pegs[destination] and disk > pegs[destination][0]:
        return False, "Larger disk onto smaller disk"

    # All checks passed. Execute the legal move.
    moving_disk = pegs[source].pop(0)
    pegs[destination].insert(0, moving_disk)

    return True, "Legal"

#
def snapshot_board(
    pegs: dict[int, list[int]]
) -> dict[int, list[int]]:
    """
    Return an independent copy of the current board.

    This prevents later moves from changing earlier
    recorded visual states.
    """

    return {
        peg: disks.copy()
        for peg, disks in pegs.items()
    }


def construct_fault(error, pegs, disk, source, destination):
    """
    Construct a faulty move proposal without changing the board.

    Returns:
        disk, source, destination, human_label

    Visual-only and human-label faults retain legal moves.
    """

    human_label = "Legal"

    if error == "Malformed Data":
        source = "one"
        human_label = "Illegal"

    elif error == "Invalid Peg ID":
        destination = 4
        human_label = "Illegal"

    elif error == "Empty Source Peg":
        empty_pegs = [p for p in pegs if not pegs[p]]

        if not empty_pegs:
            raise ValueError("No empty peg available for this fault")

        source = empty_pegs[0]
        destination = next(p for p in pegs if p != source)
        human_label = "Illegal"

    elif error == "Ghost Disk":
        disk = max(
            d for disks in pegs.values() for d in disks
        ) + 1
        human_label = "Illegal"

    elif error == "Size Inversion":
        candidates = [
            (src, dst)
            for src in pegs
            for dst in pegs
            if src != dst
            and pegs[src]
            and pegs[dst]
            and pegs[src][0] > pegs[dst][0]
        ]

        if not candidates:
            raise ValueError("No size inversion available for this board")

        source, destination = candidates[0]
        disk = pegs[source][0]
        human_label = "Illegal"

    elif error == "Identical Pegs":
        occupied = [p for p in pegs if pegs[p]]
        source = occupied[0]
        destination = source
        disk = pegs[source][0]
        human_label = "Illegal"

    elif error == "Human Discrepancy":
        # The move remains legal, but the human label is incorrect.
        human_label = "Illegal"

    elif error == "Visual Drift":
        # The move remains legal. Only its reported visual state changes.
        pass

    else:
        raise ValueError(f"Unknown fault type: {error}")

    return disk, source, destination, human_label

#
def construct_fault(error, pegs, disk, source, destination):
    """
    Construct a faulty move proposal without changing the board.

    Returns:
        disk, source, destination, human_label

    Visual-only and human-label faults retain legal moves.
    """

    human_label = "Legal"

    if error == "Malformed Data":
        source = "one"
        human_label = "Illegal"

    elif error == "Invalid Peg ID":
        destination = 4
        human_label = "Illegal"

    elif error == "Empty Source Peg":
        empty_pegs = [p for p in pegs if not pegs[p]]

        if not empty_pegs:
            raise ValueError("No empty peg available for this fault")

        source = empty_pegs[0]
        destination = next(p for p in pegs if p != source)
        human_label = "Illegal"

    elif error == "Ghost Disk":
        disk = max(
            d for disks in pegs.values() for d in disks
        ) + 1
        human_label = "Illegal"

    elif error == "Size Inversion":
        candidates = [
            (src, dst)
            for src in pegs
            for dst in pegs
            if src != dst
            and pegs[src]
            and pegs[dst]
            and pegs[src][0] > pegs[dst][0]
        ]

        if not candidates:
            raise ValueError("No size inversion available for this board")

        source, destination = candidates[0]
        disk = pegs[source][0]
        human_label = "Illegal"

    elif error == "Identical Pegs":
        occupied = [p for p in pegs if pegs[p]]
        source = occupied[0]
        destination = source
        disk = pegs[source][0]
        human_label = "Illegal"

    elif error == "Human Discrepancy":
        # The move remains legal, but the human label is incorrect.
        human_label = "Illegal"

    elif error == "Visual Drift":
        # The move remains legal. Only its reported visual state changes.
        pass

    else:
        raise ValueError(f"Unknown fault type: {error}")

    return disk, source, destination, human_label


def generate_corrupt_hanoi_sheet(num_disks: int, filename: str):
    """
    Generates a Hanoi test spreadsheet containing every error condition
    checked by verify_hanoi.py across an optimal 2^n - 1 move sequence.
    """
    # Fix the random seed to produce reproducible row selections
    random.seed(42)

    # Compute optimal move count using the recurrence relation limit 2^n - 1
    total_moves = (2**num_disks) - 1

    # Verify that the sequence has enough moves to test all 8 scenarios
    if total_moves < 8:
        raise ValueError(
            f"Disk count {num_disks} produces {total_moves} moves. "
            "A minimum of 4 disks (15 moves) is required to test all 8 error cases."
        )

    # replaced current solver with an optimal reference sequence
    base_moves = generate_optimal_moves(num_disks)

    # Select distinct reference moves for fault injection.
    available_indices = list(range(1, total_moves))
    random.shuffle(available_indices)

    fault_types = [
        "Malformed Data",
        "Invalid Peg ID",
        "Empty Source Peg",
        "Ghost Disk",
        "Size Inversion",
        "Identical Pegs",
        "Visual Drift",
        "Human Discrepancy",
    ]

    error_mapping = {
        fault: available_indices.pop()
        for fault in fault_types
    }

    index_to_error = {
        index: fault
        for fault, index in error_mapping.items()
    }

    # Authoritative board. Only legal moves may change it.
    pegs = {1: list(range(1, num_disks + 1)), 2: [], 3: []}

    rows = []

    def append_row(disk, source, destination, human_label, fault):
        """
        Validate an attempted move, then record its resulting board.

        Illegal attempts leave the authoritative board unchanged.
        """

        legal, reason = apply_hanoi_move(
            pegs, disk, source, destination
        )

        # Capture the post-attempt board.
        visual = snapshot_board(pegs)

        # Corrupt only the reported visual state when requested.
        if fault == "Visual Drift":
            visual[3] = [99]

        rows.append({
            "Move #": len(rows) + 1,
            "Disk": disk,
            "From": source,
            "To": destination,
            "Peg 1": str(visual[1]),
            "Peg 2": str(visual[2]),
            "Peg 3": str(visual[3]),
            "Human Check": human_label,
            "Targeted Error": fault,
        })

        return legal, reason

    # Follow the optimal solution while inserting fault attempts.
    for idx, (disk, source, destination) in enumerate(base_moves):

        fault = index_to_error.get(idx)

        if fault is not None:
            faulty_disk, faulty_source, faulty_destination, human_label = (
                construct_fault(
                    fault, pegs, disk, source, destination
                )
            )

            # Insert the negative-test attempt.
            legal, reason = append_row(
                faulty_disk,
                faulty_source,
                faulty_destination,
                human_label,
                fault,
            )

            # Physical move faults must be rejected.
            if fault not in ("Visual Drift", "Human Discrepancy"):
                if legal:
                    raise AssertionError(
                        f"{fault} unexpectedly produced a legal move"
                    )

            # Visual and human-label faults execute the reference move.
            else:
                if not legal:
                    raise AssertionError(
                        f"{fault} unexpectedly produced an illegal move: {reason}"
                    )
                continue

        # Execute the original optimal move.
        legal, reason = append_row(
            disk, source, destination, "Legal", "None"
        )

        if not legal:
            raise AssertionError(
                f"Reference move {idx + 1} was rejected: {reason}"
            )

    # Convert row dictionaries into a pandas DataFrame
    df = pd.DataFrame(rows)
    # Save DataFrame to Excel file without index column
    df.to_excel(filename, index=False)

    # Print summary of generated test suite
    print(f"Generated test file: {filename}")
    # Added rows per number of disks and optimal reference moves
    print(f"Total Rows: {len(rows)} (for {num_disks} disks)")
    print(f"Optimal Reference Moves: {total_moves}")
    print("Injected Error Mapping:")
    for row in rows:
        if row["Targeted Error"] != "None":
            print(
                f"  - Row {row['Move #']}: "
                f"{row['Targeted Error']}"
            )
# Testing move sequence for optimization
def test_optimal_moves():
    moves = generate_optimal_moves(3)

    assert len(moves) == 7
    assert moves[0] == (1, 1, 3)
    assert moves[-1] == (1, 1, 3)

    print("Optimal move generator test passed.")


def test_board_simulator():
    # Initialize a three-disk board.
    pegs = {1: [1, 2, 3], 2: [], 3: []}

    # Test 1: A legal move should update the board.
    legal, reason = apply_hanoi_move(pegs, 1, 1, 3)

    assert legal is True
    assert reason == "Legal"
    assert pegs == {1: [2, 3], 2: [], 3: [1]}

    # Save an independent snapshot.
    saved_state = snapshot_board(pegs)

    # Test 2: A buried disk must be rejected.
    legal, reason = apply_hanoi_move(pegs, 3, 1, 2)

    assert legal is False
    assert reason == "Disk is not the top disk"
    assert pegs == saved_state

    # Test 3: A larger disk cannot be placed on a smaller disk.
    legal, reason = apply_hanoi_move(pegs, 2, 1, 3)

    assert legal is False
    assert reason == "Larger disk onto smaller disk"
    assert pegs == saved_state

    # Test 4: An empty source must be rejected.
    legal, reason = apply_hanoi_move(pegs, 1, 2, 1)

    assert legal is False
    assert reason == "Empty source peg"
    assert pegs == saved_state

    # Test 5: A second legal move updates the current board.
    legal, reason = apply_hanoi_move(pegs, 2, 1, 2)

    assert legal is True
    assert pegs == {1: [3], 2: [2], 3: [1]}

    # The earlier snapshot must remain unchanged.
    assert saved_state == {1: [2, 3], 2: [], 3: [1]}

    print("Board simulator tests passed.")


# Define entry point for execution via command-line arguments
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Generate negative testing spreadsheet for verify_hanoi.py."
    )
    # Define disk argument (-n / --disks)
    parser.add_argument(
        "-n",
        "--disks",
        type=int,
        default=4,
        help="Number of disks (minimum: 4, default: 4)",
    )
    # Define output file argument (-o / --output)
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="test_corrupt_hanoi.xlsx",
        help="Output filename (default: test_corrupt_hanoi.xlsx)",
    )

    # Parse arguments from command line
    args = parser.parse_args()

    # Call generator function
    generate_corrupt_hanoi_sheet(num_disks=args.disks, filename=args.output)
    