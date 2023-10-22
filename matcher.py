"""Module providing member to job matching"""

from collections import defaultdict
import model


def match_members_to_jobs(
    member_data: dict, jobs_data: dict[str, list[model.Job]]
) -> dict[str, list[dict]]:
    """Matches members to jobs based on members' preferences"""
    matched_jobs: dict[str, list[dict]] = defaultdict(list)
    for member_name in member_data:
        for location in member_data[member_name].locations:
            matched_jobs[member_name] += [
                job.original_data
                for job in jobs_data[location]
                if any(
                    desired_job in job.title
                    for desired_job in member_data[member_name].jobs
                )
            ]
    return matched_jobs
