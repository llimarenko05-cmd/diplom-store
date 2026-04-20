from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField("Наименование поставщика", max_length=200)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    comment = models.TextField("Комментарий", blank=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ("Женский", "Женский"),
        ("Мужской", "Мужской"),
    ]

    name = models.CharField("Наименование", max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        verbose_name="Поставщик",
        null=True,
        blank=True
    )
    gender = models.CharField(
        "Пол",
        max_length=20,
        choices=GENDER_CHOICES,
        default="Женский"
    )
    size = models.CharField("Размер", max_length=20)
    color = models.CharField("Цвет", max_length=50)
    article = models.CharField("Артикул", max_length=50, unique=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=0)
    minimum_quantity = models.PositiveIntegerField("Минимальный остаток", default=0)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "Нет в наличии"
        if self.quantity < self.minimum_quantity:
            return "Критически мало"
        if self.quantity == self.minimum_quantity:
            return "Минимальный остаток"
        return "В наличии"

    @property
    def replenishment_needed(self):
        if self.quantity < self.minimum_quantity:
            return self.minimum_quantity - self.quantity
        return 0


class StockReceipt(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество")
    supplier = models.CharField("Поставщик", max_length=200)
    receipt_date = models.DateTimeField("Дата поступления", default=timezone.now)
    comment = models.TextField("Комментарий", blank=True)

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"
        ordering = ["-receipt_date"]

    def __str__(self):
        return f"Поступление: {self.product.name} - {self.quantity}"


class Sale(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество")
    sale_date = models.DateTimeField("Дата продажи", default=timezone.now)
    comment = models.TextField("Комментарий", blank=True)

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        ordering = ["-sale_date"]

    def __str__(self):
        return f"Продажа: {self.product.name} - {self.quantity}"


class SaleOrder(models.Model):
    created_at = models.DateTimeField("Дата продажи", auto_now_add=True)

    class Meta:
        verbose_name = "Продажа (чек)"
        verbose_name_plural = "Продажи (чеки)"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Продажа #{self.id} от {self.created_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())


class SaleItem(models.Model):
    sale = models.ForeignKey(
        SaleOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Продажа"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция продажи"
        verbose_name_plural = "Позиции продажи"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price


class ReceiptOrder(models.Model):
    created_at = models.DateTimeField("Дата поступления", auto_now_add=True)
    supplier_name = models.CharField("Поставщик", max_length=200)

    class Meta:
        verbose_name = "Поступление (накладная)"
        verbose_name_plural = "Поступления (накладные)"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Накладная #{self.id} от {self.created_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        ReceiptOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Накладная"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = "Позиция поступления"
        verbose_name_plural = "Позиции поступления"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class ActionLog(models.Model):
    ACTION_CHOICES = [
        ("CREATE_PRODUCT", "Добавление товара"),
        ("UPDATE_PRODUCT", "Редактирование товара"),
        ("DELETE_PRODUCT", "Удаление товара"),
        ("CREATE_SALE", "Оформление продажи"),
        ("CREATE_RECEIPT", "Оформление поступления"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    action_type = models.CharField("Тип действия", max_length=50, choices=ACTION_CHOICES)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Товар"
    )
    description = models.TextField("Описание")
    created_at = models.DateTimeField("Дата и время", default=timezone.now)

    class Meta:
        verbose_name = "Журнал действий"
        verbose_name_plural = "Журнал действий"
        ordering = ["-created_at"]

    def __str__(self):
        username = self.user.username if self.user else "Неизвестный пользователь"
        return f"{username} - {self.get_action_type_display()}"
