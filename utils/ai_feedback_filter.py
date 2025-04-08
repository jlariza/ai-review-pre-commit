from enum import Enum

from utils.protocols import AIConsumerProtocol


class FeedbackType(Enum):
    REVIEW = "REVIEW"
    SECURITY = "SECURITY"
    FORMAT = "FORMAT"


class AIConsumerFeedbackResponse:
    TYPES_OF_FEEDBACK = {
        FeedbackType.REVIEW: "Please review this code for code smells, bad practices and outdated or deprecated code and provide feedback.",
        FeedbackType.SECURITY: "Please review this code security based in OWASP and provide feedback",
        FeedbackType.FORMAT: "Please review this code format, based on the best lint and format practices, and provide feedback",
    }

    def __init__(self, consumer: AIConsumerProtocol):
        self.consumer = consumer

    def get_review_feedback(
        self,
        input: str,
        model: str = "gpt-4o-mini",
    ) -> list[str]:
        """
        Get the review feedback from the AI consumer.
        """
        return self._filter_feedback(
            instructions=self._generate_instructions(FeedbackType.REVIEW),
            input=input,
            model=model,
        )

    def get_security_feedback(
        self,
        input: str,
        model: str = "gpt-4o-mini",
    ) -> list[str]:
        """
        Get the security feedback from the AI consumer.
        """
        return self._filter_feedback(
            instructions=self._generate_instructions(FeedbackType.SECURITY),
            input=input,
            model=model,
        )

    def get_format_feedback(
        self,
        input: str,
        model: str = "gpt-4o-mini",
    ) -> list[str]:
        """
        Get the format feedback from the AI consumer.
        """
        return self._filter_feedback(
            instructions=self._generate_instructions(FeedbackType.FORMAT),
            input=input,
            model=model,
        )

    def get_all_feedback(
        self,
        input: str,
        model: str = "gpt-4o-mini",
        feedback_types: list[str] = [FeedbackType.REVIEW],
    ) -> dict[str, list[str]]:
        """
        Get all feedback from the AI consumer.
        """
        return {
            "review": self.get_review_feedback(input, model)
            if FeedbackType.REVIEW in feedback_types
            else [],
            "security": self.get_security_feedback(input, model)
            if FeedbackType.SECURITY in feedback_types
            else [],
            "format": self.get_format_feedback(input, model)
            if FeedbackType.FORMAT in feedback_types
            else [],
        }

    def _generate_instructions(self, feedback_type: FeedbackType) -> str:
        """
        Generates instructions for the AI consumer based on the feedback type.

        :param feedback_type: The type of feedback to generate instructions for.
        :return: The generated instructions.
        """
        if feedback_type not in self.TYPES_OF_FEEDBACK:
            raise ValueError(f"Invalid feedback type: {feedback_type}")
        return f"{self.TYPES_OF_FEEDBACK[feedback_type]}. Return OK if there is no feedback."

    def _filter_feedback(
        self,
        instructions: str,
        input: str,
        model: str = "gpt-4o-mini",
    ) -> list[str]:
        """
        Filters feedback using the AI consumer.

        :param instructions: The instructions for the AI consumer.
        :param input: The input for the AI consumer.
        :param model: The model to use for text generation (default: "gpt-4o-mini").
        :return: The filtered feedback.
        """
        response = self.consumer.generate_text(instructions, input, model)
        # Parse the response
        response = response.split("\n")
        # Check if the response contains feedback
        feedback = [line for line in response if line and line != "OK"]
        return feedback
