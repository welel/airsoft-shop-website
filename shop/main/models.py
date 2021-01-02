from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=200, verbose_name='Название категории')
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Item(models.Model):
    
    class Meta:
        abstract = True

    title = models.CharField(max_length=200, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(max_length=2000,
            verbose_name='Описание'
    )
    price = models.DecimalField(max_digits=9, decimal_places=2,
            verbose_name='Цена'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
            verbose_name='Категория'
    )
                                    
    def __str__(self):
        return self.title


class GunItem(Item):

    source_power = models.CharField(max_length=20, 
            verbose_name='Источник питания'
    )
    magazine = models.PositiveIntegerField(verbose_name='Размер магазина')
    weight = models.DecimalField(max_digits=9, decimal_places=2, 
            verbose_name='Вес'
    )
    muzzle_velocity = models.PositiveIntegerField(
            verbose_name='Начальная скорость'
    )


class BulletsItem(Item):

    count = models.CharField(max_length=20, verbose_name='Количество')
    weight = models.DecimalField(max_digits=9, decimal_places=2, 
            verbose_name='Вес'
    )
    diameter = models.DecimalField(max_digits=9, decimal_places=2, 
            verbose_name='Диаметр'
    )


class CartItem(models.Model):

    user = models.ForeignKey('Customer', on_delete=models.CASCADE,
                                verbose_name='Покупатель')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE,
            verbose_name='Корзина', related_name='related_item'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
            verbose_name='Общая цена'
    )
                                    
    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.item.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', on_delete=models.CASCADE,
            verbose_name='Владелец'
    )
    items = models.ManyToManyField(CartItem, blank=True,
            related_name='related_cart'
    )
    total_items = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
            verbose_name='Общая цена'
    )
                                    
    def __str__(self):
        return 'Корзина: {}'.format(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
            verbose_name='Пользователь'
    )
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    
    def __str__(self):
        return 'Пользователь: {} {}'.format(
            self.user.first_name, self.user.last_name)
