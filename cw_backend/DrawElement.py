import cv2
import numpy as np


def draw_element(element, debug=False):
    # Create a blank image with size 5000x3000 and 3 channels (RGB)

    width = 0
    height = 0

    width_arr = [0]

    for plane in element.element_planes:

        if debug:
            print(f'{len(plane.all_profiles)} profiles in plane')

        width += int(plane.width)
        width_arr.append(int(plane.width))
        height = int(plane.height)

    height += 500
    width += 500

    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    i = 0

    colour_ar = [[255, 0, 0],
                 [0, 0, 255],
                 [0, 255, 0],
                 [255, 255, 0],
                 [0, 255, 255],
                 [100, 100, 100]]

    def add_openings_as_rectangle(opening, img, hor_offset, color, level, global_height, global_width):
        # print(level)
        # print(opening)
        this_colour = color[level]
        r, g, b = this_colour[0], this_colour[1], this_colour[2]
        origin = opening.origin
        height = int(global_height)
        width = int(global_width)
        tolerance = 50
        # print(f'Drawing origing: {origin}')
        x1 = int(origin.x + 250 + hor_offset + tolerance)
        y1 = int(-origin.y + 250 + height - tolerance)
        x2 = int(x1 + opening.width - 2 * tolerance)
        y2 = int(y1 - opening.height + 2 * tolerance)
        cv2.rectangle(img, (x1, y1), (x2, y2), (b, g, r), -1)

        if len(opening.children) == 0:
            cv2.circle(img, (opening.center.x + 250 + hor_offset, -opening.center.y + 250 + height), 50, (0, 0, 0), 10)

        for child_opening in opening.children:
            add_openings_as_rectangle(child_opening, img, hor_offset, color, level + 1, global_height, global_width)

    for plane in element.element_planes:

        depth = 0

        temp_colour = colour_ar[i]

        r, g, b = temp_colour[0], temp_colour[1], temp_colour[2]

        add_openings_as_rectangle(plane.opening, img, width_arr[i], colour_ar, depth, plane.height, plane.width)

        for profile in plane.all_profiles:
            x1 = int(profile.start.x + 250 + width_arr[i])
            y1 = int(-profile.start.y + height - 250)
            x2 = int(profile.end.x + 250 + width_arr[i])
            y2 = int(-profile.end.y + height - 250)

            cv2.line(img, (x1, y1), (x2, y2), (b, g, r), 20)

        i += 1

    # Scale down the image to a particular height in pixels (e.g. 500 pixels)
    height = 500
    scale = height / img.shape[0]
    width = int(img.shape[1] * scale)
    dim = (width, height)
    img_resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # Display the original image and the resized image
    # cv2.imshow('Original Image', img)
    cv2.imshow('Resized Image', img_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
