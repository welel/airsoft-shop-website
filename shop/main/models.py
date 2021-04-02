from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django_better_admin_arrayfield.models.fields import ArrayField
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Category of salable products.

    Categories organized in a tree. Each product has one category.
    Products can't have root categories.

    """
    parent = TreeForeignKey('self', null=True, blank=True, 
                            related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Category name')
    slug = models.SlugField(unique=True, max_length=200, editable=False)
    description = models.TextField(max_length=2500, null=True, blank=True)
    image = models.ImageField(default='ProductDefault.webp')
    
    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        slug = slugify(self.name, allow_unicode=True)
        if not self.slug or self.slug != slug:
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items_category', kwargs={'category_slug': self.slug})


class Item(models.Model):
    """Abstract model of a salable product.

    ..Item - each subclass starts with name of product and ends
             with "Item".

    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    description = models.TextField(max_length=2500, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(default='ProductDefault.webp')
    sku = models.CharField('Stock Keeping Unit', max_length=20, unique=True,
                           null=True, blank=True)
    features = ArrayField(models.CharField('Feature', max_length=150),
                          blank=True, null=True)
    color = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                 blank=True)
    added = models.DateField('Date added', auto_now_add=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
                      
    class Meta:
        abstract = True
        ordering = ['-added', 'category', 'price']
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slug = slugify(self.title, allow_unicode=True)
        if not self.slug or self.slug != slug:
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={
            'category_slug': self.category.slug, 'item_slug': self.slug})


class GunItem(Item):

    category_parent = 'Airsoft Guns'
    power_source = models.CharField(max_length=20, null=True, blank=True)
    muzzle_velocity = models.PositiveIntegerField(blank=True, null=True)
    magazine_capacity = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Gun'
        verbose_name_plural = 'Guns'


class AmmoItem(Item):

    category_parent = 'BBS & Pellets'
    quantity = models.PositiveIntegerField()
    diameter = models.DecimalField(max_digits=5, decimal_places=2)

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


# Mapping - root category on class (type).
CATEGORY_MODEL = {
    GunItem.category_parent: GunItem,
    AmmoItem.category_parent: AmmoItem,
    AccessoryItem.category_parent: AccessoryItem,
    GearItem.category_parent: GearItem,
}


class LatestItemManager:
    """Manager gets all existing items.

    TODO: Get rid of this class.

    """
    @staticmethod
    def get_last_items():
        items = []
        for item_class in CATEGORY_MODEL.values():
            items.extend(item_class.objects.order_by('-id'))
        return items
