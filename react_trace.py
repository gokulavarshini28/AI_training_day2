import sys
from pathlib import Path

# Allow this file to use the Day 1 files
DAY1_FOLDER = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DAY1_FOLDER))

from agent import agent


QUESTION = (
    "Which is cheaper: CS101 and AI202 with a 10% scholarship, "
    "or all three courses with a 25% scholarship? By how much?"
)

print("QUESTION:", QUESTION)
print()
print("--- THE AGENT'S ACTIONS AND OBSERVATIONS ---")

answer = agent(QUESTION, max_steps=8)

print()
print("FINAL ANSWER:", answer)