import { ARENA_SCENE } from "./constants";
import kaplayContext from "./kaplay-context";
import { arena } from "./scenes";

kaplayContext.scene(ARENA_SCENE, () => arena(kaplayContext));

kaplayContext.go(ARENA_SCENE);
