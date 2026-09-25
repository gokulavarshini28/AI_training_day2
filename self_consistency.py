import sys
from pathlib import Path
from collections import Counter

# Allow this file to use the Day 1 files
DAY1_FOLDER = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DAY1_FOLDER))

from config import client, MODEL
from cot_compare import COT_PROMPT, QUESTIONS


RUNS = 5
TEMPERATURE = 0.8


def extract_answer(text):
    """Get the final answer from the model response."""

    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()

    return text.strip().splitlines()[-1].strip()


def normalize_answer(answer):
    """Convert equivalent numeric answers to the same format."""

    cleaned = answer.replace(",", "")

    number = ""

    for ch in cleaned:
        if ch.isdigit() or ch == ".":
            number += ch

    try:
        return f"{float(number):.2f}"
    except ValueError:
        return answer.strip()


def run_many(question):

    answers = []

    for attempt in range(1, RUNS + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": COT_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=TEMPERATURE,
        )

        raw_answer = extract_answer(
            response.choices[0].message.content
        )

        answer = normalize_answer(raw_answer)

        print(f"Run {attempt}: {answer}")

        answers.append(answer)

    return answers


if __name__ == "__main__":

    print("\n=== SELF-CONSISTENCY ===\n")

    question = QUESTIONS[0]

    print("QUESTION:")
    print(question)
    print()

    answers = run_many(question)

    counts = Counter(answers)

    winner, count = counts.most_common(1)[0]

    print()
    print(f"Majority answer: {winner}")
    print(f"Votes: {count} out of {RUNS}")