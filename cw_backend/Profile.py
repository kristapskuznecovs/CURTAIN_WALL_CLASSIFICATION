import Geometry


class Profile:
    def __init__(self, profile, length, guid, start_x, start_y, start_z, end_x, end_y, end_z):
        self.profile = profile
        self.length = length
        self.guid = guid
        self.start = Geometry.Point(start_x, start_y, start_z)
        self.global_start = Geometry.Point(start_x, start_y, start_z)
        self.end = Geometry.Point(end_x, end_y, end_z)
        self.global_end = Geometry.Point(end_x, end_y, end_z)
        self.direction = self.get_direction()

    def orient_points(self):
        if self.direction == 'V':
            if self.start.y > self.end.y:
                self.start, self.end = self.end, self.start
        if self.direction == 'H':
            if self.start.x > self.end.x:
                self.start, self.end = self.end, self.start

    def __str__(self):
        return f'|{self.direction:>4} | {self.start} | {self.end} | {self.guid} {self.middle_point}'

    def get_direction(self):
        if abs(self.start.z - self.end.z) < 1:
            return 'H'
        if abs(self.start.x - self.end.x) < 1 and abs(self.start.y - self.end.y) < 1:
            return 'V'
        return "Diagonal"

    def get_direction_local(self):
        if abs(self.start.y - self.end.y) < 1:
            return 'H'
        if abs(self.start.x - self.end.x) < 1:
            return 'V'
        return "Diagonal"

    @property
    def middle_point(self):
        middle_x = self.start.x + (self.end.x - self.start.x) / 2
        middle_y = self.start.y + (self.end.y - self.start.y) / 2
        middle_z = self.start.z + (self.end.z - self.start.z) / 2
        return Geometry.Point(middle_x, middle_y, middle_z)


def find_vertical_profile(y_pos, all_profiles):
    for profile in all_profiles:
        # print(profile.middle_point.y)
        if abs(profile.middle_point.y - y_pos) < 1:
            # print('Returning profile')
            return profile
    return None


def find_horizontal_profile(x_pos, all_profiles):
    for profile in all_profiles:
        if abs(profile.middle_point.x - x_pos) < 1:
            return profile
    return None


def find_bottom_beams(profiles):
    bottom_profiles = [profiles[0]]

    for profile in profiles[1:]:

        if profile.middle_point.z < bottom_profiles[0].middle_point.z - 100:
            bottom_profiles = [profile]

        elif bottom_profiles[0].middle_point.z - 100 < profile.middle_point.z < bottom_profiles[0].middle_point.z + 100:
            bottom_profiles.append(profile)
    return bottom_profiles


def sort_bottom_profiles(bottom_profiles):
    if len(bottom_profiles) > 1:
        first = bottom_profiles[0]
        second = bottom_profiles[1]

        distance1 = Geometry.distance_2pt(first.end, second.start)
        distance2 = Geometry.distance_2pt(second.end, first.start)

        if distance2 < distance1:
            bottom_profiles.reverse()
