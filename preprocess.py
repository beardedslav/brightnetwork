"""Preprocessing of member and job data"""

from collections import defaultdict
import string

import model

_punctuation_translator = str.maketrans("", "", string.punctuation)


def _lowercase_strip_punctuation_and_split(str_: str) -> set[str]:
    return set(str_.lower().translate(_punctuation_translator).split(" "))


def members(members_data: list[dict[str, str]]) -> dict[str, model.Member]:
    """Preprocess member data: find preferred locations and jobs"""
    known_locations = {"london", "edinburgh", "manchester", "york"}
    known_jobs = {"internship", "marketing", "design", "software", "designer"}

    preprocessed_members = {
        member["name"]: model.Member(
            member["name"],
            known_locations & _lowercase_strip_punctuation_and_split(member["bio"]),
            known_jobs & _lowercase_strip_punctuation_and_split(member["bio"]),
            member,
        )
        for member in members_data
    }

    return preprocessed_members


def jobs(jobs_data: list[dict[str, str]]) -> dict[str, list[model.Job]]:
    """Preprocess job data by aggregating jobs by their location"""
    jobs_dict = defaultdict(list)
    for job in jobs_data:
        jobs_dict[job["location"].lower()].append(
            model.Job(job["title"].lower(), job["location"].lower(), job)
        )
    return jobs_dict
