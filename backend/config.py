IGNORE_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    "venv",
    "env",
    "node_modules",
    ".idea",
    ".vscode",
    "build",
    "dist"
}

IGNORE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".zip",
    ".exe",
    ".dll",
    ".so",
    ".pyc"
}

LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",
    ".tsx": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rs": "rust"
}

SEMANTIC_NODES = {
    "python": {
        "class_definition",
        "function_definition",
        "decorated_definition",
    },

    "javascript": {
        "class_declaration",
        "function_declaration",
        "method_definition",
    },

    "java": {
        "class_declaration",
        "method_declaration",
    },
}
