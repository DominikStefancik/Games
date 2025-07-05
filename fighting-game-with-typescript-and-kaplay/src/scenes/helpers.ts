export const fetchMapData = async (mapFilePath: string) => {
  if (!mapFilePath.endsWith(".json")) {
    throw new Error("The path is not to a JSON file");
  }

  const response = await fetch(mapFilePath);

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return await response.json();
};
