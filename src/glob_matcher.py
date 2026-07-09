import re


def globe_to_regex(pattern):
    regex = ""
    i = 0
    """Walk through the pattern one piece at a time, translating glob symbols to regex."""

    while i < len(pattern):
        rest = pattern[i:]  # handling the pattern starting from char i

        if rest.startswith("**/"):
            # check for glob of zero or more folders with folders as optional
            regex += "(?:.*/)?"
            i += 3
        elif rest.startswith("**"):
            # check for glob which matches everything including  folder boundaries
            regex += ".*"
            i += 2
        elif rest.startswith("*"):
            # check for glob matched within a single folder not across a /
            regex += "[^/]*"
            i += 1
        else:
            # a normal character (like a letter or a dot) is escaped and matched literally
            regex += re.escape(pattern[i])
            i += 1
    # Anchor with ^ and $ so the pattern must match the whole path, not just part of it
    return "^" + regex + "$"


def match_path(pattern, path):
    """This test will return true if a glob which is converted to regex matches the path"""
    return re.match(globe_to_regex(pattern), path) is not None


# converted to boolean just to get True or False outputs
