from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from mptt.models import MPTTModel, TreeForeignKey
from django_better_admin_arrayfield.models.fields import ArrayField


User = get_user_model()


# TODO: Add the function get_absolute_url-reverse and than change templates.
class Category(MPTTModel):

    parent = TreeForeignKey('self', null=True, blank=True, 
                            related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Category name')
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=2500, null=True,  # TODO: null (temp for migrations)
                                   verbose_name='Description')
    image = models.ImageField(default='ProductDefault.webp',
                              verbose_name='Image')
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __str__(self):
        return self.name


class Item(models.Model):
    
    title = models.CharField(max_length=200, unique=True,
                             verbose_name='Title')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=2500,
                                   verbose_name='Description')
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                verbose_name='Price')
    image = models.ImageField(default='ProductDefault.webp',
                              verbose_name='Image')
    # TODO: Solve unique/null problem.
    sku = models.CharField(max_length=16, unique=True, blank=True,
                           verbose_name='Stock Keeping Unit')
    features = ArrayField(models.CharField(max_length=150,
                          verbose_name='Feature'), blank=True, null=True,
                          verbose_name='Features')
    color = models.CharField(max_length=50, blank=True,
                             verbose_name='Color')
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                 verbose_name='Weight')
    added = models.DateField(auto_now_add=True, blank=True,
                             verbose_name='Date added')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Category')
    quantity_sold = models.PositiveIntegerField(default=0,
                                                verbose_name='Quantity sold')
                      
    class Meta:
        abstract = True
        ordering = ['-added', 'category', 'price']
    
    def __str__(self):
        return self.title


class GunItem(Item):

    category_parent = 'Airsoft Guns'
    power_source = models.CharField(max_length=20, blank=True, 
                                    verbose_name='Power source')
    muzzle_velocity = models.PositiveIntegerField(
        blank=True,
        verbose_name='Muzzle velocity'
    )
    magazine_capacity = models.PositiveIntegerField(
        blank=True,
        verbose_name='Magazine capacity'
    )

    class Meta:
        verbose_name = 'Gun'
        verbose_name_plural = 'Guns'


class AmmoItem(Item):

    category_parent = 'BBS & Pellets'
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    diameter = models.DecimalField(max_digits=5, decimal_places=2, 
                                   verbose_name='Diameter')

    class Meta:
        verbose_name = 'Ammunition'


class GearItem(Item):
    
    category_parent = 'Tactical Gear'

    class Meta:
        verbose_name = 'Tactical gear'


class AccessoryItem(Item):

    category_parent = 'Accessories'

    class Meta:
        verbose_name = 'Accessory'
        verbose_name_plural = 'Accessories'


class CartItem(models.Model):

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,
                                 verbose_name='Customer')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE,
                             related_name='related_item', verbose_name='Cart')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name='Total price')
      
    def __str__(self):
        return 'Item: {} (in cart)'.format(self.content_object.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', on_delete=models.CASCADE,
                              verbose_name='Owner')
    items = models.ManyToManyField(CartItem, blank=True,
                                   related_name='related_cart',
                                   verbose_name='Items')
    total_items = models.PositiveIntegerField(default=0,
                                              verbose_name='Total items')
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name='Total price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return 'Cart: {}'.format(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='User')
    phone = models.CharField(max_length=20, verbose_name='Phone')
    address = models.CharField(max_length=255, verbose_name='Address')
    
    def __str__(self):
        return 'User: {} {} ({})'.format(self.user.first_name,
                                         self.user.last_name,
                                         self.user.username)


ITEMS = [GunItem, AmmoItem, GearItem, AccessoryItem]


class LatestItemManager:

    @staticmethod
    def get_last_items():
        items = []
        for item_type in ITEMS:
            items.extend(item_type.objects.order_by('-id'))
        return items
