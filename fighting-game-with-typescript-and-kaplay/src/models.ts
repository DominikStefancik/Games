// the values are taken from the map defined in the arena.json
type LayerType = "objectgroup" | "tilelayer";

export interface Layer {
  name: string;
  type: LayerType;
  objects?: object;
}
