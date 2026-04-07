## Goals:
FLEEING - PHASE 1
Flee Feature:
⁃ Make the smaller squares flee away from the bigger ones
⁃ All squares tend to keep a certain randomness to their behavior/ trajectory . Take the time to THINKl
⁃ Think of strategies and how you would implement them. Find the generic and edge cases. Draw figures!
accurate
" Write up your thinking/ analysis in MY_NOTES. md
Code as much as you can yourself Really do try on your own. There's lots of code in your project you might be able to reuse and modify to achieve the Flee behavior.
s to onboard NJ
Lists, vectors, distances etc..
If you use Al/ CoPilot: Tame it: "Here is what I am thinking to make the smaller square.... Do not give away the full solution/ fagoritm,jus hepme leanhowto do progrestely."
Use the Stubs & Todo. Adapt to your needs: "add extra explanations. Explain how each funiction stub relates to another"

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
