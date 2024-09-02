from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

class User(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address


    @field_validator('name')
    def name_must_be_alpha(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError('Name must only contain alphabetic characters and spaces!!!')
        return v

    @field_validator('is_employed')
    def check_age_and_employment(cls, v, info):
        age = info.data.get('age')
        if v and age is not None and (age < 18 or age > 65):
            raise ValueError('Employed users must be between 18 and 65 years old?')
        return v

def process_user_registration(json_data: str) -> str:
    try:

        user = User.model_validate_json(json_data)
        return user.model_dump_json(indent=4)

    except ValidationError as e:
       return e.json(indent=4)

json_input1 = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input2 = """{
    "name": "John",
    "age": 25,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 10
    }
}"""

json_input3 = """{
    "name": "John123",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 15
    }
}"""

json_input4 = """{
    "name": "Jane",
    "age": 16,
    "email": "jane.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Los Angeles",
        "street": "Sunset Boulevard",
        "house_number": 200
    }
}"""

json_input5 = """{
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "is_employed": false,
    "address": {
        "city": "San Francisco",
        "street": "Market Street",
        "house_number": -5
    }
}"""

# Verarbeitung und Ausgabe der Ergebnisse
print("Beispiel 1 Ergebnis:")
print(process_user_registration(json_input1))
print("\n")

print("Beispiel 2 Ergebnis:")
print(process_user_registration(json_input2))
print("\n")

print("Beispiel 3 Ergebnis:")
print(process_user_registration(json_input3))
print("\n")

print("Beispiel 4 Ergebnis:")
print(process_user_registration(json_input4))
print("\n")

print("Beispiel 5 Ergebnis:")
print(process_user_registration(json_input5))