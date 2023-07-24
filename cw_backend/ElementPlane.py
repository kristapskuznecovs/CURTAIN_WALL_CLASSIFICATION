import math

import Opening
import Profile
import Geometry


class ElementPlane:
    def __init__(self, bottom_beam, all_profiles):
        self.bottom_beam = bottom_beam
        self.all_profiles = all_profiles
        self.height = 0
        self.width = 0
        self.opening = ""
        self.plane = generate_plane_from_bottom_beam(bottom_beam, all_profiles)

    def __str__(self):
        return f'{self.height:>9} x {self.width:<9} Plane: {self.plane}'

    def generate_size(self):
        """
        Possible problem, currently size is generated from middle points.
        Possible cases with missing edge beams should be looked into.
        :return:
        """
        height = self.height
        width = self.width

        for profile in self.all_profiles:
            horizontal = max(profile.start.x, profile.end.x)
            vertical = max(profile.start.y, profile.end.y)

            if vertical > height:
                height = vertical
            if horizontal > width:
                width = horizontal

        self.height = height
        self.width = width

    def generate_openings(self):
        profiles = self.all_profiles[:]
        opening = Opening.Opening(self.height, self.width, Geometry.Point(0, 0, 0), self.all_profiles, self.plane,
                                  level=0)
        self.opening = opening
        opening.top = Profile.find_H_profile_at_y_pos(self.height, profiles)
        opening.bottom = Profile.find_H_profile_at_y_pos(0, profiles)
        opening.left = Profile.find_V_profile_at_x_pos(0, profiles)
        opening.right = Profile.find_V_profile_at_x_pos(self.width, profiles)

        if opening.top is not None:
            profiles.remove(opening.top)
        if opening.bottom is not None:
            profiles.remove(opening.bottom)
        if opening.left is not None:
            profiles.remove(opening.left)
        if opening.right is not None:
            profiles.remove(opening.right)

        opening.profiles_inside = profiles
        level = 1
        Opening.recursion_split_openings(opening, profiles, level)


def generate_plane_from_bottom_beam(bottom_beam, all_profiles):
    start = bottom_beam.start
    end = bottom_beam.end
    origin = bottom_beam.start
    x0 = start.x
    y0 = start.y
    z0 = start.z
    x1 = end.x
    y1 = end.y
    z1 = end.z

    x_vector = Geometry.Vector(x1 - x0, y1 - y0, z1 - z0)

    vertical_profile = find_most_vertical_profile(all_profiles)

    v_z_start = vertical_profile.start.z
    v_z_end = vertical_profile.end.z

    if v_z_start < v_z_end:
        v_start = vertical_profile.start
        v_end = vertical_profile.end
    else:
        v_start = vertical_profile.end
        v_end = vertical_profile.start

    v_x0 = v_start.x
    v_y0 = v_start.y
    v_z0 = v_start.z

    v_x1 = v_end.x
    v_y1 = v_end.y
    v_z1 = v_end.z

    y_vector = Geometry.Vector(v_x1 - v_x0, v_y1 - v_y0, v_z1 - v_z0)

    return Geometry.Plane(origin, x_vector, y_vector)


def find_most_vertical_profile(all_profiles):
    def get_ratio(profile):
        start = profile.start
        end = profile.end

        dif_x = end.x - start.x
        dif_y = end.y - start.y
        dif_z = abs(end.z - start.z)

        horizontal = math.sqrt(dif_x ** 2 + dif_y ** 2)
        if horizontal < 1:
            horizontal = 1
        vertical = dif_z
        ratio = vertical / horizontal

        return ratio

    vertical_profile = all_profiles[0]
    ratio = get_ratio(vertical_profile)

    for profile in all_profiles[1:]:
        temp_ratio = get_ratio(profile)

        if temp_ratio > ratio:
            ratio = temp_ratio
            vertical_profile = profile
    return vertical_profile


def sort_profiles_by_planes(bottom_profiles, all_profiles):
    result = []
    for _ in bottom_profiles:
        result.append([])
    for profile in all_profiles:
        if len(bottom_profiles) == 1:
            result[0].append(profile)
            continue

        if len(bottom_profiles) == 2:

            first = bottom_profiles[0]

            distance1, closest_point1 = Geometry.distance_point_to_line(profile.middle_point, first)
            closest_point1 = Geometry.Point(closest_point1[0], closest_point1[1], closest_point1[2])
            distance_to_start = Geometry.distance_2pt(closest_point1, first.start)
            if distance_to_start < first.length + 10:
                within_first = True
            else:
                within_first = False

            second = bottom_profiles[1]

            distance2, closest_point2 = Geometry.distance_point_to_line(profile.middle_point, second)
            closest_point2 = Geometry.Point(closest_point2[0], closest_point2[1], closest_point2[2])
            distance_to_end = Geometry.distance_2pt(closest_point2, second.end)

            if distance_to_end < second.length + 10:
                within_second = True
            else:
                within_second = False

            if within_first and not within_second:
                result[0].append(profile)
                continue

            elif not within_first and within_second:
                result[1].append(profile)
                continue

            else:
                if distance1 < distance2:
                    result[0].append(profile)
                    continue
                else:
                    result[1].append(profile)
    return result
