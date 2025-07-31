import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  DUCK_STATE,
  COLOR,
  TAG,
  GAME_STATE,
  DUCK_ANIMATION,
  SPRITE,
  SOUND,
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
    kaplayContext.sprite(SPRITE.duck, { anim: DUCK_ANIMATION.flyingSide }),
    kaplayContext.area({
      shape: new kaplayContext.Rect(kaplayContext.vec2(0), 24, 24),
    }),
    kaplayContext.anchor("center"),
    kaplayContext.pos(startingPositions[chosenStartingPositionIndex]),
    // defines a state machine specifically for the duck game object
    kaplayContext.state(DUCK_STATE.fly, [
      DUCK_STATE.fly,
      DUCK_STATE.shot,
      DUCK_STATE.fall,
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

        this.quackingSound = kaplayContext.play(SOUND.quacking, {
          volume: 0.5,
          loop: true,
        });
        this.flappingSound = kaplayContext.play(SOUND.flapping, {
          loop: true,
          speed: 2,
        });

        const sky = kaplayContext.get(TAG.sky)[0];

        this.onStateUpdate(DUCK_STATE.fly, () => {
          const currentAnimation =
            this.getCurAnim().name === DUCK_ANIMATION.flyingSide
              ? DUCK_ANIMATION.flyingDiagonal
              : DUCK_ANIMATION.flyingSide;

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

        this.onStateEnter(DUCK_STATE.shot, async () => {
          gameStateManager.numberOfDucksShotInRound++;
          this.quackingSound.stop();
          this.flappingSound.stop();
          await kaplayContext.wait(0.2);
          this.enterState(DUCK_STATE.fall);
        });

        this.onStateEnter(DUCK_STATE.fall, () => {
          /*
           * When the method "play()" is called on a game object, it plays its animation
           * which name is passed as an argument.
           * When the method "play()" is called on the Kaplay's context object, it plays a sound
           * which name is passed as an argument.
           */
          this.play(DUCK_ANIMATION.falling);
          this.fallingSound = kaplayContext.play(SOUND.falling, {
            volume: 0.7,
          });
        });

        this.onStateUpdate(DUCK_STATE.fall, async () => {
          this.move(0, this.speed);

          // if the falling duck reached the ground
          if (this.pos.y > kaplayContext.height() - 70) {
            this.fallingSound.stop();
            kaplayContext.play(SOUND.impact);
            kaplayContext.destroy(this);
            sky.color = kaplayContext.Color.fromHex(COLOR.BLUE);
            const duckIcon = kaplayContext.get(
              `${TAG.duckIcon}-${this.duckId}`,
              { recursive: true },
            )[0];

            if (duckIcon) {
              duckIcon.color = kaplayContext.Color.fromHex(COLOR.RED);
            }

            await kaplayContext.wait(1);
            gameStateManager.enterState(GAME_STATE.duckHunted);
          }
        });

        // if a game object has the "area()" component, then the method "onClick()" is available on it
        this.onClick(() => {
          if (gameStateManager.numberOfBulletsLeft < 0) {
            return;
          }

          gameStateManager.currentScore += 100;
          this.play(DUCK_ANIMATION.shot);
          this.enterState(DUCK_STATE.shot);
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
          gameStateManager.enterState(GAME_STATE.duckEscaped);
        });
      },
    },
  ]);
};

export default createDuck;
