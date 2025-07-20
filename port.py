import os
import json
import requests
import shutil
import urllib.request
from zipfile import ZipFile

pokemons = None
pwd = os.getcwd()

# cobblemon-bedrock
animationsBedrock = f"{pwd}/development_resource_packs/cobblemon/animations"
animationControllersBedrock = f"{pwd}/development_resource_packs/cobblemon/animation_controllers"
entityBedrock = f"{pwd}/development_resource_packs/cobblemon/entity"
entitiesBedrock = f"{pwd}/development_behavior_packs/cobblemon/entities"
modelsBedrock = f"{pwd}/development_resource_packs/cobblemon/models/entity"
textsBedrock = f"{pwd}/development_resource_packs/cobblemon/texts"
texturesEntityBedrock = f"{pwd}/development_resource_packs/cobblemon/textures/entity"
texturesItemsBedrock = f"{pwd}/development_resource_packs/cobblemon/textures/items"

# cobblemon-main
cobblemon = f"{pwd}/cobblemon-main/common/src/main/resources/assets/cobblemon"
animationsMain = f"{cobblemon}/bedrock/pokemon/animations"
modelsMain = f"{cobblemon}/bedrock/pokemon/models"
texturesMain = f"{cobblemon}/textures/pokemon"

def download_and_extract_cobblemon(download_url, extract_to='.'):
    zip_path = os.path.join(extract_to, 'cobblemon-main.zip')
    # Download the file
    print(f"Downloading {download_url}...")
    r = requests.get(download_url, stream=True)
    r.raise_for_status()
    with open(zip_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded to {zip_path}")

    # Extract the file
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")

    # Optionally, clean up the zip file
    os.remove(zip_path)
    print(f"Removed {zip_path}")

# Example usage:
download_and_extract_cobblemon(
    'https://gitlab.com/cable-mc/cobblemon/-/archive/main/cobblemon-main.zip'
)

def copy_animations():
    print("Copying animations...")
    if not os.path.exists(animationsBedrock): os.makedirs(animationsBedrock)
    shutil.copytree(src = animationsMain, dst = animationsBedrock, dirs_exist_ok=True)
    print("Copy animations complete.")

def copy_models():
    print("Copying models...")
    if not os.path.exists(modelsBedrock): os.makedirs(modelsBedrock)
    shutil.copytree(src = modelsMain, dst = modelsBedrock, dirs_exist_ok=True)
    print("Copy models complete.")

def copy_textures():
    print("Copying textures...")
    if not os.path.exists(texturesEntityBedrock): os.makedirs(texturesEntityBedrock)
    shutil.copytree(src = texturesMain, dst = texturesEntityBedrock, dirs_exist_ok=True)
    print("Copy textures complete.")

def create_texts():
    print("Creating texts...")
    if not os.path.exists(textsBedrock): os.makedirs(textsBedrock)
    fileName = f"{textsBedrock}/en_US.lang"
    if os.path.exists(f"{textsBedrock}/en_US.lang"): os.remove(fileName)
    with open(fileName, "w") as file:
        for pokemon in pokemons:
            pokemonName = pokemon[pokemon.index("_")+1:].capitalize()
            # Name "fixes" for Display Name
            pokemonName = pokemonName.replace("Nidoranf","Nidoran F")
            pokemonName = pokemonName.replace("Nidoranm","Nidoran M")
            pokemonName = pokemonName.replace("Mrmime","Mr Mime")
            pokemonName = pokemonName.replace("Mimejr","Mime Jr")
            pokemonName = pokemonName.replace("Porygonz","Porygon Z")
            pokemonName = pokemonName.replace("Walkingwake","Walking Wake")
            pokemonName = pokemonName.replace("Ironleaves","Iron Leaves")
            file.write(f"entity.cobblemon:{pokemon}.name={pokemonName}\n")
            file.write(f"item.spawn_egg.entity.cobblemon:{pokemon}.name=Spawn {pokemonName}\n")
    print("Create text complete.")

def download_spawn_egg_textures():
    print("Downloading spawn egg textures...")
    if not os.path.exists(texturesItemsBedrock): os.makedirs(texturesItemsBedrock)
    for pokemon in pokemons:
        spriteBaseUri1 = "https://img.pokemondb.net/sprites/sword-shield/icon"
        spriteBaseUri2 = "https://img.pokemondb.net/sprites/scarlet-violet/icon"
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        fileName = f"{texturesItemsBedrock}/{pokemon}_spawn_egg.png"
        pokemonName = pokemon[pokemon.index("_")+1:]
        # Name "fixes" for URL
        pokemonName = pokemonName.replace("nidoranf","nidoran-f")
        pokemonName = pokemonName.replace("nidoranm","nidoran-m")
        pokemonName = pokemonName.replace("mrmime","mr-mime")
        pokemonName = pokemonName.replace("mimejr","mime-jr")
        pokemonName = pokemonName.replace("porygonz","porygon-z")
        pokemonName = pokemonName.replace("walkingwake","walking-wake")
        pokemonName = pokemonName.replace("ironleaves","iron-leaves")
        try:
            spriteUrl = f"{spriteBaseUri1}/{pokemonName}.png"
            opener.retrieve(spriteUrl, fileName)
        except:
            try:
                spriteUrl = f"{spriteBaseUri2}/{pokemonName}.png"
                opener.retrieve(spriteUrl, fileName)
            except Exception as e: print(f"Failed to download: {pokemon}")
        # Update item_texture.json
        item_texture_json_path = f"{pwd}/development_resource_packs/cobblemon/textures/item_texture.json"
        with open(item_texture_json_path, "r") as itemTexureFile:
            itemTextureData = json.load(itemTexureFile)
        itemTextureData["texture_data"][f"{pokemon}_spawn_egg"] = {}
        itemTextureData["texture_data"][f"{pokemon}_spawn_egg"]["textures"] = [f"textures/items/{pokemon}_spawn_egg"]
        with open(item_texture_json_path, "w") as itemTexureFile:
            json.dump(itemTextureData, itemTexureFile, indent=4)
    print("Download spawn egg textures complete.")

def create_animation_controllers():
    print("Creating animation controllers...")
    if not os.path.exists(animationControllersBedrock):
        os.makedirs(animationControllersBedrock)
    # One shared controller for all Pokémon
    controller = {
        "format_version": "1.10.0",
        "animation_controllers": {
            "controller.animation.pokemon": {
                "initial_state": "default",
                "states": {
                    "default": {
                        "animations": [
                            {"ground_idle": "query.is_on_ground"},
                            {"air_idle": "!query.is_on_ground && !query.is_in_water && !query.is_jumping"},
                            {"water_idle": "query.is_in_water"}
                        ],
                        "transitions": [
                            {"walking": "query.modified_move_speed >= 0.01 && query.is_on_ground && !query.is_in_water"},
                            {"swimming": "query.is_swimming"},
                            {"flying": "query.modified_move_speed >= 0.01 && q.can_fly && !query.is_on_ground && !query.is_in_water && !query.is_jumping"},
                            {"sleeping": "q.is_sleeping"}
                        ],
                        "blend_transition": 0.3
                    },
                    "walking": {
                        "animations": ["walking"],
                        "transitions": [
                            {"default": "query.modified_move_speed <= 0.01 || !query.is_on_ground || query.is_in_water"}
                        ],
                        "blend_transition": 0.3
                    },
                    "flying": {
                        "animations": ["flying"],
                        "transitions": [
                            {"default": "query.is_on_ground || query.is_in_water"}
                        ],
                        "blend_transition": 0.3
                    },
                    "swimming": {
                        "animations": ["swimming"],
                        "transitions": [
                            {"default": "!query.is_in_water"}
                        ],
                        "blend_transition": 0.3
                    },
                    "sleeping": {
                        "animations": ["sleeping"],
                        "transitions": [
                            {"default": "!q.is_sleeping"}
                        ],
                        "blend_transition": 0.3
                    }
                }
            }
        }
    }
    fileName = f"{animationControllersBedrock}/pokemon.animation_controller.json"
    with open(fileName, "w") as file:
        json.dump(controller, file, indent=4)
    print("Create animation controllers complete.")

def create_client_entities():
    print("Creating client entities...")
    if not os.path.exists(entityBedrock): os.makedirs(entityBedrock)
    for pokemon in pokemons:
        pokemonName = pokemon[pokemon.index("_")+1:]
        fileName = f"{entityBedrock}/{pokemon}.entity.json"
        # Always use cobblemon prefix
        entity = {
            "format_version": "1.18.3",
            "minecraft:client_entity": {
                "description": {
                    "identifier": f"cobblemon:{pokemon}",
                    "materials": {
                        "default": "entity_emissive_alpha"
                    },
                    "textures": {
                        "default": f"textures/entity/{pokemon}/{pokemonName}.png",
                        "shiny_default": f"textures/entity/{pokemon}/shiny_{pokemonName}.png"
                    },
                    "animations": {
                        "ground_idle": f"animation.{pokemonName}.ground_idle",
                        "air_idle": f"animation.{pokemonName}.ground_idle",
                        "water_idle": f"animation.{pokemonName}.ground_idle",
                        "walking": f"animation.{pokemonName}.walking",
                        "controller": "controller.animation.pokemon"
                    },
                    "render_controllers": [
                        {"controller.render.pokemon": "query.property('cobblemon:shiny') ? 1 : 0"}
                    ],
                    "spawn_egg": {
                        "texture": pokemonName,
                        "texture_index": 0
                    },
                    "geometry": {
                        "default": f"geometry.{pokemonName}"
                    }
                }
            }
        }
        with open(fileName, "w") as file:
            json.dump(entity, file, indent=4)
    print("Create client entities complete.")

def create_behavior_entities():
    print("Creating behavior entities...")
    if not os.path.exists(entitiesBedrock): os.makedirs(entitiesBedrock)
    for pokemon in pokemons:
        fileName = f"{entitiesBedrock}/{pokemon}.behavior.json"
        pokemonName = pokemon[pokemon.index("_")+1:]
        # Use template with cobblemon prefix
        template_path = "development_behavior_packs/cobblemon/entities/0001_template.behavior.json"
        with open(template_path, "r") as jsonTemplateFile:
            jsonTemplateData = json.load(jsonTemplateFile)
        jsonTemplateData["minecraft:entity"]["description"]["identifier"] = f"cobblemon:{pokemon}"
        if "properties" not in jsonTemplateData["minecraft:entity"]["description"]:
            jsonTemplateData["minecraft:entity"]["description"]["properties"] = {}
        jsonTemplateData["minecraft:entity"]["description"]["properties"].update({
            "cobblemon:shiny": {
                "type": "bool",
                "default": False,
                "client_sync": True
            },
            "cobblemon:skin_index": {
                "type": "int",
                "default": 0,
                "client_sync": True
            }
        })
        with open(fileName, "w") as file:
            json.dump(jsonTemplateData, file, indent=4)
    print("Create behavior entities complete.")

def get_cobblemon():
    url = "https://gitlab.com/cable-mc/cobblemon/-/archive/main/cobblemon-main.zip"
    os.system(f"curl {url} -O -L")
    with ZipFile("cobblemon-main.zip", 'r') as zip:
        zip.extractall(f"{pwd}")

def get_evolution(pokemonName):
    url = "https://pogoapi.net/api/v1/pokemon_evolutions.json"
    response = requests.get(url)
    jsonData = response.json()
    for item in jsonData:
        pokemon_name = str(item["pokemon_name"]).lower()
        evolution = None
        if  pokemon_name == pokemonName:
            evolution_id = item["evolutions"][0]["pokemon_id"]
            evolution_id = f"{evolution_id}".zfill(4)
            evolution_name = str(item["evolutions"][0]["pokemon_name"]).lower()
            evolution = f"{evolution_id}_{evolution_name}"
            break
    return evolution

get_cobblemon()
copy_animations()
copy_models()
copy_textures()
pokemons = next(os.walk(texturesEntityBedrock))[1]
create_texts()
download_spawn_egg_textures()
create_animation_controllers()
create_client_entities()
create_behavior_entities()
