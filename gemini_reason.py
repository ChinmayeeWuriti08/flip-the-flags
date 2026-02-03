import os
import sys
from google import genai
from scan_flags import scan_flags


REASONING_MODE = "local"  
REPO_PATH = sys.argv[1] if len(sys.argv) > 1 else "sample_repo"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_category(output):
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Category:"):
            return line.replace("Category:", "").strip()
    return None


def count_flag_dependencies(flag_name, folder_path):
    count = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if flag_name in line:
                            count += 1
    return count



def derive_signals(flag, dependency_count):
    snippet = flag["code"].lower()

    return {
        "controls_core_logic": "login" in snippet or "payment" in snippet,
        "marked_temporary": "temporary" in snippet or "rollout" in snippet,
        "hardcoded_flag": "= true" in snippet,
        "dependency_lines": dependency_count,
    }


def local_reasoning(flag, signals):
    if signals["controls_core_logic"] and not signals["hardcoded_flag"]:
        return f"""
Category: Danger
Explanation:
This flag controls runtime behavior in a critical execution path.
Incorrect usage could have high-impact consequences.

Suggested Action:
- Audit all dependent code paths.
- Restrict or remove runtime control.
"""

    if signals["marked_temporary"] and not signals["hardcoded_flag"]:
        return f"""
Category: Needs Fixing
Explanation:
This flag was introduced for temporary behavior control.
It is referenced in approximately {signals['dependency_lines']} lines of code.
Unresolved rollout flags increase maintenance burden.

Suggested Action:
- Decide whether the feature is permanent.
- Remove the flag or formalize configuration.
"""

    if signals["hardcoded_flag"]:
        return f"""
Category: Obsolete / Remove
Explanation:
This flag is statically set and no longer provides runtime control.
Retaining it adds unnecessary cognitive load.

Suggested Action:
- Remove the flag.
- Inline the active code path.
"""

    return """
Category: Needs Fixing
Explanation:
This flag has unclear intent and impact.
Its behavior cannot be confidently assessed.
Ambiguity increases long-term risk.

Suggested Action:
- Review intent and usage.
"""



def gemini_reasoning(flag, signals):
    prompt = f"""
You are a senior software engineer reviewing feature flags in a long-lived codebase.

Derived Signals:
- Controls core logic: {signals['controls_core_logic']}
- Marked temporary: {signals['marked_temporary']}
- Hardcoded value: {signals['hardcoded_flag']}
- Dependency lines: {signals['dependency_lines']}

Flag Name: {flag['name']}
File: {flag['file']}

Code Context:
{flag['code']}

Respond strictly in this format:

Category: <Danger | Needs Fixing | Obsolete / Remove>
Explanation:
- Exactly 3 short sentences
- Sentence 1: current technical state
- Sentence 2: why original intent no longer applies
- Sentence 3: why the developer should care

Suggested Action:
- 1–3 imperative cleanup steps
"""

    response = client.models.generate_content(
        model="models/gemini-pro-latest",
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
    )

    return response.text



def classify_flag(flag):
    dependency_count = count_flag_dependencies(flag["name"], REPO_PATH)
    # print(f"[DEBUG] {flag['name']} dependency lines = {dependency_count}")
    signals = derive_signals(flag, dependency_count)

    if REASONING_MODE == "local":
        return local_reasoning(flag, signals)

    return gemini_reasoning(flag, signals)



if __name__ == "__main__":
    flags = scan_flags(REPO_PATH)

    results = {
        "Danger": [],
        "Needs Fixing": [],
        "Obsolete / Remove": [],
        "Analysis Skipped": [],
    }

    for flag in flags:
        output = classify_flag(flag)
        category = extract_category(output)

        if category in results:
            results[category].append({
                "name": flag["name"],
                "output": output,
                "dependency_lines": count_flag_dependencies(flag["name"], REPO_PATH)
            })
            # results[category].append((flag["name"], output))
        else:
            results["Analysis Skipped"].append((flag["name"], output))

    print("\n===== FLAG SENSE REPORT =====\n")
    

    if all(len(results[cat]) == 0 for cat in ["Danger", "Needs Fixing", "Obsolete / Remove"]):
        print("No feature flags were detected in the scanned repository.")
        print("This likely indicates a clean or a configuration light codebase.\n")
    else:
        for category in ["Danger", "Needs Fixing", "Obsolete / Remove"]:
            if results[category]:
                print(f"{category.upper()} ({len(results[category])})\n")

                for item in results[category]:
                    print(f"Flag: {item['name']}")
                    print(f"Dependent code lines: {item['dependency_lines']}\n")
                    print(item["output"])
                    print("-" * 50)
    if results["Analysis Skipped"]:
        print("\nANALYSIS SKIPPED\n")
        for name, _ in results["Analysis Skipped"]:
            print(f"- {name}")
