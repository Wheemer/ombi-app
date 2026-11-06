import sys

import atheris

with atheris.instrument_imports(include=["update_ombi"]):
    from update_ombi import normalize_version, version_key


@atheris.instrument_func
def fuzz_release_tag(data: bytes) -> None:
    tag = data.decode("utf-8", errors="replace")
    version = tag.removeprefix("v")
    parts = version.split(".")
    valid = len(parts) == 3 and all(part.isascii() and part.isdigit() for part in parts)
    assert normalize_version(tag) == (version if valid else None)
    if valid:
        assert version_key(version) == tuple(map(int, parts))


if __name__ == "__main__":
    for seed in (b"v4.60.20", b"4.53.10", b"build-v4.60.20", b"v4.60.20.1", b"v4.60.20\n"):
        fuzz_release_tag(seed)
    atheris.Setup(sys.argv, fuzz_release_tag)
    atheris.Fuzz()
