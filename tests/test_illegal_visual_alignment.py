
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


# Resolve paths relative to the repository, not the terminal directory.
ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "negative" / "test_corrupt_hanoi.xlsx"
VERIFIER = ROOT / "verify_hanoi.py"


class TestIllegalVisualAlignment(unittest.TestCase):
    """Verify visual drift detection on a rejected Hanoi move."""

    def test_illegal_move_with_visual_drift(self):
        # Work in a temporary directory to preserve research fixtures.
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "illegal_visual_drift.xlsx"
            output_file = Path(temp_dir) / "verified_visual_drift.xlsx"

            # Load the known negative-test fixture.
            df = pd.read_excel(FIXTURE)

            # Confirm the expected test row exists exactly once.
            target = df["Move #"] == 10
            self.assertEqual(target.sum(), 1)

            # Corrupt the reported board without changing the move itself.
            df.loc[target, "Peg 3"] = "[99]"
            df.to_excel(input_file, index=False)

            # Run the real verifier against the modified spreadsheet.
            result = subprocess.run(
                [
                    sys.executable,
                    str(VERIFIER),
                    str(input_file),
                    str(output_file),
                    "4",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            # A rejected experiment should still produce an output file.
            self.assertEqual(
                result.returncode,
                0,
                msg=f"Verifier failed:\n{result.stderr}",
            )
            self.assertTrue(output_file.exists())

            # Inspect the verifier's actual row-level classifications.
            verified = pd.read_excel(output_file)
            row = verified.loc[verified["Move #"] == 10]

            self.assertEqual(len(row), 1)
            self.assertEqual(
                row.iloc[0]["Programmatic Validation"],
                "Illegal",
            )
            self.assertEqual(
                row.iloc[0]["Visual State Match"],
                "DRIFT",
            )


if __name__ == "__main__":
    unittest.main()
