import Geometry
import Profile
import ElementPlane


# Element objects are first created as "dumb" objects only containing GUID, and added profiles to the profiles list
# Afterwards, profiles are sorted into "dumb" element planes
# Lastly element planes are split into openings
class Element:
    def __init__(self, guid):
        self.guid = guid
        self.profiles = []
        self.element_planes = []
        self.plane_count = 0

    def __str__(self):
        return f'{self.guid} | {len(self.profiles)}'

    def generate_planes(self):
        bottom_profiles = Profile.find_bottom_beams(self.profiles)

        if len(bottom_profiles) > 1:
            Profile.sort_bottom_profiles(bottom_profiles)

        profiles_by_planes = ElementPlane.sort_profiles_by_planes(bottom_profiles, self.profiles)

        # Create element plane "dumb" objects
        for _ in range(len(profiles_by_planes)):
            bottom_profile = bottom_profiles.pop(0)
            all_profiles_on_plane = profiles_by_planes.pop(0)
            self.element_planes.append(ElementPlane.ElementPlane(bottom_profile, all_profiles_on_plane))

        # Orient coordinates to plane local coordinate system
        for element_plane in self.element_planes:
            target_plane = element_plane.plane
            for profile in element_plane.all_profiles:
                profile.start = Geometry.get_local_coordinate(profile.start, target_plane)
                profile.end = Geometry.get_local_coordinate(profile.end, target_plane)
                profile.direction = profile.get_direction_local()
                profile.orient_points()

        self.plane_count = len(self.element_planes)

