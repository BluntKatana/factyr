import psutil
from ctransformers import AutoModelForCausalLM

class LanguageModel:
    def __init__(self) -> None:
        # Get total MB of memory of user
        memory = psutil.virtual_memory()
        total_memory = memory.total / 1024 / 1024
        print(f"Total memory: {total_memory} MB")

        # Load model depending on memory of user
        if total_memory < 10000:
            repository="TheBloke/Llama-2-7B-GGUF"
            model_file="llama-2-7b.Q4_K_M.gguf"
            print(f"WARNING: You have less than 10 GB of memory. This might cause problems. {repository} will be loaded.")
            self._llm = AutoModelForCausalLM.from_pretrained(
                repository,
                model_file=model_file,
                model_type="llama",
                local_files_only=True
            )
        else:
            repository="TheBloke/zephyr-7B-beta-GGUF"
            model_file="zephyr-7b-beta.Q5_K_M.gguf"
            print(f"You have more than 10 GB of memory. ${repository} will be loaded.")
            self._llm = AutoModelForCausalLM.from_pretrained(repository, model_file=model_file, model_type="llama")
        pass

    def get_answer(self, question: str) -> str:
        """
        Get answer from language model.

        :param question: question to be answered
        """
        print("Computing the answer (can take some time)...")
        return self._llm(question, max_new_tokens=100, temperature=0.4)
