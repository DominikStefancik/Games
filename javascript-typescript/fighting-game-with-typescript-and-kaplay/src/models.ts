// the values for the types are taken from the map defined in the arena.json
export type TiledLayer = TiledTileLayer | TiledObjectLayer;

interface TileBaseLayer {
  id: number;
  name: string;
  height: number;
  width: number;
  x: number;
  y: number;
  visible: boolean;
  opacity: number;
}

export interface TiledTileLayer extends TileBaseLayer {
  type: "tilelayer";
  data: number[];
  // we add this to have an exclusive union (exclucive OR) in the TiledLayer type
  // meaning that the type TiledTileLayerwill will never have the field "objects"
  objects: never;
}

export interface TiledObjectLayer extends TileBaseLayer {
  type: "objectgroup";
  // we add this to have an exclusive union (exclucive OR) in the TiledLayer type
  // meaning that the type TiledObjectLayer will never have the field "data"
  data: never;
  objects: TiledObject[];
}

interface TiledObject {
  id: number;
  name: string;
  type: string;
  point: boolean;
  height: number;
  width: number;
  x: number;
  y: number;
  rotation: number;
  visible: boolean;
  opacity: number;
}

export type Direction = "left" | "right";
