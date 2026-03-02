import type { GameObj, KAPLAYCtx, Vec2 } from "kaplay";
import type { Direction } from "../models";

export const createHealthBar = (params: {
  context: KAPLAYCtx;
  owner: GameObj;
  direction: Direction;
}) => {
  const { context, owner, direction } = params;

  const healthContainerPosition: { [key: string]: Vec2 } = {
    left: context.vec2(310, 40),
    right: context.vec2(972, 40),
  };

  const healthContainer = context.add([
    context.rect(600, 50),
    context.color(200, 0, 0),
    context.area(),
    context.anchor("center"),
    context.outline(4),
    context.pos(healthContainerPosition[direction]),
    context.fixed(),
  ]);

  // the health display must be a child of the health container
  // so it can be placed on top it
  const healthDisplay = healthContainer.add([
    context.rect(600, 46),
    context.color(0, 200, 0),
    context.pos(-300, -23),
    context.rotate(0),
  ]);

  if (direction === "right") {
    // the "rotateBy" method is available after we add the "rotate" component
    healthDisplay.rotateBy(180);
    healthDisplay.pos = context.vec2(300, 23);
  }

  const reduceWithBy = healthDisplay.width / (owner.maxHealthPoints + 1);

  context.onUpdate(() => {
    if (owner.hp() === owner.previousHealthPoints) {
      return;
    }

    owner.previousHealthPoints = owner.hp();

    if (owner.hp() !== 0) {
      context.tween(
        healthDisplay.width,
        healthDisplay.width - reduceWithBy,
        0.1,
        (newWidth) => (healthDisplay.width = newWidth),
        context.easings.linear,
      );

      return;
    }

    context.tween(
      healthDisplay.width,
      0,
      0.1,
      (newWidth) => (healthDisplay.width = newWidth),
      context.easings.linear,
    );
  });
};
