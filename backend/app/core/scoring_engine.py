def score_structure(structure) -> int:
    score = 0

    if structure.has_readme:
        score += 4
    if structure.has_tests:
        score += 4
    if structure.has_ci:
        score += 3
    if structure.max_depth <= 4:
        score += 4

    return min(score, 15)


def score_code_quality(code) -> int:
    score = 0

    if code.pylint_score:
        if code.pylint_score >= 8:
            score += 10
        elif code.pylint_score >= 6:
            score += 6
        else:
            score += 3

    if code.average_complexity <= 3:
        score += 10
    elif code.average_complexity <= 5:
        score += 6
    else:
        score += 3

    if not code.high_complexity_files:
        score += 5

    return min(score, 25)


def score_documentation(doc) -> int:
    score = 0

    if doc.has_readme:
        score += 5
    if doc.has_installation:
        score += 3
    if doc.has_usage:
        score += 3
    if doc.doc_to_code_ratio >= 0.1:
        score += 4

    return min(score, 15)


def score_testing(testing) -> int:
    score = 0

    if testing.has_tests:
        score += 5
    if testing.test_files_count >= 5:
        score += 5
    elif testing.test_files_count >= 2:
        score += 3

    if testing.has_coverage:
        score += 5

    return min(score, 15)


def score_git_practices(git) -> int:
    score = 0

    if git.total_commits >= 10:
        score += 5
    elif git.total_commits >= 3:
        score += 3

    if git.commit_message_quality == "good":
        score += 5
    elif git.commit_message_quality == "average":
        score += 3

    if git.has_multiple_branches:
        score += 3
    if git.has_pull_requests:
        score += 2

    return min(score, 15)


def score_maintainability(code, doc, testing) -> int:
    score = 0

    if code.average_complexity <= 3:
        score += 5
    if doc.doc_to_code_ratio >= 0.1:
        score += 5
    if testing.has_tests:
        score += 5

    return min(score, 15)


from backend.app.models.analysis_models import ScoreBreakdown

def calculate_final_score(structure, code, doc, testing, git) -> ScoreBreakdown:
    s_structure = score_structure(structure)
    s_code = score_code_quality(code)
    s_doc = score_documentation(doc)
    s_test = score_testing(testing)
    s_git = score_git_practices(git)
    s_maintain = score_maintainability(code, doc, testing)

    total = (
        s_structure +
        s_code +
        s_doc +
        s_test +
        s_git +
        s_maintain
    )

    if total >= 75:
        level = "Advanced"
        badge = "Gold"
    elif total >= 45:
        level = "Intermediate"
        badge = "Silver"
    else:
        level = "Beginner"
        badge = "Bronze"

    return ScoreBreakdown(
        structure=s_structure,
        code_quality=s_code,
        documentation=s_doc,
        testing=s_test,
        git_practices=s_git,
        maintainability=s_maintain,
        total_score=total,
        level=level,
        badge=badge
    )
