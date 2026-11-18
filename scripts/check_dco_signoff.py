"""Check DCO sign-offs on every commit in a pull-request range."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


SIGNOFF = re.compile(
    r"^Signed-off-by:\s+.+\s+<[^<>\s]+@[^<>\s]+>\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def has_dco_signoff(message: str) -> bool:
    """Return whether a commit message contains a well-formed DCO trailer."""
    return SIGNOFF.search(message) is not None


def commit_messages(base: str, head: str, root: Path) -> list[tuple[str, str, str]]:
    """Return (sha, subject, full message) for commits in base..head."""
    result = subprocess.run(
        [
            "git", "log", "--format=%H%x1f%s%x1f%B%x00",
            f"{base}..{head}",
        ],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    commits = []
    for record in result.stdout.split("\x00"):
        if not record.strip():
            continue
        fields = record.split("\x1f", 2)
        if len(fields) != 3:
            raise ValueError(f"Could not parse git log record: {record[:120]!r}")
        commits.append((fields[0].strip(), fields[1].strip(), fields[2]))
    return commits


def audit_messages(commits: list[tuple[str, str, str]]) -> list[str]:
    """Return a diagnostic for each commit without a DCO sign-off."""
    return [
        f"{sha[:12]} {subject}"
        for sha, subject, message in commits
        if not has_dco_signoff(message)
    ]


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print(
            "Usage: python scripts/check_dco_signoff.py BASE_SHA HEAD_SHA",
            file=sys.stderr,
        )
        return 2
    try:
        commits = commit_messages(args[0], args[1], Path(__file__).resolve().parents[1])
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"Unable to inspect contribution commits: {exc}", file=sys.stderr)
        return 2

    missing = audit_messages(commits)
    if missing:
        print("Every contribution commit must include a DCO sign-off:")
        print("\n".join(f"  - {item}" for item in missing))
        print("Create or amend commits with: git commit -s")
        return 1
    print(f"DCO sign-off verified for all {len(commits)} contribution commit(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
