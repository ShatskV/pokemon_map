import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    pokemons_on_page = []
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        pokemon = entity.pokemon
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
            add_pokemon(
                    folium_map, entity.lat,
                    entity.lon,
                    img_url
                )
        else:
            add_pokemon(
                    folium_map, entity.lat,
                    entity.lon
                )
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
       
    pokemon_entities = pokemon.pokemon_entities.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    if pokemon.image:
        img_url = request.build_absolute_uri(pokemon.image.url)
    else:
        img_url = None
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )
    pokemon_top_page = {
                'pokemon_id': pokemon.id,
                'img_url': img_url,
                'title_ru': pokemon.title,
                'description': pokemon.description,
                'title_en': pokemon.title_en,
                'title_jp': pokemon.title_jp,
                }
    if pokemon.previous_evolution:
        pokemon_top_page['previous_evolution'] = {'pokemon_id': pokemon.previous_evolution.id,
                                                  'title_ru': pokemon.previous_evolution.title,
                                                  'img_url': request.build_absolute_uri(
                                                            pokemon.previous_evolution.image.url)
                                                 }
    pokemon_next_evolution = pokemon.next_evolutions.first()
    if pokemon_next_evolution:
        pokemon_top_page['next_evolution'] = {'pokemon_id': pokemon_next_evolution.id,
                                              'title_ru': pokemon_next_evolution.title,
                                              'img_url': request.build_absolute_uri(
                                                            pokemon_next_evolution.image.url)
                                             }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_top_page
    })
