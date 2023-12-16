import psutil
from ctransformers import AutoModelForCausalLM

class LanguageModel:
    def __init__(self, verbose=True) -> None:
        self.verbose = verbose
        self.load_model()

    def load_model(self):
        """
        Dynamically load language model depending on memory of user.
        """

        SMALL_MODEL_REPO = "TheBloke/Llama-2-7B-GGUF"
        SMALL_MODEL_FILE = "llama-2-7b.Q4_K_M.gguf"
        LARGE_MODEL_REPO = "TheBloke/zephyr-7B-beta-GGUF"
        LARGE_MODEL_FILE = "zephyr-7b-beta.Q5_K_M.gguf"

        # Get total MB of memory of user
        memory = psutil.virtual_memory()
        total_memory = memory.total / 1024 / 1024

        # Load model depending on memory of user
        if total_memory < 10000:

            if self.verbose:
                print(f" WARNING: You have less than 10 GB of memory. This might cause problems. {SMALL_MODEL_REPO} will be loaded.")
            self._llm = AutoModelForCausalLM.from_pretrained(
                SMALL_MODEL_REPO,
                model_file=SMALL_MODEL_FILE,
                model_type="llama",
                local_files_only=True
            )
        else:

            if self.verbose:
                print(f" You have more than 10 GB of memory. {LARGE_MODEL_REPO} will be loaded.")
            try:
                self._llm = AutoModelForCausalLM.from_pretrained(model_path_or_repo_id='models/zephyr-7b-beta.Q5_K_M.gguf')
            except:
                self._llm = AutoModelForCausalLM.from_pretrained(
                    LARGE_MODEL_REPO,
                    model_file=LARGE_MODEL_FILE,
                    model_type="llama"
                )

    def get_answer(self, question: str) -> str:
        """
        Get answer from language model.

        :param question: question to be answered
        """

        if self.verbose:
            print(" Computing the answer (can take some time)...")
        return self._llm(question, max_new_tokens=100, temperature=0.4)
