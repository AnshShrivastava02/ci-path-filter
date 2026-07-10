from src.glob_matcher import match_path


def test_single_star_stays_in_one_segment():
    # * should match within a segment but not cross a slash
    assert match_path("*.md", "guide.md") is True
    assert match_path("*.md", "docs/guide.md") is False


def test_double_star_crosses_segments():
    # ** should match across any number of folders
    assert match_path("web/**/*.ts", "web/components/button/index.ts") is True


def test_double_star_matches_zero_segments():
    # ** should also match when there are NO folders in between
    assert match_path("app/src/**/*.kt", "app/src/Payment.kt") is True


def test_literal_dot_is_not_a_wildcard():
    # the dot in .kt should be a literal dot, not "any character"
    assert match_path("*.kt", "Payment.kt") is True
    assert match_path("*.kt", "PaymentXkt") is False


def test_exact_filename_match():
    assert match_path("README.md", "README.md") is True
    assert match_path("README.md", "src/README.md") is False
