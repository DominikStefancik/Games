import type { GameObj, KAPLAYCtx } from "kaplay";
import {
  BACKGROUND_SPRITE_1_ID,
  BACKGROUND_SPRITE_2_ID,
  FENCE_SPRITE_ID,
  SHOP_SPRITE_ID,
} from "../constants";
import { drawTile, fetchMapData, loadSceneSprites } from "./helpers";
import type { TiledLayer } from "../models";
import { loadEntitySprites } from "../entities/helpers";
import { createSamurai } from "../entities/samurai";
import { createNinja } from "../entities/ninja";

export const arena = async (context: KAPLAYCtx) => {
  context.setGravity(2000);

  loadSceneSprites(context);
  loadEntitySprites(context);

  // the output of calling the "add()" method is a game object
  context.add([
    context.sprite(BACKGROUND_SPRITE_1_ID),
    context.pos(0, 0),
    context.scale(4),
    // the game object will stay fixed regardless of how camera moves
    context.fixed(),
  ]);
  context.add([
    context.sprite(BACKGROUND_SPRITE_2_ID),
    context.pos(0, 0),
    context.scale(4),
    // the game object will stay fixed regardless of how camera moves
    context.fixed(),
  ]);

  // draw a scene based on the tile map description
  const { layers, tilewidth, tileheight } =
    await fetchMapData("./maps/arena.json");

  const entities: {
    [key: string]: GameObj | null;
  } = {
    player1: null,
    player2: null,
  };

  /*
   * We create a map as a main object and add tiles to it as its children
   * That way, if we modify the map (e.g. move or scale), its children will
   * automatically be modified (e.g. moved or scaled) with it
   */
  const map = context.add([context.pos(0, 0)]);

  let layer: TiledLayer;
  for (layer of layers) {
    if (
      layer.name === "DecorationSpawnPoints" &&
      layer.type === "objectgroup"
    ) {
      for (const object of layer.objects) {
        switch (object.name) {
          case SHOP_SPRITE_ID:
            // we are adding the shop animation as a child of the map
            map.add([
              context.sprite(SHOP_SPRITE_ID, {
                anim: "default", // play the "default" animation as soon as you add the shop into the map
              }),
              context.pos(object.x, object.y),
              // allow us to draw the object from the middle of a canvas
              context.area(),
              context.anchor("center"),
            ]);
            break;
          case FENCE_SPRITE_ID:
            // we are adding the shop animation as a child of the map
            map.add([
              context.sprite(FENCE_SPRITE_ID),
              context.pos(object.x, object.y + 2),
              // allow us to draw the object from the middle of a canvas
              context.area(),
              context.anchor("center"),
            ]);
            break;
        }
      }

      continue;
    }

    if (layer.name === "Boundaries" && layer.type === "objectgroup") {
      for (const object of layer.objects) {
        // we create invisible objects in the map which will serve as Boundaries
        // so players cannot get out of the canvas
        map.add([
          context.area({
            shape: new context.Rect(
              context.vec2(0),
              object.width,
              object.height,
            ),
          }),
          context.pos(object.x, object.y + tileheight / 2),
          // the property "isStatic" says that a game object is not susceptible to gravity
          // and it will not move after it collides with another game object
          context.body({ isStatic: true }),
        ]);
      }

      continue;
    }

    if (layer.name === "SpawnPoints" && layer.type === "objectgroup") {
      for (const object of layer.objects) {
        switch (object.name) {
          case "player-1":
            entities.player1 = createSamurai({
              context,
              parentObject: map,
              position: context.vec2(object.x, object.y),
            });
            break;
          case "player-2":
            entities.player2 = createNinja({
              context,
              parentObject: map,
              position: context.vec2(object.x, object.y),
            });
            break;
          default:
            throw new Error(`There is no spawn point for the ${object.name}`);
        }
      }

      continue;
    }

    if (layer.type === "tilelayer") {
      drawTile({
        context,
        layer,
        map,
        tileWidth: tilewidth,
        tileHeight: tileheight,
      });
    }

    // allows to set the position of a camera
    context.setCamPos(
      context.vec2(context.center().x - 450, context.center().y - 160),
    );
    // it allows you to scale the camera
    context.setCamScale(context.vec2(4));
  }
};
