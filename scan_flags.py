import os
import re

import os
import re

def scan_flags(folder_path):
    # print(">>> SCANNING FOLDER:", os.path.abspath(folder_path))
    flags = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            # print(">>> FOUND FILE:", file)
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    for lineno, line in enumerate(f, start=1):
                        match = re.match(
                            r"\s*([A-Z][A-Z0-9_]*)\s*=\s*(True|False)",
                            line
                        )

                        if match:
                            flags.append({
                                "name": match.group(1),
                                "value": match.group(2),
                                "file": file_path,
                                "line": lineno,
                                "code": line.strip()
                            })

    return flags




# def scan_flags(repo_path):
    flags = {}

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    match = re.search(r"\b([A-Z_]{3,})\s*=\s*(True|False)\b", line)
                    if match:
                        flag_name = match.group()

                        start = max(0, i - 3)
                        end = min(len(lines), i + 4)
                        snippet = "".join(lines[start:end])

                        if flag_name not in flags:
                            flags[flag_name] = {
                                "name": flag_name,
                                "file": file_path,
                                "snippet": snippet
                            }

    return list(flags.values())
