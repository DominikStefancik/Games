from os.path import join

from settings import load_model

from .constants import ModelAsset

def load_models():
    return {
        ModelAsset.BAGUETTE: load_model(join("assets", "models", "baguette.gltf")),
        ModelAsset.BAGUETTE_HALF: load_model(join("assets", "models", "baguette_half.gltf")),
        ModelAsset.BAGUETTE_SLICE: load_model(join("assets", "models", "baguette_slice.gltf")),
        ModelAsset.BREAD: load_model(join("assets", "models", "bread.gltf")),
        ModelAsset.BREAD_HALF: load_model(join("assets", "models", "bread_half.gltf")),
        ModelAsset.BREAD_ROLL: load_model(join("assets", "models", "bread_roll.gltf")),
        ModelAsset.BREAD_SLICE: load_model(join("assets", "models", "bread_slice.gltf")),
        ModelAsset.CAKE_BIRTHDAY: load_model(join("assets", "models", "cake_birthday.gltf")),
        ModelAsset.CAKE_BIRTHDAY_CUT: load_model(join("assets", "models", "cake_birthday_cut.gltf")),
        ModelAsset.CAKE_BIRTHDAY_SLICE: load_model(join("assets", "models", "cake_birthday_slice.gltf")),
        ModelAsset.CAKE_CHOCOLATE: load_model(join("assets", "models", "cake_chocolate.gltf")),
        ModelAsset.CAKE_CHOCOLATE_CUT: load_model(join("assets", "models", "cake_chocolate_cut.gltf")),
        ModelAsset.CAKE_CHOCOLATE_SLICE: load_model(join("assets", "models", "cake_chocolate_slice.gltf")),
        ModelAsset.CAKE_STRAWBERRY: load_model(join("assets", "models", "cake_strawberry.gltf")),
        ModelAsset.CAKE_STRAWBERRY_CUT: load_model(join("assets", "models", "cake_strawberry_cut.gltf")),
        ModelAsset.CAKE_STRAWBERRY_SLICE: load_model(join("assets", "models", "cake_strawberry_slice.gltf")),
        ModelAsset.CINNAMON_ROLL: load_model(join("assets", "models", "cinnamon_roll.gltf")),
        ModelAsset.COOKIE: load_model(join("assets", "models", "cookie.gltf")),
        ModelAsset.CROISSANT: load_model(join("assets", "models", "croissant.gltf")),
        ModelAsset.CUPCAKE: load_model(join("assets", "models", "cupcake.gltf")),
        ModelAsset.DONUT: load_model(join("assets", "models", "donut.gltf")),
        ModelAsset.DONUT_CHOCOLATE: load_model(join("assets", "models", "donut_chocolate.gltf")),
        ModelAsset.DONUT_PINK: load_model(join("assets", "models", "donut_pink.gltf")),
        ModelAsset.MUFFIN: load_model(join("assets", "models", "muffin.gltf")),
        ModelAsset.PIE_APPLE: load_model(join("assets", "models", "pie_apple.gltf")),
        ModelAsset.PIE_APPLE_CUT: load_model(join("assets", "models", "pie_apple_cut.gltf")),
        ModelAsset.PIE_APPLE_SLICE: load_model(join("assets", "models", "pie_apple_slice.gltf")),
        ModelAsset.PIE_CHERRY: load_model(join("assets", "models", "pie_cherry.gltf")),
        ModelAsset.PIE_CHERRY_CUT: load_model(join("assets", "models", "pie_cherry_cut.gltf")),
        ModelAsset.PIE_CHERRY_SLICE: load_model(join("assets", "models", "pie_cherry_slice.gltf")),
        ModelAsset.WAFFLE: load_model(join("assets", "models", "waffle.gltf")),
        ModelAsset.WAFFLE_STACKED: load_model(join("assets", "models", "waffle_stacked.gltf")),
    }
