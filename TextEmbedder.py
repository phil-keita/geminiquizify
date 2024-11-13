from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

MODEL_NAME = 'text-embedding-004'
DIMENSIONS = 384
TASK = 'QUESTION_ANSWERING'

class TextEmbedder:

    def __init__(self):
        self.dim = DIMENSIONS
        self.task = TASK
        self.model_name = MODEL_NAME
        self.model = TextEmbeddingModel.from_pretrained(model_name=self.model_name)

    def embed_text(self, texts: list[str]) -> list[list[float]]:
        """ Embeds text with pretrained model
        Returns: 
            A list of lists containing the embedding vectors for each input text
        """
        inputs = [TextEmbeddingInput(text, self.task) for text in texts]
        kwargs = dict(output_dimensionality = self.dim) if self.dim else {}
        embeddings = self.model.get_embeddings(inputs, **kwargs)
        embeddings = [e.values for e in embeddings]
        return embeddings


