from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey



User = get_user_model()


def get_product_url(obj, viewname, model_name):
    ct_model = obj.__class__.meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class Category(MPTTModel):

    parent = TreeForeignKey('self', null=True, blank=True, 
            related_name='children', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, unique=True,
            verbose_name='Category name'
    )
    slug = models.SlugField(unique=True)
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __str__(self):
        return self.name


class Item(models.Model):
    
    title = models.CharField(max_length=200, unique=True,
            verbose_name='Title')
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(default='ProductDefault.webp',
            verbose_name='Image')
    description = models.TextField(max_length=2500,
            verbose_name='Description'
    )
    price = models.DecimalField(max_digits=9, decimal_places=2,
            verbose_name='Price'
    )
    sku = models.CharField(max_length=16, unique=True, blank=True,
            verbose_name='Stock Keeping Unit')
    features = ArrayField(models.CharField(max_length=150), blank=True,
            null=True, verbose_name='Features'
    )
    color = models.CharField(max_length=50, blank=True,
            verbose_name='Color'
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
            verbose_name='Weight'
    )
    added = models.DateField(auto_now_add=True, blank=True,
            verbose_name='Date added'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
            verbose_name='Category'
    )
                      
    class Meta:
        abstract = True
        ordering = ['-added', 'category', 'price']
    
    def __str__(self):
        return self.title


class GunItem(Item):

    power_source = models.CharField(max_length=20, blank=True, 
            verbose_name='Power source'
    )
    muzzle_velocity = models.PositiveIntegerField(blank=True, 
            verbose_name='Muzzle velocity'
    )
    magazine_capacity = models.PositiveIntegerField(blank=True, 
            verbose_name='Magazine capacity'
    )
    
    class Meta:
        verbose_name = 'Gun'
        verbose_name_plural = 'Guns'
    
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class AmmoItem(Item):

    quantity =  models.PositiveIntegerField(verbose_name='Quantity')
    diameter = models.DecimalField(max_digits=5, decimal_places=2, 
            verbose_name='Diameter'
    )

    class Meta:
        verbose_name = 'Ammunition'


class GearItem(Item):
    
    class Meta:
        verbose_name = 'Tactial gear'


class AccessoryItem(Item):

    class Meta:
        verbose_name = 'Accessory'
        verbose_name_plural = 'Accessories'


class CartItem(models.Model):

    user = models.ForeignKey('Customer', on_delete=models.CASCADE,
            verbose_name='Customer')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE,
            related_name='related_item', verbose_name='Cart'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
            verbose_name='Total price'
    )
      
    def __str__(self):
        return 'Item: {} (for cart)'.format(self.item.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', on_delete=models.CASCADE,
            verbose_name='Owner'
    )
    items = models.ManyToManyField(CartItem, blank=True,
            related_name='related_cart', verbose_name='Items'
    )
    total_items = models.PositiveIntegerField(default=0,
            verbose_name='Total items'
    )
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
            verbose_name='Total price'
    )
                                    
    def __str__(self):
        return 'Cart: {}'.format(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
            verbose_name='User'
    )
    phone = models.CharField(max_length=20, verbose_name='Phone')
    address = models.CharField(max_length=255, verbose_name='Address')
    
    def __str__(self):
        return 'User: {} {}'.format(self.user.first_name, self.user.last_name)


goodses = [GunItem, AmmoItem, GearItem, AccessoryItem]

class LatestItemManager():
    
    @staticmethod
    def get_last_items():
        items = []
        for item_type in goodses:
            items.extend(item_type.objects.order_by('-id'))
        return items
