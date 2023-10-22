"""Unit tests for preprocessing member and job data"""
import preprocess


def _members_test_data(
    job: str = "software engineer", location: str = "Edinburgh"
) -> list[dict]:
    return [{"name": "John Doe", "bio": f"I am a {job} from {location}"}]


def _jobs_test_data(
    second_job_title: str = "Financial advisor", second_job_location: str = "Hamilton"
) -> list[dict]:
    return [
        {"title": "Solicitor", "location": "Hamilton"},
        {"title": second_job_title, "location": second_job_location},
    ]


def test_process_lowercase_strip_punctuation_and_split() -> None:
    assert preprocess._lowercase_strip_punctuation_and_split("Yes.") == {"yes"}
    assert preprocess._lowercase_strip_punctuation_and_split("Yes, but no.") == {
        "yes",
        "but",
        "no",
    }
    assert preprocess._lowercase_strip_punctuation_and_split("") == {""}
    assert preprocess._lowercase_strip_punctuation_and_split(" ") == {""}
    assert preprocess._lowercase_strip_punctuation_and_split("Yes, .;") == {"yes", ""}


def test_members_unknown_location() -> None:
    preprocessed_members = preprocess.members(_members_test_data(location="Glasgow"))
    assert preprocessed_members["John Doe"].locations == set()


def test_members_unknown_job() -> None:
    processed_members = preprocess.members(
        _members_test_data(job="mechanical engineer")
    )
    assert processed_members["John Doe"].jobs == set()


def test_members() -> None:
    processed_members = preprocess.members(_members_test_data())
    assert processed_members["John Doe"].locations == {"edinburgh"}
    assert processed_members["John Doe"].jobs == {"software"}


def test_jobs() -> None:
    assert len(preprocess.jobs([])) == 0


def test_jobs_aggregated_by_location() -> None:
    preprocessed_jobs = preprocess.jobs(_jobs_test_data())
    assert len(preprocessed_jobs) == 1
    assert len(preprocessed_jobs["hamilton"]) == 2


def test_two_jobs_with_the_same_title_are_not_treated_as_duplicate() -> None:
    preprocessed_jobs = preprocess.jobs(_jobs_test_data(second_job_title="Solicitor"))
    assert len(preprocessed_jobs["hamilton"]) == 2


def test_two_jobs_with_the_same_title_and_different_locations_are_not_aggregated_by_location() -> (
    None
):
    preprocessed_jobs = preprocess.jobs(
        _jobs_test_data(second_job_title="Solicitor", second_job_location="Glasgow")
    )
    assert len(preprocessed_jobs) == 2
    assert len(preprocessed_jobs["hamilton"]) == 1
    assert len(preprocessed_jobs["glasgow"]) == 1
