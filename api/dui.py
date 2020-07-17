import re
from typing import List


class Dui:
    fs_string: str = ''
    bs_string: str = ''
    bs_array: List[str]
    front_side: dict
    back_side: dict

    def __init__(self, fs_string=None, bs_string=None, bs_array=None):
        self.fs_string = fs_string or ''
        self.bs_string = bs_string
        self.bs_array = bs_array or []

        self.front_side = {}
        self.back_side = {}

        if fs_string:
            self.parse_front()

        if bs_string and bs_array:
            self.parse_back()

    def get_key(self, regex: str, side: str = None) -> str:
        search = re.search(regex, self.fs_string if not side else side)
        if search is not None:
            return search.group(0).strip()
        else:
            return ''

    def parse_front(self):
        # To get the data from the dui we use the data provided by amazon textract
        # as a single joined string.
        # 'dui's come with a simple layout of 1 column and several rows
        # rows come in pairs of key and value
        # this allows us to make multiple regex to get values between rows.

        if not self.fs_string:
            raise Exception('fs_string can\'t be empty')

        lastNameRegex = r'(?<=name)(?=[A-Z\s])(.*?)(?=Nombres)'
        nameRegex = r'(?<=Names)(?=[A-Z\s])(.*?)(?=Cono)'
        knownBy = r'(?<=Known by)(?=[A-Z\s])(.*?)(?=Genero)'
        genderAndBirthRegex = r'(?<=Salvadorean by)(?=[A-Z\s])(.*?)(?=Fecha)'
        birthDateAndPlace = r'(?<=Birth)(?=[A-Z\s])(.*?)(?=Fecha)'
        issuance = r'(?<=issuance)(.*)(?=Fecha)'
        uid = r'[0-9]{8}-[0-9]'
        datesRegex = r'([0-9]{2}/[0-9]{2}/[0-9]{4})'

        # Persons full name
        self.front_side['firstName'] = self.get_key(nameRegex)
        self.front_side['lastName'] = self.get_key(lastNameRegex)
        self.front_side['knownBy'] = self.get_key(knownBy)

        # Gender and birth
        genderAndBirth = self.get_key(genderAndBirthRegex)
        self.front_side['gender'] = genderAndBirth[:1]
        self.front_side['salvadorian'] = genderAndBirth[2:]

        # Date of issuance and place
        issuance = self.get_key(issuance)
        # since issuance comes as a string 'DD/MM/YYYY state, city'
        # treat the string as a slice to divide the needed data in two
        self.front_side['issuanceDate'] = issuance[0:10]
        self.front_side['issuancePlace'] = issuance[10:].strip()

        # Place of birth and date.
        birthAndPlace = self.get_key(birthDateAndPlace)
        # since birthAndPlace comes as a string 'DD/MM/YYYY state, city'
        # treat the string as a slice to divide the needed data in two
        self.front_side['birthDate'] = birthAndPlace[0:10]
        self.front_side['placeOfBirth'] = birthAndPlace[10:].strip()

        # DUI number
        self.front_side['uid'] = self.get_key(uid)

        # Dui expiration date
        dates = re.findall(datesRegex, self.fs_string)
        # Workaround
        # Naive technique, we assume the expiration date will always come as the
        # last date in the document.
        # this is successful only when all dates are found.
        self.front_side['expirationDate'] = dates[-1] if len(dates) == 3 else ''

        return self.front_side

    def parse_back(self):
        if not self.bs_string:
            raise Exception('bs_string can\'t be empty')

        if not self.bs_array:
            raise Exception('bs_array can\'t be empty')
        # Regex
        # lastNameRegex = r'(?<=name)(?=[A-Z\s])(.*?)(?=Nombres)'
        addressAndTypeReg = r'(?<=Type)(?=[A-Z\s])(.*?)(?=NIT)'
        addressReg = r'([A-Z])(.*?)(?=[A-Z]{2}-[0-9])'
        nitReg = r'(?<=NIT)(.*?)(?=Municipio)'
        zipCodeReg = r'[0-9]{4,10}'
        mothersNameReg = r'(?<=Status)(?=[A-Z\s])(.*?)(?=Nombre)'
        fathersNameReg = r'(?<=\(A\))(?=[A-Z\s])(.*?)(?=Tipo)'
        maritalStatusReg = r'[A-Z]*\(A\)'
        # initial str = 'Spouse's' name, we only took the 'S' just in case, OCR sorta fails
        # end str = 'Profesi' to avoid a case in which ocr doesn't detects 'tildes'
        spousesNameReg = r'(?!.*Name)(?=[A-Z\s])(.*?)(?=Profesi)'
        professionReg = r'(?<=Trade)(?=[A-Z\s])(.*?)(?=[A-Z]*[0-9]+)'

        # Validate if the index on the response array is not any of this,
        # so we dont use it as a value
        isNotKey = r'Codigo|de|Zona|Zip|Code'

        # Person residence address and dui procedure type to get it.
        addressAndType = self.get_key(addressAndTypeReg, self.bs_string)
        address = re.match(addressReg, addressAndType)

        # the address and the procedure types comes in
        # a single string like 'some fake, address 22  RN-3' so
        # we apply addressReg to split them and get both values
        self.back_side['address'] = (address.group(0)).strip() if address is not None else ''
        self.back_side['procedureType'] = addressAndType[len(addressAndType) - 4:]
        self.back_side['nit'] = self.get_key(nitReg, self.bs_string)

        # We need to get the index of the zip code key so we can iterate the response array
        # and add the state and city of the response into its own keys without
        # adding a key as value by accident
        # we start iterating from the 'city' index through 'zip' index
        stateIndex = [i for i, item in enumerate(self.bs_array) if re.search('State', item)]
        try:
            self.back_side['city'] = self.bs_array[stateIndex[0] + 1] \
                if re.match(isNotKey, self.bs_array[stateIndex[0] + 1]) is None \
                else ''
        except IndexError:
            self.back_side['city'] = '-'

        try:
            self.back_side['state'] = self.bs_array[stateIndex[0] + 2] \
                if re.match(isNotKey, self.bs_array[stateIndex[0] + 2]) is None \
                else ''
        except IndexError:
            self.back_side['state'] = '-'

        self.back_side['zipCode'] = self.get_key(zipCodeReg, self.bs_string)
        self.back_side['mothersName'] = self.get_key(mothersNameReg, self.bs_string)
        self.back_side['fathersName'] = self.get_key(fathersNameReg, self.bs_string)
        self.back_side['maritalStatus'] = self.get_key(maritalStatusReg, self.bs_string)
        self.back_side['spousesName'] = self.get_key(spousesNameReg, self.bs_string)
        self.back_side['profession'] = self.get_key(professionReg).strip()

        return self.back_side

    def __repr__(self):
        return str(self.__dict__)
