def rewrite_content(content: str, tone: str) -> str:
    return (
        f"Rewrite the following content in a {tone} tone:\n\n"
        f"{content}\n\n"
        "Ensure it remains clear and engaging."
    )
