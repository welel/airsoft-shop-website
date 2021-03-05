from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


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
    owner = models.ForeignKey('user.Customer', on_delete=models.CASCADE,
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

    customer = models.ForeignKey('user.Customer', on_delete=models.CASCADE)
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
