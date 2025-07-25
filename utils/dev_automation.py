def generate_commit_and_issue(task_description: str) -> str:
    return (
        f"Generate a conventional commit message and a GitHub issue template "
        f"based on this task description:\n\n{task_description}\n\n"
        "Include:\n- A commit message using conventional format\n"
        "- A GitHub issue with title, description, and a checklist"
    )
