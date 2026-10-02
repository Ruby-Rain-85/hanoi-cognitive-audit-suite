import pandas as pd

data = {
    "Move #": [1, 2, 3, 4, 5, 6, 7, 8],
    "Disk": [1, 2, 1, 3, 1, 1, 1, 2],
    "From": [1, 1, 3, 1, 2, 4, "one", 1],
    "To": [2, 2, 1, 3, 2, 2, 2, 3],
    "Peg 1": [
        "[2, 3]",
        "[3]",
        "[1, 2, 3]",
        "[2]",
        "[2, 3]",
        "[2, 3]",
        "[2, 3]",
        "[3]",
    ],
    "Peg 2": ["[1]", "[2, 1]", "[1]", "[1]", "[1]", "[1]", "[1]", "[1]"],
    "Peg 3": ["[]", "[]", "[]", "[3]", "[]", "[]", "[]", "[99]"],
    "Human Check": [
        "Legal",
        "Illegal",
        "Illegal",
        "Illegal",
        "Illegal",
        "Illegal",
        "Illegal",
        "Legal",
    ],
}

df = pd.DataFrame(data)
df.to_excel("test_corrupt_hanoi.xlsx", index=False)
print("File test_corrupt_hanoi.xlsx created successfully.")