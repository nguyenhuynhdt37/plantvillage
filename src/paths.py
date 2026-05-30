"""Path discovery helpers for portable notebooks and scripts."""

from __future__ import annotations

from pathlib import Path


def find_project_dir(start=None) -> Path:
    """Find the project `plan` directory from common notebook/script locations."""

    search_roots = []
    if start is not None:
        start_path = Path(start).resolve()
        search_roots.extend([start_path, *start_path.parents])

    cwd = Path.cwd().resolve()
    search_roots.extend([cwd, *cwd.parents])

    seen = set()
    for root in search_roots:
        if root in seen:
            continue
        seen.add(root)

        if root.name == "plan" and (root / "src").exists():
            return root

        plan_dir = root / "plan"
        if (plan_dir / "src").exists():
            return plan_dir

    raise FileNotFoundError(
        "Không tìm thấy thư mục project plan chứa src/. "
        "Hãy chạy notebook từ repo hoặc thư mục plan."
    )
