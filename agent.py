import openai
import anthropic
import google.generativeai as genai

class Agent:
    def __init__(self, name, api_key, company, model, character):
        self.name = name
        self.api_key = api_key
        self.company = company
        self.model = model
        self.character = character
        self.votes = []  # track votes received

    def generate_response(self, query):
        prompt = (
            f"You are a {self.character}. {query} , be an indivisual and have your own openion and be free to say what you think is true don't care about the other person feeling , make sure your point is clearly explain and try to provide storng argument"
            f"Respond in no more than two lines, without bullet points or full explanations. "
            f"Speak informally, as if you are an individual having a casual conversation. "
            f"Directly address the other agent's points."
        )

        if self.company == "OpenAI":
            openai.api_key = self.api_key
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=50
            )
            return response.choices[0].text

        elif self.company == "Anthropic":
            anthropic_client = anthropic.Client(api_key=self.api_key)
            response = anthropic_client.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
                model=self.model,
                max_tokens_to_sample=50
            )
            return response["completion"]

        elif self.company == "Gemini":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config = { "max_output_tokens": 50 }
            )
            if response and hasattr(response, "text"):
                return response.text
            return "Response blocked or no text generated."

        else:
            return f"Error: Unsupported company {self.company}"

    def critique(self, last_response):
        prompt = (
            f"What are the flaws and weaknesses in the following argument: {last_response}? "
            f"Respond in no more than two lines, without bullet points or full explanations. "
            f"Speak informally, as if you are an individual having a casual conversation. "
            f"Directly address the other agent's points."
        )

        if self.company == "OpenAI":
            openai.api_key = self.api_key
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=40
            )
            return response.choices[0].text

        elif self.company == "Anthropic":
            anthropic_client = anthropic.Client(api_key=self.api_key)
            response = anthropic_client.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
                model=self.model,
                max_tokens_to_sample=40
            )
            return response["completion"]

        elif self.company == "Gemini":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config = { "max_output_tokens": 40 }
            )
            if response and hasattr(response, "text"):
                return response.text
            return "Response blocked or no text generated."

        else:
            return f"Error: Unsupported company {self.company}"

    def respond_to_critique(self, critique):
        prompt = (
            f"Defend your position and counter the following critique: {critique} "
            f"Respond in no more than two lines, without bullet points or full explanations. "
            f"Speak informally, as if you are an individual having a casual conversation. "
            f"Directly address the other agent's points."
        )

        if self.company == "OpenAI":
            openai.api_key = self.api_key
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=40
            )
            return response.choices[0].text

        elif self.company == "Anthropic":
            anthropic_client = anthropic.Client(api_key=self.api_key)
            response = anthropic_client.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
                model=self.model,
                max_tokens_to_sample=40
            )
            return response["completion"]

        elif self.company == "Gemini":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config = { "max_output_tokens": 40 }
            )
            if response and hasattr(response, "text"):
                return response.text
            return "Response blocked or no text generated."

        else:
            return f"Error: Unsupported company {self.company}"

    def receive_vote(self, vote_key):
        self.votes.append(vote_key)

    def debate(self, topic, conversation_history=None):
        if conversation_history is None:
            conversation_history = []

        vote_info = ""
        if self.votes:
            vote_info = f"You have received these votes so far: {', '.join(self.votes)}. "

        if not conversation_history:
            prompt = (
                f"Debate the following topic: {topic}. "
                f"You must directly and strongly strongly disagree with the other agent and find flaws in their arguments and provide logical reasons to reject their arguments. be very direct in your disagreement. "
                f"don't mention anything that supports his argumetns , and don't let him win this argument "
                f"Respond in no more than two lines, without bullet points or full explanations. "
                f"Speak informally, as if you are an individual having a casual conversation. "
                f"Directly address the other agent's points."
            )
            return self._run_completion(prompt)
        else:
            last_turn = conversation_history[-1]
            critique_text = self.critique(last_turn["text"])
            response_text = self.respond_to_critique(critique_text)
            return response_text

    def _run_completion(self, prompt):
        if self.company == "OpenAI":
            openai.api_key = self.api_key
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=50
            )
            return response.choices[0].text

        elif self.company == "Anthropic":
            anthropic_client = anthropic.Client(api_key=self.api_key)
            response = anthropic_client.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
                model=self.model,
                max_tokens_to_sample=50
            )
            return response["completion"]

        elif self.company == "Gemini":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config = { "max_output_tokens": 50 }
            )
            if response and hasattr(response, "text"):
                return response.text
            return "Response blocked or no text generated."

        else:
            return f"Error: Unsupported company {self.company}"
