from app.model.relations_model.credit_recognition_model import CreditRecognitionModel
from app.persistence.relations_persistence.credit_recognition_persistence import CreditRecognitionPersistence
from app.util.error_handlers import RecordNotFound

class CreditRecognitionService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credit_recognition_type_id,
        credit_recognition_name,
        credit_recognition_category_id,
        credit_recognition_keywords,
        conferring_credential,
        conferring_identifier,
        supporting_credential,
    ):

        credit_recognition = CreditRecognitionModel(
            credit_recognition_type_id=credit_recognition_type_id,
            credit_recognition_name=credit_recognition_name,
            credit_recognition_category_id=credit_recognition_category_id,
            credit_recognition_keywords=credit_recognition_keywords,
            conferring_credential=conferring_credential,
            conferring_identifier=conferring_identifier,
            supporting_credential=supporting_credential,
        )
        credit_recognition = CreditRecognitionPersistence.add(user_id, user_name, credit_recognition)
        return credit_recognition

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        id,
        args
    ):
        credit_recognition = CreditRecognitionPersistence.get(id)

        if credit_recognition is None:
            raise RecordNotFound("'credit recognition' with uuid'{}' not found.".format(id))

        credit_recognition = CreditRecognitionModel(
            id=id,
            credit_recognition_type_id=args.get("credit_recognition_type_id", credit_recognition.credit_recognition_type_id),
            credit_recognition_name=args.get("credit_recognition_name", credit_recognition.credit_recognition_name),
            credit_recognition_category_id=args.get("credit_recognition_category_id", credit_recognition.credit_recognition_category_id),
            credit_recognition_keywords=args.get("credit_recognition_keywords", credit_recognition.credit_recognition_keywords),
            conferring_credential=args.get("conferring_credential", credit_recognition.conferring_credential),
            conferring_identifier=args.get("conferring_identifier", credit_recognition.conferring_identifier),
            supporting_credential=args.get("supporting_credential", credit_recognition.supporting_credential),
        )
        credit_recognition = CreditRecognitionPersistence.update(user_id, user_name, credit_recognition)

        return credit_recognition

    @classmethod
    def delete(cls, user_id, user_name, credit_recognition):
        CreditRecognitionPersistence.delete(user_id, user_name, credit_recognition)
        return credit_recognition

    @classmethod
    def delete_by_id(cls, user_id, user_name, id):
        credit_recognition = CreditRecognitionPersistence.get(id)
        if credit_recognition is None:
            raise RecordNotFound("'credit recognition' with id'{}' not found.".format(id))
        CreditRecognitionPersistence.delete(user_id, user_name, credit_recognition)
        return credit_recognition

    @classmethod
    def get(cls, id):
        credit_recognition = CreditRecognitionPersistence.get(id)
        if credit_recognition is None:
            raise RecordNotFound("'credit recognition' with id'{}' not found.".format(id))
        return credit_recognition

    @classmethod
    def get_all(cls, page, limit):
        return CreditRecognitionPersistence.get_all(page, limit)
