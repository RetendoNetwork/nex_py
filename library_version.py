import semver


class LibraryVersion:
    def __init__(self, major: int, minor: int, patch: int, game_specific_patch: str):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.game_specific_patch = game_specific_patch
        self.semver = f"v{major}.{minor}.{patch}"

    def copy(self):
        return LibraryVersion(
            self.major,
            self.minor,
            self.patch,
            self.game_specific_patch
        )

    def semver_compare(self, compare: str):
        if not compare.startswith("v"):
            compare = "v" + compare

        if not semver.VersionInfo.is_valid(compare):
            return 0

        return semver.compare(self.semver, compare)

    def greater_or_equal(self, compare):
        return self.semver_compare(compare) != -1

    def less_or_equal(self, compare):
        return self.semver_compare(compare) != 1

    @staticmethod
    def new_patched_library_version(major, minor, patch, game_specific_patch):
        return LibraryVersion(major, minor, patch, game_specific_patch)

    @staticmethod
    def new_library_version(major, minor, patch):
        return LibraryVersion(major, minor, patch)


class LibraryVersions:
    def __init__(self):
        self.main = LibraryVersion
        self.data_store = LibraryVersion
        self.match_making = LibraryVersion
        self.ranking = LibraryVersion
        self.ranking2 = LibraryVersion
        self.messaging = LibraryVersion
        self.utility = LibraryVersion
        self.nat_traversal = LibraryVersion

    def set_default(self, version: LibraryVersion):
        self.main = version
        self.data_store = version.copy()
        self.match_making = version.copy()
        self.ranking = version.copy()
        self.ranking2 = version.copy()
        self.messaging = version.copy()
        self.utility = version.copy()
        self.nat_traversal = version.copy()

    @staticmethod
    def new_library_versions():
        return LibraryVersions()