from os.path import join

from settings import load_model, load_texture

from .constants import ModelAsset, TextureAsset


def load_textures():
    return {
        TextureAsset.BACKGROUND: load_texture(join("assets", "textures", "background.jpg")),
    }


def load_models():
    return {
        # Baked Goods
        ModelAsset.BAGUETTE: load_model(
            join("assets", "models", "baked_goods", "baguette.gltf")
        ),
        ModelAsset.BAGUETTE_HALF: load_model(
            join("assets", "models", "baked_goods", "baguette_half.gltf")
        ),
        ModelAsset.BAGUETTE_SLICE: load_model(
            join("assets", "models", "baked_goods", "baguette_slice.gltf")
        ),
        ModelAsset.BREAD: load_model(
            join("assets", "models", "baked_goods", "bread.gltf")
        ),
        ModelAsset.BREAD_HALF: load_model(
            join("assets", "models", "baked_goods", "bread_half.gltf")
        ),
        ModelAsset.BREAD_ROLL: load_model(
            join("assets", "models", "baked_goods", "bread_roll.gltf")
        ),
        ModelAsset.BREAD_SLICE: load_model(
            join("assets", "models", "baked_goods", "bread_slice.gltf")
        ),
        ModelAsset.CAKE_BIRTHDAY: load_model(
            join("assets", "models", "baked_goods", "cake_birthday.gltf")
        ),
        ModelAsset.CAKE_BIRTHDAY_CUT: load_model(
            join("assets", "models", "baked_goods", "cake_birthday_cut.gltf")
        ),
        ModelAsset.CAKE_BIRTHDAY_SLICE: load_model(
            join("assets", "models", "baked_goods", "cake_birthday_slice.gltf")
        ),
        ModelAsset.CAKE_CHOCOLATE: load_model(
            join("assets", "models", "baked_goods", "cake_chocolate.gltf")
        ),
        ModelAsset.CAKE_CHOCOLATE_CUT: load_model(
            join("assets", "models", "baked_goods", "cake_chocolate_cut.gltf")
        ),
        ModelAsset.CAKE_CHOCOLATE_SLICE: load_model(
            join("assets", "models", "baked_goods", "cake_chocolate_slice.gltf")
        ),
        ModelAsset.CAKE_STRAWBERRY: load_model(
            join("assets", "models", "baked_goods", "cake_strawberry.gltf")
        ),
        ModelAsset.CAKE_STRAWBERRY_CUT: load_model(
            join("assets", "models", "baked_goods", "cake_strawberry_cut.gltf")
        ),
        ModelAsset.CAKE_STRAWBERRY_SLICE: load_model(
            join("assets", "models", "baked_goods", "cake_strawberry_slice.gltf")
        ),
        ModelAsset.CINNAMON_ROLL: load_model(
            join("assets", "models", "baked_goods", "cinnamon_roll.gltf")
        ),
        ModelAsset.COOKIE: load_model(
            join("assets", "models", "baked_goods", "cookie.gltf")
        ),
        ModelAsset.CROISSANT: load_model(
            join("assets", "models", "baked_goods", "croissant.gltf")
        ),
        ModelAsset.CUPCAKE: load_model(
            join("assets", "models", "baked_goods", "cupcake.gltf")
        ),
        ModelAsset.DONUT: load_model(
            join("assets", "models", "baked_goods", "donut.gltf")
        ),
        ModelAsset.DONUT_CHOCOLATE: load_model(
            join("assets", "models", "baked_goods", "donut_chocolate.gltf")
        ),
        ModelAsset.DONUT_PINK: load_model(
            join("assets", "models", "baked_goods", "donut_pink.gltf")
        ),
        ModelAsset.MUFFIN: load_model(
            join("assets", "models", "baked_goods", "muffin.gltf")
        ),
        ModelAsset.PIE_APPLE: load_model(
            join("assets", "models", "baked_goods", "pie_apple.gltf")
        ),
        ModelAsset.PIE_APPLE_CUT: load_model(
            join("assets", "models", "baked_goods", "pie_apple_cut.gltf")
        ),
        ModelAsset.PIE_APPLE_SLICE: load_model(
            join("assets", "models", "baked_goods", "pie_apple_slice.gltf")
        ),
        ModelAsset.PIE_CHERRY: load_model(
            join("assets", "models", "baked_goods", "pie_cherry.gltf")
        ),
        ModelAsset.PIE_CHERRY_CUT: load_model(
            join("assets", "models", "baked_goods", "pie_cherry_cut.gltf")
        ),
        ModelAsset.PIE_CHERRY_SLICE: load_model(
            join("assets", "models", "baked_goods", "pie_cherry_slice.gltf")
        ),
        ModelAsset.WAFFLE: load_model(
            join("assets", "models", "baked_goods", "waffle.gltf")
        ),
        ModelAsset.WAFFLE_STACKED: load_model(
            join("assets", "models", "baked_goods", "waffle_stacked.gltf")
        ),
        # Picnic set
        ModelAsset.APPLE: load_model(
            join("assets", "models", "picnic_set", "apple.gltf")
        ),
        ModelAsset.APPLE_CUT: load_model(
            join("assets", "models", "picnic_set", "apple_cut.gltf")
        ),
        ModelAsset.APPLE_PIECE: load_model(
            join("assets", "models", "picnic_set", "apple_piece.gltf")
        ),
        ModelAsset.BOWL: load_model(
            join("assets", "models", "picnic_set", "bowl.gltf")
        ),
        ModelAsset.CHEESE_A: load_model(
            join("assets", "models", "picnic_set", "cheese_a.gltf")
        ),
        ModelAsset.CHEESE_B: load_model(
            join("assets", "models", "picnic_set", "cheese_b.gltf")
        ),
        ModelAsset.COOLER: load_model(
            join("assets", "models", "picnic_set", "cooler.gltf")
        ),
        ModelAsset.DRINK_CAN: load_model(
            join("assets", "models", "picnic_set", "drink_can.gltf")
        ),
        ModelAsset.FORK: load_model(
            join("assets", "models", "picnic_set", "fork.gltf")
        ),
        ModelAsset.FRISBEE: load_model(
            join("assets", "models", "picnic_set", "frisbee.gltf")
        ),
        ModelAsset.GRAPES: load_model(
            join("assets", "models", "picnic_set", "grapes.gltf")
        ),
        ModelAsset.GRAPES_BOWL: load_model(
            join("assets", "models", "picnic_set", "grapes_bowl.gltf")
        ),
        ModelAsset.JAM: load_model(join("assets", "models", "picnic_set", "jam.gltf")),
        ModelAsset.KNIFE: load_model(
            join("assets", "models", "picnic_set", "knife.gltf")
        ),
        ModelAsset.MUG: load_model(join("assets", "models", "picnic_set", "mug.gltf")),
        ModelAsset.PICNIC_BASKET_ROUND: load_model(
            join("assets", "models", "picnic_set", "picnic_basket_round.gltf")
        ),
        ModelAsset.PICNIC_BASKET_SQUARE: load_model(
            join("assets", "models", "picnic_set", "picnic_basket_square.gltf")
        ),
        ModelAsset.PILLOW_SMALL_BLUE: load_model(
            join("assets", "models", "picnic_set", "pillow_small_blue.gltf")
        ),
        ModelAsset.PILLOW_SMALL_GREEN: load_model(
            join("assets", "models", "picnic_set", "pillow_small_green.gltf")
        ),
        ModelAsset.PILLOW_SMALL_RED: load_model(
            join("assets", "models", "picnic_set", "pillow_small_red.gltf")
        ),
        ModelAsset.PLATE_A: load_model(
            join("assets", "models", "picnic_set", "plate_a.gltf")
        ),
        ModelAsset.PLATE_B: load_model(
            join("assets", "models", "picnic_set", "plate_b.gltf")
        ),
        ModelAsset.RADIO: load_model(
            join("assets", "models", "picnic_set", "radio.gltf")
        ),
        ModelAsset.SANDWICH: load_model(
            join("assets", "models", "picnic_set", "sandwich.gltf")
        ),
        ModelAsset.SPOON: load_model(
            join("assets", "models", "picnic_set", "spoon.gltf")
        ),
        ModelAsset.TEAPOT: load_model(
            join("assets", "models", "picnic_set", "teapot.gltf")
        ),
        ModelAsset.THERMOS: load_model(
            join("assets", "models", "picnic_set", "thermos.gltf")
        ),
        ModelAsset.WINE_BOTTLE: load_model(
            join("assets", "models", "picnic_set", "wine_bottle.gltf")
        ),
        ModelAsset.WINE_GLASS: load_model(
            join("assets", "models", "picnic_set", "wine_glass.gltf")
        ),
    }
