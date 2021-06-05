import pandas
import telebot


class Kivano:
    help_text = '''
/categories - для получения списка категорий
/categories {название категории} - для получения информации о товарах этой категории
Пример: /categories Мобильные телефоны
/product {название товара} - для получения информации о товаре
Пример: /product Сотовый телефон Xiaomi Redmi 9 4/64GB серый
'''
    __kivano = pandas.read_csv('kivano.csv')
    nameset = set(__kivano.name.to_list())
    linkset = set(__kivano.link.to_list())
    categoryset = set(__kivano.category.to_list())

    def show_category(self, args):
        if len(args) <= 0:
            return 'Ноутбуки и Компьютеры\nМобильные телефоны\nМелкая бытовая техника\nТовары для красоты'
        else:
            if args in self.categoryset:
                product = self.__kivano[self.__kivano.category == args]
                product = product[['name', 'link']][:11].to_string()
                return product
            else:
                return f'Категория с названием "{args}" не существует'

    def show_product(self, args):
        if len(args) <= 0:
            return 'напишите название продукта рядом с командой /product'
        else:
            if args in self.nameset:
                product = self.__kivano[self.__kivano.name == args]
                product = product[['name', 'category', 'link', ]][:11].to_string()
                return product
            else:
                return f'Категория с названием "{args}" не существует'


TOKEN = "1730326110:AAEwPnDh3SYH_zgd_F3gjmqbcZpKrQd09dk"

bot = telebot.TeleBot(TOKEN)
kbot = Kivano()


@bot.message_handler(commands=['start', 'help'])
def show(message):
    bot.send_message(message.chat.id, kbot.help_text)


@bot.message_handler(commands=['product'])
def fractions(message):
    arg = message.text[9:]
    bot.send_message(message.chat.id, kbot.show_product(arg))


@bot.message_handler(commands=['categories'])
def categories(message):
    arg = message.text[12:]
    bot.send_message(message.chat.id, kbot.show_category(args=arg))


if __name__ == '__main__':
    bot.polling()
