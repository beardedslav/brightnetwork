"""Bright Network Hiring Challenge"""
import logging

from client import BrightNetworkHiringChallengeClient
import preprocess
import matcher


logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.ERROR,
)


def main() -> None:
    client = BrightNetworkHiringChallengeClient()
    members_response = client.retrieve_members()
    jobs_response = client.retrieve_jobs()
    members_data = preprocess.members(members_response)
    jobs_data = preprocess.jobs(jobs_response)
    matched_data = matcher.match_members_to_jobs(members_data, jobs_data)

    for member_name in matched_data:
        print("========================")
        print("Member: " + member_name)
        print("Matched jobs: " + str(matched_data[member_name]))
        print("========================")


if __name__ == "__main__":
    main()
