import type { GameObj } from "kaplay";
import type { RoomData, SceneData } from "./scenes/models";
import {
  EXIT_NAME,
  POSITION_TAG,
  ROOM_DATA_LAYER_NAME,
  SCENE,
} from "./constants";
import {
  setCameraHorizontalControls,
  setCameraVerticalZones,
  setExitZones,
  setMapColliders,
} from "./scenes/helpers";
import { createPlayer } from "./entities/player";
import kaplayContext from "./kaplay-context";
import { createHealthCartridge } from "./entities/healthCartridge";
import healthBar from "./ui/healthBar";
import { createEnemyDrone } from "./entities/enemyDrone";
import { stateManager } from "./state/globalStateManager";
import { createEnemyBoss } from "./entities/enemyBoss";

export const setUpRoomMap = (params: {
  map: GameObj;
  roomData: RoomData;
  scene: string;
  verticalBound: number;
  previousSceneData: SceneData;
}) => {
  const { map, roomData, scene, verticalBound, previousSceneData } = params;
  const colliders = [];
  const positions = [];
  const cameras = [];
  const exits = [];

  for (const layer of roomData.layers) {
    switch (layer.name) {
      case ROOM_DATA_LAYER_NAME.colliders:
        colliders.push(...layer.objects);
        break;
      case ROOM_DATA_LAYER_NAME.positions:
        positions.push(...layer.objects);
        break;
      case ROOM_DATA_LAYER_NAME.cameras:
        cameras.push(...layer.objects);
        break;
      case ROOM_DATA_LAYER_NAME.exits:
        exits.push(...layer.objects);
        break;
      default:
        break;
    }
  }

  let destinationScene = "";

  switch (scene) {
    case SCENE.room1:
      destinationScene = SCENE.room2;
      break;
    case SCENE.room2:
      destinationScene = SCENE.room1;
      break;
    default:
      break;
  }

  setMapColliders(map, colliders);
  setCameraVerticalZones(map, cameras);

  const player = map.add(createPlayer());
  setCameraHorizontalControls({ map, player, roomData });
  setExitZones({ map, exits, destinationScene });

  for (const position of positions) {
    if (position.name === POSITION_TAG.player && !previousSceneData.exitName) {
      player.setPosition(kaplayContext.vec2(position.x, position.y));
      player.setControls();
      player.setEvents();
      player.enablePassthrough();
      player.respawnIfOutOfBounds(verticalBound, scene);
    }

    if (
      (position.name === POSITION_TAG.entrance1 &&
        previousSceneData.exitName === EXIT_NAME["exit-1"]) ||
      (position.name === POSITION_TAG.entrance2 &&
        previousSceneData.exitName === EXIT_NAME["exit-2"])
    ) {
      player.setPosition(kaplayContext.vec2(position.x, position.y));
      player.setControls();
      player.setEvents();
      player.enablePassthrough();
      player.respawnIfOutOfBounds(verticalBound, scene);
      kaplayContext.setCamPos(player.pos);
    }

    if (position.type === POSITION_TAG.drone) {
      const drone = map.add(
        createEnemyDrone(kaplayContext.vec2(position.x, position.y)),
      );
      drone.setBehaviour();
      drone.setEvents();
    }

    if (
      position.name === POSITION_TAG.boss &&
      !stateManager.getState().isBossDefeated
    ) {
      const boss = map.add(
        createEnemyBoss(kaplayContext.vec2(position.x, position.y)),
      );
      boss.setBehaviour();
      boss.setEvents();
    }

    if (position.type === POSITION_TAG.cartridge) {
      map.add(
        createHealthCartridge(kaplayContext.vec2(position.x, position.y)),
      );
    }
  }

  kaplayContext.add(healthBar);
};
