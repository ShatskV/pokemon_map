from django.db import models  # noqa F401


# your models here
class Pokemon(models.Model):
    title = models.CharField('Название на русском', max_length=200)
    image = models.ImageField('Изображение', upload_to='pokemons', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    title_en = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)
    previous_evolution = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                           verbose_name='Предыдущая эволюция',
                                           related_name='next_evolutions')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.SET_NULL,
                                verbose_name='Покемон', null=True,
                                related_name='for_pokemon')
    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)
    

    def __str__(self):
        return f'{self.lat} {self.lon}'
