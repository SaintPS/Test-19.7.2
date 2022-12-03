from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()

# Тест на получение апи ключа, при вводе НЕправильного пароля/логина
def test_get_api_key_for_valid_user(email=valid_email, password="password"):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# Тест на получение апи ключа, при вводе правильного пароля/логина
def test_get_api_key_for_not_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    print(result)
    print(status)
    assert 'key' in result

# Тест на  получение списка питомцев
def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_api_pets(auth_key, filter)
    assert status == 200
    print (result)
    assert len(result['pets']) > 0

# Тест на  получение списка питомцев
def test_get_all_pets_with_no_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_api_pets(auth_key, filter)
    assert status == 200
    assert 'pets' in result


# Тест на проверку добавления нового питомца по всем (имя, тип, возраст, фото)
def test_add_new_pet_with_valid_data(name = "Carton", animal_type = 'cat', age = '4', pet_photo = 'images/111.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, rusult = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status ==200
    assert rusult['name'] == name
    assert rusult['animal_type'] == animal_type
    assert rusult['age'] == age
    assert rusult['pet_photo'] is not None

# Негативный тест на проверку добавления нового питомца с именем из цифр (имя, тип, возраст, фото)
def test_add_new_pet_with_valid_data(name = "123456789", animal_type = 'cat', age = '4', pet_photo = 'images/111.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, rusult = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status ==200
    assert rusult['name'] == name
    assert rusult['animal_type'] == animal_type
    assert rusult['age'] == age
    assert rusult['pet_photo'] is not None
    # Тест провален, питомец добавляется с именем из цифр

# Негативный тест на проверку добавления нового питомца с типом из цифр (имя, тип, возраст, фото)
def test_add_new_pet_with_valid_data(name = "Carton", animal_type = '12345', age = '4', pet_photo = 'images/111.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, rusult = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status ==200
    assert rusult['name'] == name
    assert rusult['animal_type'] == animal_type
    assert rusult['age'] == age
    assert rusult['pet_photo'] is not None
    # Тест провален, питомец добавляется с типом из цифр

# Негативный тест на проверку добавления нового питомца с возрастом из букв (имя, тип, возраст, фото)
def test_add_new_pet_with_valid_data(name = "Carton", animal_type = 'кот', age = 'ылводлов', pet_photo = 'images/111.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, rusult = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status ==200
    assert rusult['name'] == name
    assert rusult['animal_type'] == animal_type
    assert rusult['age'] == age
    assert rusult['pet_photo'] is not None
    # Тест провален, питомец добавляется с возрастом из букв


# Негативный тест на проверку добавления нового питомца с пустыми полями (имя, тип, возраст, фото)
def test_add_new_pet_with_no_valid_data(name = "", animal_type = '', age = '', pet_photo = 'images/111.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, rusult = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status ==200
    assert rusult['name'] == name
    assert rusult['animal_type'] == animal_type
    assert rusult['age'] == age
    assert rusult['pet_photo'] is not None
#  Тест провален, питомец добавляется без имени, типа и возраста с одним фото

# Негативный тест на проверку добавления нового питомца с тексовым файлов вместо фото (имя, тип, возраст, фото)
def test_add_new_pet_with_no_valid_data(name = "Tat", animal_type = 'cj,', age = '99', pet_photo = 'images/gorod3.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, rusult = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status ==200
    assert rusult['name'] == name
    assert rusult['animal_type'] == animal_type
    assert rusult['age'] == age
    assert rusult['pet_photo'] is not None
#  Тест провален, питомец добавляется, тест должен быть провален


# Тест на проверку удаления добавления питомца по всем полям
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_api_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Cartoon2", "cat", "4", "images/111.jpg")
        _, my_pets = pf.get_list_of_api_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_api_pets(auth_key, "my_pets")
    print (status)
    assert status == 200
    assert pet_id not in my_pets.values()


# Тест на проверку изменения данных о питомце (имя, тип, возраст)
def test_successful_update_self_pet_info(name='222', animal_type='222', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_api_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# Тест на проверку добавления нового питомца по всем (имя, тип, возраст) без фото
def test_add_new_pet_without_photo(name = "Carto", animal_type = 'cat', age = '4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, rusult = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status ==200
    assert rusult['name'] == name
    assert rusult['animal_type'] == animal_type
    assert rusult['age'] == age


# Тест на проверку добавления фото к новому питомцу ранее добавленному без фото
def test_set_photo(pet_photo='images/123.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_api_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] is not None
    else:
        raise Exception("There is no my pets")