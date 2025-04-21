import llm_loader


class GameDesignDocument:

    def __init__(self, pillar, mechanic, public):
        self.pillar = pillar
        self.mechanic = mechanic
        self.public = public
        self.goals = self.define_goals()
        self.template = self.define_template()
        self.llm_instance = llm_loader.LLMLoader()

    def deploy_gdd(self):
        lmm_input = f"With 500 words, write the Game Design Document for " \
                f"the categorie {self.mechanic} to teach {self.pillar} for computational thinking. " \
                f"The target audience is {self.public}. " \
                f"Follow exactly the template {self.template}. " \
                f"And use the goals {self.goals} like references. "

        result = self.llm_instance.chat(lmm_input)
        return result

    def deploy_code(self, gdd):
        lmm_input = f"Create a game in JavaScript as a monolith skeleton code " \
                    f"to help code develepers to implement the proposed game "\
                    f"Based on this Game Design Document: {gdd}. "

        result = self.llm_instance.code(lmm_input)
        return result

    def deploy_artifact(self, gdd):
        lmm_input = f"Create an unppluged computational thinking activity " \
                    f"to help teachers to apply the proposed game at classroom."\
                    f"Based on this Game Design Document: {gdd}."

        result = self.llm_instance.artifact(lmm_input)
        return result

    @staticmethod
    def define_template():
        template = "Game Title: " \
                   "    1. Game Overview" \
                   "    •	Genre:" \
                   "    •	Computational Thinking Pillars:" \
                   "    •	Platform: Web" \
                   "    •	Target Audience:" \
                   "    •	Objective:" \
                   "    2. Educational Objectives" \
                   "    3. Game Mechanics" \
                   "    4. Narrative and Theme" \
                   "    5. Characters and Environments" \
                   "    6. Interface and Controls" \
                   "    7. Challenges and Puzzles" \
                   "    8. Teacher Support Resources" \
                   "    9. Assessment and Feedback" \
                   "    10. Technological Implementation"
        return template

    @staticmethod
    def define_goals():
        goals = [
            "Educational Objectives of the Game: The basis of our GDD template is clearly defining the game’s educational objectives. "
            "This section of the GDD should describe the specific computational thinking skills to be addressed, such as algorithmic thinking, "
            "pattern recognition, problem abstraction, and decomposition. Each objective is tailored to match the desired educational level and align with established curriculum standards. "
            "By defining precise educational goals, the game design process becomes purpose-driven, ensuring that the game experience serves as a means to achieve meaningful learning outcomes.",

            "Target Audience and Educational Level: Understanding the target audience is essential to create engaging and relevant educational games. "
            "In this section, we identify the specific demographic characteristics of the players, such as age group, academic level, and prior knowledge "
            "of computational thinking concepts. By tailoring the game content to match the cognitive abilities and interests of the intended audience, "
            "we enhance the game’s accessibility and potential impact on learning outcomes. Moreover, this section provides insight into the appropriate educational level for which the game is designed, allowing educators to integrate it seamlessly into their teaching strategies.",

            "Game Mechanics and Dynamics: The game mechanics and dynamics are the core elements that govern the interactive and challenging aspects of the game. "
            "This document section outlines the rules, interactions, and mechanisms players will encounter throughout the gameplay. By carefully designing game mechanics "
            "that align with the identified educational objectives, we ensure that players engage in activities that foster computational thinking skills. "
            "The game’s dynamics refer to how these mechanics interact and evolve, providing a dynamic and captivating gameplay experience that sustains learners’ interest and motivation.",

            "Story and Narrative: Narrative and storytelling play a crucial role in immersing players in the game world. In this part of the document, we craft a captivating and "
            "relevant story that complements the game’s educational content. The narrative serves as a backdrop to contextualize the challenges and puzzles presented to the players, "
            "creating an engaging and coherent game experience. A compelling story enhances player engagement and provides a memorable and meaningful context for reinforcing computational thinking concepts.",

            "Characters and Environments: Characters and environments contribute to the overall atmosphere and experience of the game. In this field, we design characters representing diverse roles and perspectives, making the game relatable and inclusive. "
            "The game environments are carefully crafted to align with the narrative and support the gameplay challenges. By creating a visually appealing and immersive world, learners are motivated to actively explore and interact with the game’s content.",

            "Game Interface: The game interface serves as the primary point of interaction between players and the game world. We design an intuitive, user-friendly interface in this document space that facilitates seamless gameplay. "
            "The interface is crafted to be visually appealing and navigable, providing players with a smooth and enjoyable experience. A well-designed interface ensures that learners can focus on the computational challenges presented without being impeded by unnecessary complexities.",

            "Challenges and Puzzles: Central to the educational experience, this section outlines the various challenges and puzzles strategically designed to reinforce computational thinking skills. "
            "Each challenge is thoughtfully crafted to align with specific educational objectives and progressively increases in complexity as players advance through the game. "
            "By presenting learners with engaging and intellectually stimulating problems, we encourage them to apply computational thinking techniques creatively and critically.",

            "Teacher Support Resources: Educators play a vital role in effectively integrating the game into the classroom. In this section, we provide teacher support resources, including guidelines, lesson plans, and supplementary materials, to facilitate seamlessly incorporating the game into the educational curriculum. "
            "These resources empower educators to leverage the game’s full potential and ensure that learners’ experiences extend beyond the game environment into the classroom.",

            "Evaluation and Feedback: Evaluating the effectiveness of the educational game is crucial to assess its impact on learning outcomes. This section outlines the evaluation methods and feedback mechanisms employed to gauge learners’ progress and comprehension. "
            "By gathering quantitative and qualitative data on the game’s educational impact, we can identify areas for improvement and continuously enhance the game’s pedagogical efficacy."
        ]

        return goals
