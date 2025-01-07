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

    def generate_response(self, query):
        prompt = f"You are a {self.character}. {query} Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points."
        if self.company == "OpenAI":
            openai.api_key = self.api_key
            response = openai.completions.create(
                model=self.model,
                prompt=prompt,
                max_tokens=50
            )
            return response.choices[0].text.strip()
        elif self.company == "Anthropic":
            anthropic_client = anthropic.Anthropic(api_key=self.api_key)
            response = anthropic_client.completions.create(
                model=self.model,
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
                max_tokens_to_sample=50
            )
            return response.completion.strip()
        elif self.company == "Gemini":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt, generation_config={"max_output_tokens": 50})
            if response and hasattr(response, 'parts'):
                text_parts = [part.text for part in response.parts if hasattr(part, 'text') and part.text]
                if text_parts:
                    return " ".join(text_parts).strip()
            return "Response blocked due to safety reasons or no text was generated."
        else:
            return f"Error: Unsupported company {self.company}"

    def critique(self, response):
        if self.company == "OpenAI":
            openai.api_key = self.api_key
            response = openai.completions.create(
                model=self.model,
                prompt=f"What are the flaws and weaknesses in the following argument: {response}? Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points.",
                max_tokens=40
            )
            return response.choices[0].text.strip()
        elif self.company == "Anthropic":
            anthropic_client = anthropic.Anthropic(api_key=self.api_key)
            response = anthropic_client.completions.create(
                model=self.model,
                prompt=f"{anthropic.HUMAN_PROMPT} What are the flaws and weaknesses in the following argument: {response}? {anthropic.AI_PROMPT} Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points.",
                max_tokens_to_sample=40
            )
            return response.completion.strip()
        elif self.company == "Gemini":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(f"What are the flaws and weaknesses in the following argument: {response}? Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points.", generation_config={"max_output_tokens": 40})
            return response.text.strip()
        else:
            return f"Error: Unsupported company {self.company}"

    def respond_to_critique(self, critique):
        if self.company == "OpenAI":
            openai.api_key = self.api_key
            response = openai.completions.create(
                model=self.model,
                prompt=f"Defend your position and counter the following critique: {critique} Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points.",
                max_tokens=40
            )
            return response.choices[0].text.strip()
        elif self.company == "Anthropic":
            anthropic_client = anthropic.Anthropic(api_key=self.api_key)
            response = anthropic_client.completions.create(
                model=self.model,
                prompt=f"{anthropic.HUMAN_PROMPT} Defend your position and counter the following critique: {critique} {anthropic.AI_PROMPT} Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points.",
                max_tokens_to_sample=40
            )
            return response.completion.strip()
        elif self.company == "Gemini":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(f"Defend your position and counter the following critique: {critique} Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points.", generation_config={"max_output_tokens": 40})
            return response.text.strip()
        else:
            return f"Error: Unsupported company {self.company}"

    def debate(self, topic, conversation_history=None):
        if conversation_history is None:
            conversation_history = []
        
        if not conversation_history:
            prompt = f"Debate the following topic: {topic}. You should strongly disagree with the other agent and find flaws in their arguments. Do not agree with the other agent. Respond in no more than three lines, without bullet points or full explanations. Speak informally, as if you are an individual having a casual conversation with another individual. Directly address the other agent's points."
            if self.company == "OpenAI":
                openai.api_key = self.api_key
                response = openai.completions.create(
                    model=self.model,
                    prompt=prompt,
                    max_tokens=50
                )
                return response.choices[0].text.strip()
            elif self.company == "Anthropic":
                anthropic_client = anthropic.Anthropic(api_key=self.api_key)
                response = anthropic_client.completions.create(
                    model=self.model,
                    prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
                    max_tokens_to_sample=50
                )
                return response.completion.strip()
            elif self.company == "Gemini":
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(self.model)
                response = model.generate_content(prompt, generation_config={"max_output_tokens": 50})
                if response and hasattr(response, 'parts'):
                    text_parts = [part.text for part in response.parts if hasattr(part, 'text') and part.text]
                    if text_parts:
                        return " ".join(text_parts).strip()
                return "Response blocked due to safety reasons or no text was generated."
            else:
                return f"Error: Unsupported company {self.company}"
        else:
            last_turn = conversation_history[-1]
            critique = self.critique(last_turn['text'])
            response = self.respond_to_critique(critique)
            return response
