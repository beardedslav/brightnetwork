# Bright Network Hiring Challenge

## Approach taken

The solution matches the members to potential jobs by following this process:

1. Fetch the members and jobs data from the API
2. Preprocess the data
3. Use the preprocessed data to find matches

### Fetching the data

I decided to use *[HTTPX](https://www.python-httpx.org/)* library, mostly due to its support for async programming (even though I didn't leverage async programming in this solution). An alternative that could have been considered is *[AIOHTTP](https://docs.aiohttp.org/en/stable/)*, however AIOHTTP requires usage of async programming. I decided against using *[Requests](https://requests.readthedocs.io/en/latest/)* as it only supports HTTP/1.1 and doesn't support async.

#### Limitations and future improvements

As already mentioned the current approach means that every request will block further execution of the program, which isn't a problem with the amount of data being fetched in the exercise. This could be addressed by using *[asyncio](https://docs.python.org/3/library/asyncio.html)* or *[trio](https://trio.readthedocs.io/en/stable/)* and `httpx.AsyncClient`.

The error handling is currently limited to non-2xx HTTP codes, it should be extended to cover connectivity issues (like request timeouts) and malformed JSON responses.

As it stands the `BrightNetworkChallengeClient` class isn't unit tested. Unit testing it would require mocking the `httpx.Client` class, as unit tests shouldn't depend on connectivity to a real server.

### Preprocessing the data

All of the data used for matching is converted to lowercase to allow case insensitive matching.

For each member their bio is stripped of any punctuation and split into singular words (tokens). Due to use of sets (this is to speed up location and job preferences detection) duplicate words will be removed. Member's preferred locations are determined by simply scanning their tokenised bio against a set of known locations, which I prepared based on the test data. Prefered jobs are determined in the same way. Jobs are aggregated into a dictionary keyed by location, allowing to filter jobs by member's preferred locations first.

#### Limitations and future improvements

The selected approach is very basic and not fit for production usage, as any new members looking for jobs in new locations or new types of jobs would require changes to the code. It also assumes that just a mention of a location means a member wants to work there, meaning preferences like "outside of London" or "currently in Edinburgh but looking to relocate to London" won't be properly addressed. This could be improved with a use of natural language processing or even a large language model.

Similarly to fetching the data preprocessing could be moved to async execution. It's not a concern for such small datasets as the one used in the challenge, but when dealing with much larger datasets in production preprocessing could be paralellised or even moved to a separate service(s).

### Matching members and jobs

The chosen approach is to check if any of the jobs if any of the members' preferred locations match their preferences (currently being tied to a predefined set of keywords).

#### Limitations and future improvements

The negative preferences like "outside of London" are not taken into consideration. The existing job data structure (location keyed dictionary) might not work well with negative location preferences. This could maybe be addressed by use of a geospatial data structure, however it's not something I'm familiar with.

## Overall future improvements

If this were a production system it would definitely benefit from additional automated tests, like end to end, integaration, and component tests. These tests could also be integrated into CI/CD pipelines.

Results of preprocessing and matching aren't stored, meaning if a new user registers or a new job is added all of the preprocessing and matching has to be repeated.

Current implementation relies on high quality of the data, meaning it won't account for things like spelling mistakes.
