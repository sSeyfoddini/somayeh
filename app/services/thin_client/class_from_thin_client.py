from app.persistence.credential_schema_tables_persistence.course_persistence import CoursePersistence
from app.services.thin_client_service import ClassService
from app.persistence.credential_schema_tables_persistence.class_persistence import ClassPersistence, ClassModel


class Class:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        input = {"strm": "2204",
                 "class_nbr": "44635"}
        page = 1
        uri = "https://catalog.apps.asu.edu/catalog/classes/classlist?advanced=tru"
        responses = []

        while True:
            response = ClassService.get(input, page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

          # ClassPersistence.delete_all()

        for response in responses:
            for data in response:
                course, _, _ = CoursePersistence.get_all_by_filter({"external_id": str(data["crse_offer_nbr"])})
                course_id = None
                if course:
                    course_id = course[0].uuid

                _class = ClassModel(
                    external_class_id=data["crse_offer_nbr"],
                    course_id=course_id,
                    external_course_id="",
                    instructor_id=data["instructor_id"],
                    session_id=data["session_code"],
                    term_id=data["strm"],
                    topic=data["print_topic"],
                    reference_uri=uri+"&classNbr={}&searchType=all&term={}".format(data["catalog_nbr"], data["strm"]),
                    delivery_id=None,
                    location_id=None
                )
                ClassPersistence.add(user_id, user_name, _class)