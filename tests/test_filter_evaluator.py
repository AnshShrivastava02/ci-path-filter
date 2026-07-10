from src.filter_evaluator import evaluate_filter, evaluate_all

"""Focusing these  tests on the cases that reveal real
    logic decisions, the segment rules,
    exclusion precedence, empty inputs, and filters """


PATTERNS = ["app/src/**/*.kt", "!app/src/test/**"]


def test_file_that_survives_makes_filter_true():
    # Payment.kt is included and not excluded -> filter is true
    files = ["app/src/test/PaymentTest.kt", "app/src/main/Payment.kt"]
    assert evaluate_filter(PATTERNS, files) is True


def test_only_excluded_file_makes_filter_false():
    # the single changed file matches the include BUT also the exclude -> false
    files = ["app/src/test/PaymentTest.kt"]
    assert evaluate_filter(PATTERNS, files) is False


def test_excluded_plus_unrelated_file_is_false():
    # one file is excluded, the other doesn't match the include at all -> false
    files = ["app/src/test/PaymentTest.kt", "docs/README.md"]
    assert evaluate_filter(PATTERNS, files) is False


def test_no_matching_files_is_false():
    # nothing matches the include -> false
    files = ["web/app.ts"]
    assert evaluate_filter(PATTERNS, files) is False


def test_evaluate_all_returns_result_per_filter():
    # evaluate_all should return a dict with one True/False per filter
    filters = {
        "backend": ["app/src/**/*.kt", "!app/src/test/**"],
        "docs": ["README.md", "docs/**/*.md"],
    }
    changed = ["app/src/main/Payment.kt", "README.md"]
    results = evaluate_all(filters, changed)
    assert results == {"backend": True, "docs": True}


def test_empty_changed_files_is_false():
    # no files changed -> nothing can survive -> false
    assert evaluate_filter(PATTERNS, []) is False


def test_only_exclude_patterns_is_false():
    # a filter with only excludes and no includes -> nothing is included -> false
    only_excludes = ["!app/src/test/**"]
    assert evaluate_filter(only_excludes, ["app/src/main/Payment.kt"]) is False


def test_multiple_filters_and_multiple_patterns():
    # a realistic config: several filters, several patterns each
    filters = {
        "backend": ["app/src/**/*.kt", "!app/src/test/**"],
        "frontend": ["web/**/*.ts", "web/**/*.tsx"],
        "docs": ["README.md", "docs/**/*.md"],
        "tests": ["**/test/**/*.kt"],
    }

    changed = ["web/components/Button.tsx", "docs/setup.md"]
    results = evaluate_all(filters, changed)
    # only frontend and docs changed; backend and tests did not
    assert results == {
        "backend": False,
        "frontend": True,
        "docs": True,
        "tests": False,
    }
