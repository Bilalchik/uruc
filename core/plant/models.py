from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Species(models.Model):
    """
        Модель для учета информации о видах растений.
    """

    name = models.CharField(max_length=255, verbose_name="Название вида")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Виды растений"
        verbose_name = "Вид растения"


class Plant(models.Model):
    """
        Модель для учета информации о растениях включая вид,
        состояние здоровья, доступ к воде и местоположение.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, verbose_name="Вид растения")
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Высота (м)")
    HEALTH_CONDITION_CHOICES = [
        ('Healthy', 'Здоровое'),
        ('Diseased', 'Болеет'),
        ('Pest Infested', 'Поражено вредителями'),
        ('Nutrient Deficient', 'Недостаток питательных веществ'),
        ('Wilting', 'Увядание'),
        ('Dehydrated', 'Обезвоживание'),
        ('Frost Damage', 'Повреждение от мороза'),
        ('Sunburn', 'Солнечные ожоги'),
        ('Injured', 'Травмированное'),
        ('Other', 'Другое'),
    ]
    WATER_ACCESS_CHOICES = [
        ('Yes', 'Да, регулярно поливается'),
        ('No', 'Нет, не поливается'),
        ('Unknown', 'Неизвестно'),
        ('Seasonal', 'Поливается сезонно'),
        ('Limited', 'Ограниченный доступ к воде'),
        ('Abundant', 'Изобильный доступ к воде'),
        ('Artificial', 'Искусственное обеспечение водой'),
        ('Natural Springs', 'Источники воды'),
        ('Rainwater Collection', 'Сбор дождевой воды'),
        ('Irrigation System', 'Используется система орошения'),
        ('Other', 'Другое'),
    ]
    health_condition = models.CharField(
        max_length=30,
        choices=HEALTH_CONDITION_CHOICES,
        default='Healthy',
        verbose_name="Состояние здоровья"
    )
    crown_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Длина кроны (м)")
    water_access = models.CharField(
        max_length=30,
        choices=WATER_ACCESS_CHOICES,
        verbose_name="Доступ к воде"
    )
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Широта")
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Долгота")
    registration_date = models.DateField(auto_now_add=True)
    planting_date = models.DateField()
    full_growth_photo = models.ImageField(
        upload_to='tree_photos/full_growth/',
        verbose_name="Фотография в полный рост",
        help_text="Добавьте фотографию растения в полный рост."
    )
    fetal_photo = models.ImageField(
        upload_to='tree_photos/fetal_photo/',
        verbose_name="Фотография листьев/плодов",
        help_text="Добавьте фотографию листьев или плодов растения."
    )
    reference_point_photo = models.ImageField(
        upload_to='tree_photos/reference_point/',
        verbose_name="Фотография реперной точки",
        help_text="Добавьте фотографию, которая поможет определить местоположение растения."
    )

    class Meta:
        verbose_name = "Растение"
        verbose_name_plural = "Растения"
