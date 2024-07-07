from os import getenv
from openai import OpenAI
from httpx import Client
from wonderwords import RandomSentence

class Embedder:
	def __init__(self):
		self.scw_client = OpenAI(
			base_url=getenv("MODEL_URL"),
			api_key=getenv("SCALEWAY_SECRET_KEY"),
			http_client=Client(
				verify=False,
			),
		)

	def embed(self, text: str) -> list[float]:
		response = self.scw_client.embeddings.create(
			input=text,
			model="sentence-t5-xxl",
		)
		if response.data is None:
			raise Exception("No data in response.")
		if len(response.data) != 1:
			raise Exception(f"Expected 1 embedding, but got {len(response.data)}.")
		if len(response.data[0].embedding) != 768:
			raise Exception(f"Expected embedding of dimension 768, but got {len(response.data[0].embedding)}.")
		return response.data[0].embedding