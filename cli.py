import sys
from backend.coder import generate_code
from backend.critic import review_code
from backend.comparison import compare_code

def main():
    print("=" * 60)
    print("        CodeLoop AI - Terminal Code Reviewer")
    print("=" * 60)
    print("Enter your problem statement below.")
    print("(Press Enter twice or Ctrl+Z/Ctrl+D then Enter when finished):")
    print("-" * 60)

    lines = []
    while True:
        try:
            line = input()
            if line == "" and lines and lines[-1] == "":
                # Two consecutive empty lines to finish input
                break
            lines.append(line)
        except EOFError:
            break

    problem = "\n".join(lines).strip()
    if not problem:
        print("\n[!] No problem entered. Exiting.")
        return

    print("\n" + "=" * 60)
    print("[1/4] Generating initial solution (Coder v1)...")
    code_v1 = generate_code(problem)
    print("-" * 60)
    print("--- CODE V1 ---")
    print(code_v1)

    print("\n" + "=" * 60)
    print("[2/4] Critic AI is reviewing the solution...")
    criticism = review_code(problem, code_v1)
    print("-" * 60)
    print("--- CRITIC REVIEW ---")
    print(criticism)

    print("\n" + "=" * 60)
    print("[3/4] Coder AI is refining the code based on feedback...")
    code_v2 = generate_code(problem, code_v1, criticism)
    print("-" * 60)
    print("--- CODE V2 ---")
    print(code_v2)

    print("\n" + "=" * 60)
    print("[4/4] Comparing metrics...")
    comparison = compare_code(code_v1, code_v2)
    diff = comparison.get("difference", {})
    print("-" * 60)
    print("--- COMPARISON METRICS ---")
    print(f"Characters: {comparison['version_1']['characters']} -> {comparison['version_2']['characters']} (Delta: {diff.get('characters', 0)})")
    print(f"Lines:      {comparison['version_1']['lines']} -> {comparison['version_2']['lines']} (Delta: {diff.get('lines', 0)})")
    print(f"Words:      {comparison['version_1']['words']} -> {comparison['version_2']['words']} (Delta: {diff.get('words', 0)})")
    print(f"Change %:   {comparison.get('character_change_percent', 0)}%")
    print("=" * 60)
    print("Review process complete!")

if __name__ == "__main__":
    main()
