def get_gps_list(up_left, down_left, down_right, vertical_count, horizontal_count):
    result = []
    vertical_interval = (
        (up_left[0] - down_left[0]) / (vertical_count - 1.0), (up_left[1] - down_left[1]) / (vertical_count - 1.0))
    horizontal_interval = ((down_right[0] - down_left[0]) / (horizontal_count - 1.0)), (
        (down_right[1] - down_left[1]) / (horizontal_count - 1.0))

    print vertical_interval, horizontal_interval

    for i in xrange(vertical_count):
        for j in xrange(horizontal_count):
            result.append((down_left[0] + i * vertical_interval[0] + j * horizontal_interval[0],
                           down_left[1] + i * vertical_interval[1] + j * horizontal_interval[1]))

    return result
