from typing import Optional
import semver


class LibraryVersion:
    def __init__(self, major: int, minor: int, patch: int, game_specific_patch: str = ""):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.game_specific_patch = game_specific_patch
        self.semver = f"v{major}.{minor}.{patch}"

    def copy(self) -> 'LibraryVersion':
        """Returns a new copied instance of LibraryVersion."""
        return LibraryVersion(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            game_specific_patch=self.game_specific_patch,
        )

    def semver_compare(self, compare: str) -> int:
        """Compares the current version with the provided version string."""
        if not compare.startswith("v"):
            compare = f"v{compare}"

        if not semver.VersionInfo.isvalid(compare):
            return 0  # Invalid semver comparison returns 0 (equal)

        return semver.compare(self.semver, compare)

    def greater_or_equal(self, compare: str) -> bool:
        """Checks if the current version is greater than or equal to the provided version."""
        return self.semver_compare(compare) != -1

    def less_or_equal(self, compare: str) -> bool:
        """Checks if the current version is less than or equal to the provided version."""
        return self.semver_compare(compare) != 1

    @staticmethod
    def new_patched_library_version(major: int, minor: int, patch: int, game_specific_patch: str) -> 'LibraryVersion':
        """Creates a new LibraryVersion with a game-specific patch."""
        return LibraryVersion(major, minor, patch, game_specific_patch)


class LibraryVersions:
    def __init__(self):
        self.main: Optional[LibraryVersion] = None
        self.datastore: Optional[LibraryVersion] = None
        self.matchmaking: Optional[LibraryVersion] = None
        self.ranking: Optional[LibraryVersion] = None
        self.ranking2: Optional[LibraryVersion] = None
        self.messaging: Optional[LibraryVersion] = None
        self.utility: Optional[LibraryVersion] = None
        self.nat_traversal: Optional[LibraryVersion] = None

    def set_default(self, version: LibraryVersion):
        """Sets the default NEX protocol versions for all components."""
        self.main = version
        self.datastore = version.copy()
        self.matchmaking = version.copy()
        self.ranking = version.copy()
        self.ranking2 = version.copy()
        self.messaging = version.copy()
        self.utility = version.copy()
        self.nat_traversal = version.copy()