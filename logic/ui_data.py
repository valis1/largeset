def get_field_types():
    return [
        {'id': 'address', 'desc': 'Full Address', 'example': 'ул. Соймоновская 436', 'script': '', 'resolved_functions':[]},
        {'id': 'city', 'desc': 'Random City', 'example': 'Челябинск', 'script': '', 'resolved_functions':[]},
        {'id': 'latitude', 'desc': 'Latitude', 'example': '51.018356', 'script': '', 'resolved_functions':[]},
        {'id': 'longitude', 'desc': 'Longitude', 'example': '23.431463', 'script': '', 'resolved_functions':[]},
        {'id': 'postal_code', 'desc': 'Postal Code', 'example': '376707', 'script': '', 'resolved_functions':[]},
        {'id': 'company', 'desc': 'Company name', 'example': '«Челябэнергосбыт»', 'script': '', 'resolved_functions':[]},
        {'id': 'day_of_week', 'desc': 'Day of Week Name', 'example': 'Четверг, Пятница', 'script': '', 'resolved_functions':[]},
        {'id': 'timestamp', 'desc': 'Unix Timestamp', 'example': '1247770623', 'script': '', 'resolved_functions':[]},
        {'id': 'dish', 'desc': 'Dish Name', 'example': 'Квашеная капуста', 'script': '', 'resolved_functions':[]},
        {'id': 'drink', 'desc': 'Drink Name', 'example': 'Мэри Пикфорд', 'script': '', 'resolved_functions':[]},
        {'id': 'fruit', 'desc': 'Fruit name', 'example': 'Маболо', 'script': '', 'resolved_functions':[]},
        {'id': 'vegetable', 'desc': 'Vegetable Name', 'example': 'Лагенария', 'script': '', 'resolved_functions':[]},
        {'id': 'email', 'desc': 'Email Address', 'example': 'downs1927@yandex.com', 'script': '', 'resolved_functions':[]},
        {'id': 'full_name', 'desc': 'Person`s full name', 'example': 'Вероника Артёменко', 'script': '', 'resolved_functions':[]},
        {'id': 'job', 'desc': 'Job title', 'example': 'Менеджер по продажам', 'script': '', 'resolved_functions':[]},
        {'id': 'phone', 'desc': 'Phone number', 'example': '+7-(968)-784-10-78', 'script': '', 'resolved_functions':[]},
        {'id': 'username', 'desc': 'User name', 'example': 'Normoblastic-2016', 'script': '', 'resolved_functions':[]},
        {'id': 'text', 'desc': 'Random text', 'example': 'Java — строго типизированный объектно-ориент...', 'script': '', 'resolved_functions':[]},
        {'id': 'title', 'desc': 'Title', 'example': 'Отличительная черта языка...', 'script': '', 'resolved_functions':[]},
        {'id': 'uuid', 'desc': 'UUID 4', 'example': '762d6a46-2701-448d-bc47-4520a05dd0ea', 'script': '', 'resolved_functions':[]},
        {'id': 'file_name', 'desc': 'File name', 'example': 'distributor.odt', 'script': '', 'resolved_functions': []},
        {'id': 'url_home', 'desc': 'Site url', 'example': 'http://www.flapping.miami', 'script': '', 'resolved_functions': []},
        {'id': 'mac', 'desc': 'Mac Address', 'example': '00:16:3e:1d:ce:1f', 'script': '', 'resolved_functions': []},
        {'id': 'ip', 'desc': 'IP Address', 'example': '102.93.58.22', 'script': '', 'resolved_functions': []},
        {'id': 'car_model', 'desc': 'Car model', 'example': 'Continental Mark II', 'script': '', 'resolved_functions': []},
        {'id': 'sequence', 'desc': 'Digit Sequence', 'example': '10, 20, 30 ...', 'script': 'start = 1; step = 1',
         'resolved_functions': []},
        {'id': 'price', 'desc': 'Price', 'example': '10.06, 11.2 ...', 'script': 'min = 1; max = 100',
         'resolved_functions': []},
        {'id': 'datetime', 'desc': 'Date and time', 'example': '01.09.2019 21:29:20',
         'script': 'min = 2018; max = 2019; format= %d%m%Y %h:%m:%s', 'resolved_functions': []},
        {'id': 'date', 'desc': 'Date and time', 'example': '01.09.2010',
         'script': 'min = 2018; max = 2019; format= %d%m%Y', 'resolved_functions': []},
        {'id': 'ean_code', 'desc': 'EAN Code', 'example': '4002232323231',
         'script': 'type = ean-13', 'resolved_functions': []},
        {'id': 'int', 'desc': 'Integer numbers', 'example': '103, 200, 423',
         'script': 'min = 10; max = 104; ', 'resolved_functions': []},
        {'id': 'float', 'desc': 'Float numbers', 'example': '1.04, 2.05 ...',
         'script': 'min = 10; max = 104; ', 'resolved_functions': []},




    ]