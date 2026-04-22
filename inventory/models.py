from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской'),
    ]

    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    name = models.CharField(max_length=200, verbose_name='Наименование')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Поставщик'
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, verbose_name='Пол')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name='Размер')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    article = models.CharField(max_length=100, unique=True, verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Текущее количество')
    minimum_quantity = models.PositiveIntegerField(default=0, verbose_name='Минимальный остаток')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def stock_status(self):
        if self.quantity > self.minimum_quantity:
            return 'В наличии'
        if self.quantity == self.minimum_quantity:
            return 'Заканчивается'
        return 'Критически мало'


class StockReceipt(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    supplier = models.CharField(max_length=200, blank=True, verbose_name='Поставщик')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    receipt_date = models.DateTimeField(default=timezone.now, verbose_name='Дата поступления')

    class Meta:
        verbose_name = 'Поступление'
        verbose_name_plural = 'Поступления'
        ordering = ['-receipt_date', '-id']

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    sale_date = models.DateTimeField(default=timezone.now, verbose_name='Дата продажи')

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        ordering = ['-sale_date', '-id']

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'


class SaleOrder(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Чек продажи'
        verbose_name_plural = 'Чеки продаж'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'Чек №{self.id}'


class SaleItem(models.Model):
    sale = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, related_name='items', verbose_name='Чек')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Позиция продажи'
        verbose_name_plural = 'Позиции продажи'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'


class ReceiptOrder(models.Model):
    supplier_name = models.CharField(max_length=200, verbose_name='Поставщик')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Накладная поступления'
        verbose_name_plural = 'Накладные поступления'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'Накладная №{self.id}'


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(ReceiptOrder, on_delete=models.CASCADE, related_name='items', verbose_name='Накладная')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция поступления'
        verbose_name_plural = 'Позиции поступления'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'


class ActionLog(models.Model):
    ACTION_TYPES = [
        ('CREATE_PRODUCT', 'Добавление товара'),
        ('UPDATE_PRODUCT', 'Редактирование товара'),
        ('DELETE_PRODUCT', 'Удаление товара'),
        ('CREATE_SALE', 'Оформление продажи'),
        ('CREATE_RECEIPT', 'Оформление поступления'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES, verbose_name='Тип действия')
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Товар'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Журнал действий'
        verbose_name_plural = 'Журнал действий'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'{self.get_action_type_display()} - {self.created_at:%d.%m.%Y %H:%M}'
