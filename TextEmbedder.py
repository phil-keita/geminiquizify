from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

MODEL_NAME = 'text-embedding-004'
DIMENSIONS = 384 #Be careful when changing this. This is the dimensionality for ChromnaDB. Anything else will crash the code
TASK = 'RETRIEVAL_QUERY'

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
        # This embedding modal only allows 250 elements per request
        inputs_list = [inputs[i:i + 250] for i in range(0, len(inputs), 250)] 
        result = []
        for input in inputs_list:
            embeddings = self.model.get_embeddings(input, **kwargs)
            result += [e.values for e in embeddings]
        return result


