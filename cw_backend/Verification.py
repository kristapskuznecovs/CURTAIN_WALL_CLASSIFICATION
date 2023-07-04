def correct_amount_of_beams(element):
    if len(element.profiles) < 4:
        return False
    return True


def any_profile_is_vertical(element):
    for profile in element.profiles:
        if abs(profile.start.z - profile.end.z)>50:
            return True
    return False


def valid_or_invalid_elements(elements):

    element_list_copy = elements[:]
    bad_elements = []

    for element in element_list_copy:
        profile_count = correct_amount_of_beams(element)
        vertical = any_profile_is_vertical(element)

        if not profile_count or not vertical:
            elements.remove(element)
            bad_elements.append(element)

    return elements, bad_elements

