from libulb.catalog.course import Course


def test_simple_course():
    course = Course.get_from_slug('info-f-101', "201617")

    assert course.slug == "info-f-101"
    assert course.name == "Programmation"
    assert len(course.profs) == 1
    assert course.language == "french"
