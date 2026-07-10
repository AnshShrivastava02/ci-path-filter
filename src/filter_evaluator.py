from src.glob_matcher import match_path


def evaluate_filter(patterns, changed_files):
    """Decide if a filter is true or false  if any changed file matches an include or exclude filter"""

    # handling patterns first
    # separating the patterns into includes and excludes
    includes = []
    excludes = []

    for pattern in patterns:
        if pattern.startswith("!"):
            excludes.append(
                pattern[1:]
            )  # appending pattern in excludes after removing !
        else:
            includes.append(pattern)  # appending in includes

    # handling changed files
    # checking each file and matching them using glob match path
    for file in changed_files:
        included = False
        for pattern in includes:
            if match_path(pattern, file):
                included = True  # the file matched at least one include pattern

        excluded = False
        for pattern in excludes:
            if match_path(pattern, file):
                excluded = True  # the file matched at least one exclude pattern

        # Making filter evaluation logic - included and NOT excluded
        if included and not excluded:
            return True  # filter returns true if filter matches

    return False  # if nothing matches filter is false


def evaluate_all(filters, changed_files):
    """will run evaluate filter method on every filter name and files"""
    results = {}
    for name, patterns in filters.items():
        results[name] = evaluate_filter(patterns, changed_files)
    return results
