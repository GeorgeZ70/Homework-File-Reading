# Создадим Класс чтения текстовых файлов 
class OpenFiles:
  def __init__(self, file_name_list = None, encoding = 'utf-8'):
    self.file_name_list = file_name_list
    self.encoding = encoding
    self.file_data_list = []

# Функция для построчного чтения файлов
  def open_files(self):
    if self.file_name_list is None:
      print('Ошибка! Список файлов не передан')
    elif len(self.file_name_list) <= 0:
      return print('Ошибка! Список файлов пуст')
    else:
      for file in self.file_name_list:
        try:
          with open(file, 'r', encoding = self.encoding) as f:
            data = f.read().split('\n')
            self.file_data_list.append(data)
        except FileNotFoundError:
          print(f'Ошибка! Не удалось открыть следующий файл: {file}')
    return self.file_data_list
  

# Создадим дочерний класс вывода информации о блюдах из кулинарной книги 
class GetCookBook (OpenFiles):
  def __init__(self, file_name_list = None, our_dish_list = None, encoding = 'utf-8'):
    super().__init__(file_name_list, encoding)
    self.our_dish_list = our_dish_list
    self.recipes_data_list = sum(self.open_files(), []) # объединённый список рецептов из списка файлов на входе
    self.recipe_data_list = []
    self.cook_book = {}
    self.cook_book_selection = {}
    
  # Функция различения индексов пустых строк  в списке, содержащем информацию о блюдах
  def get_boundary_indexes(self):
    gap_idx_list = []
    for idx in range(len(self.recipes_data_list)):
        if self.recipes_data_list[idx] == '':
          gap_idx_list.append(idx)
    return gap_idx_list

  # Воспользуемся полученными индексами для формирования отдельных списков с рецептами каждого блюда
  def get_recipe_data_list(self):
    for idx1, idx2 in zip([0] + self.get_boundary_indexes(), 
                          self.get_boundary_indexes() + [None]):
        if idx1 == 0:
          self.recipe_data_list.append(self.recipes_data_list[idx1:idx2])
        else:
          self.recipe_data_list.append(self.recipes_data_list[idx1 + 1:idx2])
    return self.recipe_data_list
  # Сформируем словарь   рецептов блюд
  def create_cook_book_dict(self):
    for recipe in self.get_recipe_data_list():
        dish_name = recipe[0]
        ingredients_list = []
        ingredients_amount = int(recipe[1])
        for i in range(ingredients_amount):
            ingredient_data = recipe[2 + i].split(' | ')
            ingredients_list.append({'ingredient_name': ingredient_data[0],
                                     'quantity': int(ingredient_data[1]),
                                     'measure': ingredient_data[2]})
        self.cook_book[dish_name] = ingredients_list
    return self.cook_book

  # Функция для выборочного вывода бдюд из списка (our_dish_list) 
  def get_cook_book_dict(self):
    if self.our_dish_list is None:
      self.our_dish_list = list(self.create_cook_book_dict().keys())
      return self.create_cook_book_dict()
    else:
      if type(self.our_dish_list) is list and len(self.our_dish_list) > 0:
        for product in self.our_dish_list:
            if product in self.create_cook_book_dict():
                self.cook_book_selection[product] = self.create_cook_book_dict()[product]
            else:
                print(f'{product} отсутствует в списке блюд')
      else:
        if type(self.our_dish_list) is not list:
          return 'Список блюд отсутствует'
        else:
          return 'Список блюд пуст'
    return self.cook_book_selection

# Создадим класс вывода информации об ингредиентах блюд 
class GetShopList (GetCookBook):
  def __init__(self, file_name_list = None, our_dish_list = None):
    super().__init__(file_name_list, our_dish_list)
    self.our_cook_book = self.get_cook_book_dict()
    self.ingredient_name_list = []
    self.ingredient_dict_list = []
    self.product_dict = {}

  # Сформируем список ингредиентов для приготовления блюд из списка 'dishes' и словари с информацией о них
  def get_ingredients_list(self, dishes, person_count):
    if len(self.our_cook_book.keys()) > 0:
        if len(self.dishes) > 0:
            for dish in self.dishes:
                if dish in self.our_cook_book:
                    ingredients = self.our_cook_book[dish]
                    for ingr in ingredients:
                        self.ingredient_dict_list.append(ingr)
                        self.ingredient_name_list.append(ingr['ingredient_name'])
        else:
          print('Не указаны блюда ')
    else:
      print('Ваш список блюд пуст')
    return self.ingredient_name_list, self.ingredient_dict_list
  
    # Создадим словарь product_dict с информацией об ингредиентах и их количестве,необходимом для приготовления блюд из списка 'dishes' 
  def get_product_dict(self, dishes, person_count, ingredient_name_list, ingredient_dict_list):
    if len(self.ingredient_name_list) > 0:
        for ingr in sorted(list(set(self.ingredient_name_list))): # преобразуем список в множество во избежание повторов ингредиентов
            for my_dict in self.ingredient_dict_list :
                if my_dict['ingredient_name'] == ingr:
                    if ingr in self.product_dict:
                        self.product_dict[ingr]['quantity'] += my_dict['quantity'] * person_count
                    else:
                        self.product_dict[ingr] = {'measure': my_dict['measure'], 
                                                'quantity': my_dict['quantity'] * person_count}
    else:
        print('Ошибка!')
    return self.product_dict
  
    # Используем созданные методы класса GetShopList для выполнения нашей задачи.Если нет списка блюд, то
    # по умолчанию используется полный список блюд из словаря cook_book  
  def get_shop_list(self, dishes = None, person_count = 1):
    self.dishes = dishes
    self.dishes = [list(self.our_cook_book.keys()) if self.dishes is None else self.dishes][0]
    if type(self.dishes) != list:
      return 'Список блюд не заполнен'
    elif len(self.dishes) <= 0:
      return 'Список блюд пуст'
    self.person_count = person_count
    if type(self.person_count) != int or self.person_count <= 0:
      return 'Количество персон не указано должным образом'
    else:
      self.ingredient_name_list, self.ingredient_dict_list = self.get_ingredients_list(dishes = self.dishes, 
                                                                                       person_count = self.person_count)

      return self.get_product_dict(dishes = self.dishes, person_count = self.person_count, 
                                   ingredient_name_list = self.ingredient_name_list,
                                   ingredient_dict_list = self.ingredient_dict_list)
      
      
# Создадим функцию get_shop_list_by_dishes для выполнения нашей задачи
# Если не передан список блюд,берём все блюда из файла
def get_shop_list(dishes = None, person_count = 1): 
  my_file_name_list = ['recipes.txt']
  my_CookBook = GetCookBook(my_file_name_list, dishes)
  my_ShopList = GetShopList(my_CookBook.file_name_list, my_CookBook.our_dish_list)
  if dishes is None:
    print(my_ShopList.get_shop_list(person_count = person_count))
  else:
    print(my_ShopList.get_shop_list(dishes, person_count))
      
      
# Класс вывода информации о тексте, содержащемся в текстовых файлах 
class TextInfo (OpenFiles):
  def __init__(self, file_name_list = None, encoding  = 'utf-8'):
    super().__init__(file_name_list, encoding)
    self.files_data = self.open_files()
    self.files_dict = {}
    self.files_dict_sorted = {}

  # Создадим словарь files_dict с  информацией о текстовых файлах
  def get_files_dict(self):
    for idx, val in enumerate(self.file_name_list):
      self.files_dict[val] = {'len_text': len(self.files_data[idx]),   # значение - количество строк в файле
                              'text': self.files_data[idx]}
    return self.files_dict

  # Отсортируем полученный словарь по количеству строк в файлах
  def sort_dict (self):
    self.len_text_list = [self.get_files_dict()[k]['len_text'] for k in self.get_files_dict().keys()]
    for l in sorted(list(set(self.len_text_list))):
        for file in self.file_name_list:
            if self.get_files_dict()[file]['len_text'] == l:
              self.files_dict_sorted[file] = self.get_files_dict()[file]
              for k in self.get_files_dict()[file]:
                self.files_dict_sorted[file][k] = self.get_files_dict()[file][k]
    return self.files_dict_sorted
  
  # Выведем информацию о количестве строк и содержимое текстовых файлов
  def print_info(self):
    for k, v in self.sort_dict().items(): # сначала выведем количество строк в файле
        print(k)
        for v2 in v.values():   # выведем построчно содержимое файла 
            if type(v2) == int:
              print(f"{v2}")
            else:
                for s in v2:
                  print(s.strip())



#get_shop_list()
#a = GetShopList(['recipes.txt']).get_shop_list()
#print(a)
#a = GetCookBook(['recipes.txt']).get_cook_book_dict()
#print(a)
#TextInfo(['1.txt', '2.txt', '3.txt']).print_info() 
#my_сook_book = GetCookBook(['recipes.txt']).get_cook_book_dict()
#print(my_сook_book)
#my_cook_book1 = GetCookBook(['recipes.txt'], ['Фахитос', 'Омлет']).get_cook_book_dict()
#print(my_cook_book1)
get_shop_list()




#file = OpenFiles(['recipes.txt']).open_files()
#print(file)
