import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  DUCK_SPRITE_ID,
  FALL_DUCK_STATE_ID,
  FLAPPING_SOUND_ID,
  FLY_DUCK_STATE_ID,
  FLYING_SIDE_ANIMATION_ID,
  QUACKING_SOUND_ID,
  SHOT_ANIMATION_ID,
  SHOT_DUCK_STATE_ID,
  SKY_TAG_ID,
  COLOR,
  DUCK_ESCAPED_GAME_STATE_ID,
  FLYING_DIAGONAL_ANIMATION_ID,
  FALLING_SOUND_ID,
  FALLING_ANIMATION_ID,
  IMPACT_SOUND_ID,
  DUCK_ICON_TAG_ID,
  DUCK_HUNTED_GAME_STATE_ID,
} from "../constants";
import gameStateManager from "../game-state-manager";

const createDuck = (params: { duckId: string; speed: number }): GameObj => {
  const { duckId, speed } = params;
  const startingPositions: Vec2[] = [
    kaplayContext.vec2(80, kaplayContext.center().y + 40),
    kaplayContext.vec2(kaplayContext.center().x, kaplayContext.center().y + 40),
    kaplayContext.vec2(200, kaplayContext.center().y + 40),
  ];
  const flyDirections: Vec2[] = [
    kaplayContext.vec2(-1, -1),
    kaplayContext.vec2(1, -1),
    kaplayContext.vec2(-1, 1),
  ];
  const chosenStartingPositionIndex = kaplayContext.randi(
    startingPositions.length,
  );
  const chosenFlyDirectionIndex = kaplayContext.randi(flyDirections.length);

  return kaplayContext.add([
    kaplayContext.sprite(DUCK_SPRITE_ID, { anim: FLYING_SIDE_ANIMATION_ID }),
    kaplayContext.area({
      shape: new kaplayContext.Rect(kaplayContext.vec2(0), 24, 24),
    }),
    kaplayContext.anchor("center"),
    kaplayContext.pos(startingPositions[chosenStartingPositionIndex]),
    // defines a state machine specifically for the duck game object
    kaplayContext.state(FLY_DUCK_STATE_ID, [
      FLY_DUCK_STATE_ID,
      SHOT_DUCK_STATE_ID,
      FALL_DUCK_STATE_ID,
    ]),
    // the "timer()" component allows a game object to have timer methods
    kaplayContext.timer(),
    /*
     * The "offscreen()" component controls the behavior of a game object when it goes
     * outside of the visible canvas.
     *
     * The parameter "destroy" says the game object should be destroyed when out of the screen.
     *
     * The parameter "distance" says how many units outside of the visible canvas
     * the game object should be when it is destroyed.
     */
    kaplayContext.offscreen({ destroy: true, distance: 100 }),
    // custom properties
    {
      duckId,
      flyTimer: 0,
      timeBeforeEscape: 5,
      flyDirection: null,
      speed,
      quackingSound: null,
      flappingSound: null,
      fallingSound: null,
      setBehaviour(this: GameObj) {
        this.flyDirection = flyDirections[chosenFlyDirectionIndex];

        // make the duck face the correct direction
        if (this.flyDirection.x < 0) {
          this.flipX = true;
        }

        this.quackingSound = kaplayContext.play(QUACKING_SOUND_ID, {
          volume: 0.5,
          loop: true,
        });
        this.flappingSound = kaplayContext.play(FLAPPING_SOUND_ID, {
          loop: true,
          speed: 2,
        });

        const sky = kaplayContext.get(SKY_TAG_ID)[0];

        this.onStateUpdate(FLY_DUCK_STATE_ID, () => {
          const currentAnimation =
            this.getCurAnim().name === FLYING_SIDE_ANIMATION_ID
              ? FLYING_DIAGONAL_ANIMATION_ID
              : FLYING_SIDE_ANIMATION_ID;

          // make sure that the duck doesn't fly of the screen
          // if it is near the edge, change the direction
          if (
            this.flyTimer < this.timeBeforeEscape &&
            (this.pos.x > kaplayContext.width() + 10 || this.pos.x < -10)
          ) {
            this.flyDirection.x = -this.flyDirection.x;
            this.flipX = !this.flipX;
            this.play(currentAnimation);
          }

          if (this.pos.y > kaplayContext.height() - 70 || this.pos.y < -10) {
            this.flyDirection.y = -this.flyDirection.y;
            this.play(currentAnimation);
          }

          this.move(kaplayContext.vec2(this.flyDirection).scale(this.speed));
        });

        this.onStateEnter(SHOT_DUCK_STATE_ID, async () => {
          gameStateManager.numberOfDucksShotInRound++;
          this.quackingSound.stop();
          this.flappingSound.stop();
          await kaplayContext.wait(0.2);
          this.enterState(FALL_DUCK_STATE_ID);
        });

        this.onStateEnter(FALL_DUCK_STATE_ID, () => {
          /*
           * When the method "play()" is called on a game object, it plays its animation
           * which name is passed as an argument.
           * When the method "play()" is called on the Kaplay's context object, it plays a sound
           * which name is passed as an argument.
           */
          this.play(FALLING_ANIMATION_ID);
          this.fallingSound = kaplayContext.play(FALLING_SOUND_ID, {
            volume: 0.7,
          });
        });

        this.onStateUpdate(FALL_DUCK_STATE_ID, async () => {
          this.move(0, this.speed);

          // if the falling duck reached the ground
          if (this.pos.y > kaplayContext.height() - 70) {
            this.fallingSound.stop();
            kaplayContext.play(IMPACT_SOUND_ID);
            kaplayContext.destroy(this);
            sky.color = kaplayContext.Color.fromHex(COLOR.BLUE);
            const duckIcon = kaplayContext.get(
              `${DUCK_ICON_TAG_ID}-${this.duckId}`,
              { recursive: true },
            )[0];

            if (duckIcon) {
              duckIcon.color = kaplayContext.Color.fromHex(COLOR.RED);
            }

            await kaplayContext.wait(1);
            gameStateManager.enterState(DUCK_HUNTED_GAME_STATE_ID);
          }
        });

        // if a game object has the "area()" component, then the method "onClick()" is available on it
        this.onClick(() => {
          if (gameStateManager.numberOfBulletsLeft < 0) {
            return;
          }

          gameStateManager.currentScore += 100;
          this.play(SHOT_ANIMATION_ID);
          this.enterState(SHOT_DUCK_STATE_ID);
        });

        /*
         * The "timer()" component allows us to use the "loop()" method.
         *
         * When a game object is destroyed, this loop event will automatically be destroyed.
         */
        this.loop(1, () => {
          this.flyTimer += 1;

          if (this.flyTimer === this.timeBeforeEscape) {
            sky.color = kaplayContext.Color.fromHex(COLOR.BEIGE);
          }
        });

        // The "offscreen()" component allows us to use the "onExitScreen()" method
        this.onExitScreen(() => {
          this.quackingSound.stop();
          this.flappingSound.stop();
          sky.color = kaplayContext.Color.fromHex(COLOR.BLUE);
          gameStateManager.numberOfBulletsLeft = 3;
          gameStateManager.enterState(DUCK_ESCAPED_GAME_STATE_ID);
        });
      },
    },
  ]);
};

export default createDuck;
