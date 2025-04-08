from openai import OpenAI, OpenAIError


class OpenAIConsumer:
    def __init__(self):
        """
        Initializes the OpenAIConsumer with the provided API key.
        """
        # OPENAI_API_KEY is set as an environment variable
        self.client = OpenAI()

    def generate_text(
        self, instructions: str, input: str, model: str = "gpt-4o"
    ) -> str:
        """
        Generates text using OpenAI's API.

        :param prompt: The input prompt for the model.
        :param model: The model to use for text generation (default: "text-davinci-003").
        :param max_tokens: The maximum number of tokens to generate (default: 100).
        :return: The generated text.
        """
        try:
            response = self.client.responses.create(
                model=model,
                instructions=instructions,
                input=input,
            )
            return response.output_text
        except OpenAIError as e:
            raise RuntimeError(f"Error generating text: {e}")
