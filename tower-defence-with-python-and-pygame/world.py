import pygame


class World:
    def __init__(self, map_image, metadata) -> None:
        self.image = map_image
        self.level_metadata = metadata
        self.waypoints = []
        self.process_metadata()

    def process_metadata(self):
        # Look through JSON metadata to extract relevant info
        for layer in self.level_metadata["layers"]:
            if layer["name"] == "waypoints":
                for object in layer["objects"]:
                    # the "waypoints_data" contains a list coordinates in the form of dictionaries
                    waypoints_data = object["polyline"]
                    self.process_waypoints(waypoints_data)

    # Iterates ovet the list of dictionaries to extract individual sets of X and Y coordinates
    def process_waypoints(self, waypoints_data):
        for point in waypoints_data:
            waypoint = (point.get("x"), point.get("y"))
            self.waypoints.append(waypoint)

    def draw(self, surface):
        # the map will be drawn from the top left corner over the whole window
        surface.blit(self.image, (0, 0))
