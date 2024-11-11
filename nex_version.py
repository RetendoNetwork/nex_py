import semver


def create_nex_version(major, minor, patch, game_specific_patch=None):
    version = {
        "Major": major,
        "Minor": minor,
        "Patch": patch,
        "GameSpecificPatch": game_specific_patch,
        "semver": f"v{major}.{minor}.{patch}"
    }
    return version


def copy_nex_version(nex_version):
    return {
        "Major": nex_version["Major"],
        "Minor": nex_version["Minor"],
        "Patch": nex_version["Patch"],
        "GameSpecificPatch": nex_version["GameSpecificPatch"],
        "semver": f"v{nex_version['Major']}.{nex_version['Minor']}.{nex_version['Patch']}"
    }


def semver_compare(nex_version, compare):
    if not compare.startswith("v"):
        compare = "v" + compare

    if not semver.validate(compare):
        return 0  # If the version is invalid

    return semver.compare(nex_version["semver"], compare)


def greater_or_equal(nex_version, compare):
    return semver_compare(nex_version, compare) != -1


def less_or_equal(nex_version, compare):
    return semver_compare(nex_version, compare) != 1


def new_patched_nex_version(major, minor, patch, game_specific_patch):
    return create_nex_version(major, minor, patch, game_specific_patch)


def new_nex_version(major, minor, patch):
    return create_nex_version(major, minor, patch)