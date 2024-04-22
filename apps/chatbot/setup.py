from typing import Optional

from chain import Chain
from enums import ModelTypes, Models
from models import ModelFactory


def get_model_path_from_option(option: ModelTypes) -> Optional[str]:
    if option == ModelTypes.BASE:
        return None

    if option == ModelTypes.FINE_TUNED:
        # TODO
        return None

    if option == ModelTypes.FINE_TUNED_AND_CV:
        # TODO
        return None


def get_chain_from_option(
    system_prompt: str, model_option: Models, path_option: ModelTypes
):
    model_path = get_model_path_from_option(path_option)
    model = ModelFactory(model_path).create_model(model_option)
    chain = Chain(system_prompt, model)

    return chain
