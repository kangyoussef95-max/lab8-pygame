# Goals:
⁃ Make the smaller squares flee away from the bigger ones
⁃ All squares tend to keep a certain randomness to their behavior/ trajectory . 

# New Variables:
FLEE_RADIUS = Distance to check for nearby bigger squares
FLEE_STRENGTH = How strongly a square moves away from a threat
dx, dy = Difference in x and y between two squares
distance = How far one square is from another
size_difference = How much bigger the threat square is
flee_x, flee_y = Direction to move away from the bigger square
total_flee_x, total_flee_y = Combined flee direction from all bigger nearby squares
weight = Makes closer and bigger threats matter more
threat_count = Number of bigger squares affecting this square 

# Generic Cases :
A small square sees one bigger square nearby => flee in the opposite direction
A small square sees multiple bigger squares => combine all flee directions
No bigger square nearby => keep normal movement and jitter

# Edge Cases:
distance == 0 => avoid divide-by-zero, use a tiny random direction
Same size squares => no fleeing
Flee force gets too strong => clamp speed
Square hits a wall while fleeing => wall bounce still applies
Many threats at once => average or limit the flee force
