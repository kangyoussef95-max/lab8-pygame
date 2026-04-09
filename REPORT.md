# Project Report: AI-Assisted Development

## 1. Initial Approach
* **Understanding:** Briefly describe your strategy for tackling the requirements.
* **Assumptions:** What did you assume about the project before starting?

## 2. Prompting & AI Interaction
* **Successes:** What types of prompts or context worked best for you?
* **Failures:** Describe specific instances where CoPilot failed (hallucinations, over-engineering, or logical errors).
* **Analysis:** Why do you think these failures happened, and how did they impact your progress?

## 3. Key Learnings
* **Technical Skills:** What CS concepts or tools did you discover or master during this project?
* **AI Workflow:** How will you change your use of AI tools in your next project?

# Project Report:

## 1. Initial Approach

**Understanding:** I opted to add the fleeing function gradually. Firstly, I clarified what "fleeing" is; a small square detects larger squares, identifies the direction to flee from the closest large square, and flees accordingly. I decided to stick to the existing code organization and implement fleeing on top of the existing random movement.
**Assumptions:** It seemed sensible to apply the fleeing algorithm to small squares only when the nearest large square is detected. Secondly, the fleeing algorithm could be used as a supplement to random movement. Lastly, there was no need to consider the influence of different threats simultaneously.

## 2. Prompting & AI Interaction

**Successes:** The most helpful prompts concerned the problem understanding, its step-by-step solution, and explanations of the algorithm. Requesting stubs and TODOs were beneficial for understanding how the fleeing algorithm would affect the object's random movement and how to combine the fleeing direction and distance with the existing movement.
**Failures:** On occasion, Copilot offered overly complicated and irrelevant solutions. For example, it sometimes suggested a complete implementation of the fleeing logic, which was too sophisticated for the lab assignment. Occasionally, it proposed a more complex algorithm that led to unexpected behavior such as the strange movement close to walls or dependence on the update order.
**Analysis:** It seems that such problems appeared due to the tendency of AI assistants to offer complete and optimized solutions regardless of the complexity and appropriateness of the assignment. Additionally, AI does not entirely consider the lab requirements, so I had to verify whether it suggested appropriate changes and adjust them.

## 3. Key Learnings

**Technical Skills:** I gained experience in working with vectors, finding distance between two objects, applying math.hypot() for that purpose, and implementing the algorithm within a game loop. Additionally, I understood that velocity must be adjusted rather than positions. Finally, I figured out how to handle special situations such as overlap detection and collision with walls.
**AI Workflow:** In a future project, I will try to employ AI differently by focusing on explanations and gradual problem solving rather than resorting to to-dos and stubs so swiftly. I will also try to test every suggested change early to ensure the proper functioning of the updated logic and proceed to the next step only after validating the previous one. 