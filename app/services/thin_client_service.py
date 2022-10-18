import requests

from app.config import Config


class StudentService:
    @classmethod
    def get(cls, data):
        url = Config.DATA_BROKER_URL + "/student/students"
        token = Config.DATA_BROKER_TOKEN
        request_body = {"email_set": [data]}
        hed = {"token": token}
        response = requests.get(url, headers=hed, json=request_body)
        if response.status_code == 200:
            return response.json()
        return None


class OrgLocationService:
    @classmethod
    def get(cls, data, page, limit):
        url = Config.DATA_BROKER_URL + "/ps_org_location/ps_org_location"
        token = Config.DATA_BROKER_TOKEN
        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data, params={"limit": limit, "page": page})
        if response.status_code == 200:
            return response.json()
        else:
            return None


class AcademicInfoService:
    @classmethod
    def get(cls, data, page, limit):
        url = Config.DATA_BROKER_URL + "/academic_info/academic_info"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class CollegesService:
    @classmethod
    def get(cls, data, page, limit):
        url = Config.DATA_BROKER_URL + "/colleges/colleges"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class ProgramsService:
    @classmethod
    def get(cls, data, page, limit):
        url = Config.DATA_BROKER_URL + "/programs/programs"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class SaGradeService:
    @classmethod
    def get(cls, page, limit):
        url = Config.DATA_BROKER_URL + "/sa_grade/sa_grade"
        token = Config.DATA_BROKER_TOKEN
        hed = {"token": token}
        response = requests.get(url, headers=hed, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class TermService:
    @classmethod
    def get(cls, page, limit):
        url = Config.DATA_BROKER_URL + "/ps_term/ps_term"
        token = Config.DATA_BROKER_TOKEN
        hed = {"token": token}
        response = requests.get(url, headers=hed, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class DepartmentService:
    @classmethod
    def get(cls, data, page, limit):
        url = Config.DATA_BROKER_URL + "/department/department"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data, params={"limit": limit, "page": page})
        if response.status_code == 200:
            return response.json()
        else:
            return None


class CourseService:
    @classmethod
    def get(cls, page, limit, data):
        url = Config.DATA_BROKER_URL + "/course/course"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, params={"limit": limit, "page": page}, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class GeneralEducationGroupService:
    @classmethod
    def get(cls, page, limit):
        url = Config.DATA_BROKER_URL + "/ps_general_education/ps_general_education"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, params={"limit": limit, "page": page})
        if response.status_code == 200:
            return response.json()
        else:
            return None


class InstructorService:
    @classmethod
    def get(cls, page, limit):
        url = Config.DATA_BROKER_URL + "/ps_instructor/ps_instructor"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class EmployeeTitlesService:
    @classmethod
    def get(cls, page, limit):
        url = Config.DATA_BROKER_URL + "/employee_titles/employee_titles"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class RolesService:
    @classmethod
    def get(cls, page, limit):
        url = Config.DATA_BROKER_URL + "/roles/roles"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, params={"limit": limit, "page": page})

        if response.status_code == 200:
            return response.json()
        else:
            return None


class PhotoService:
    @classmethod
    def get(cls, data):
        url = Config.DATA_BROKER_URL + "/student/photo"
        token = Config.DATA_BROKER_TOKEN
        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class EmployeeService:
    @classmethod
    def get(cls, data, page, limit):
        url = Config.DATA_BROKER_URL + "/employee/employee"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data, params={"limit": limit, "page": page})
        if response.status_code == 200:
            return response.json()
        else:
            return None


class ClassService:
    @classmethod
    def get(cls, data, page, limit):
        url = Config.DATA_BROKER_URL + "/class/class"
        token = Config.DATA_BROKER_TOKEN

        hed = {"token": token}
        response = requests.get(url, headers=hed, json=data, params={"limit": limit, "page": page})
        if response.status_code == 200:
            return response.json()
        else:
            return None