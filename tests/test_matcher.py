"""Unit tests for members to jobs matching"""
from collections import defaultdict
import matcher
from model import Job, Member


def test_match_members_to_jobs_no_members_no_jobs():
    assert len(matcher.match_members_to_jobs({}, {})) == 0


def test_match_members_to_jobs_no_jobs():
    matched_data = matcher.match_members_to_jobs(
        {"John Doe": Member("John Doe", ["glasgow"], ["ceo"], "")}, defaultdict(list)
    )
    assert len(matched_data) == 1
    assert len(matched_data["John Doe"]) == 0


def test_match_members_to_jobs_no_members() -> None:
    assert (
        len(matcher.match_members_to_jobs({}, {"glasgow": [Job("cto", "glasgow", "")]}))
        == 0
    )


def test_match_members_to_jobs() -> None:
    matched_data = matcher.match_members_to_jobs(
        {"John Doe": Member("John Doe", ["glasgow"], ["ceo"], "")},
        {"glasgow": [Job("ceo", "glasgow", "")]},
    )
    assert len(matched_data) == 1
    assert len(matched_data["John Doe"]) == 1
