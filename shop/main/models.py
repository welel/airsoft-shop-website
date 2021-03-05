from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django_better_admin_arrayfield.models.fields import ArrayField
from mptt.models import MPTTModel, TreeForeignKey


User = get_user_model()


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
        slug = slugify(self.title, allow_unicode=True)
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


class CartItem(models.Model):
    """Represents a product for the client's cart.

    """
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE,
                             verbose_name='Cart')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField('Quantity', default=1)
    total_price = models.DecimalField('Total price', max_digits=9,
                                      decimal_places=2)
      
    def __str__(self):
        return 'Item: {} (in cart)'.format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Represents client's cart.

    """
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE,
                              null=True)
    total_items = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0)
    in_order = models.BooleanField(default=False)

    def __str__(self):
        return 'Cart: {}'.format(self.id)

    def save(self, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart=self)
        cart_data = cart_items.aggregate(models.Sum('total_price'),
                                         models.Sum('quantity'))
        if cart_data['total_price__sum']:
            self.total_price = cart_data['total_price__sum']
            self.total_items = cart_data['quantity__sum']
        else:
            self.total_price, self.total_items = 0, 0
        super().save(*args, **kwargs)


class Customer(models.Model):
    """Profile of registered client of the store.

    """
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return 'User: {}'.format(self.user.username)


class Order(models.Model):
    """Represents a client's order of products.

    """
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Order is completed')
    )

    BUYING_TYPE_CHOICE = (
        (BUYING_TYPE_SELF, 'Self-pickup'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=1024, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,
                              default=STATUS_NEW)
    buying_type = models.CharField(
        max_length=100, choices=BUYING_TYPE_CHOICE, default=BUYING_TYPE_SELF
    )
    comment = models.TextField(max_length=3000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    receiving_date = models.DateField(null=True, editable=False)

    def __str__(self):
        return '{} | {}'.format(self.id, self.customer)
