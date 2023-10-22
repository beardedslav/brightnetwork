"""Module providing named tuples used to hold the job and member data"""
from collections import namedtuple

Job = namedtuple("Job", ["title", "location", "original_data"])
Member = namedtuple("Member", ["name", "locations", "jobs", "original_data"])
