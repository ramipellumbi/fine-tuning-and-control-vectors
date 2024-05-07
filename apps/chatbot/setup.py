from typing import Optional

from enums import ModelTypes, Models
from models import ModelFactory


def get_model_path_from_option(
    model_options: Models, option: Optional[ModelTypes]
) -> Optional[str]:
    # We never fine tuned or control vectored LLAMA
    if model_options == Models.LLAMA:
        # DO NOT EDIT THIS
        return None

    if option == ModelTypes.BASE:
        return None

    if option == ModelTypes.FINE_TUNED:
        # TODO: EDIT THIS WITH YOUR FINE TUNED PATH
        return None

    if option == ModelTypes.FINE_TUNED_AND_CV:
        # TODO: EDIT THIS WITH YOUR CV PATH
        return None


def get_model_from_options(model_option: Models, path_option: Optional[ModelTypes]):
    model_path = get_model_path_from_option(model_option, path_option)
    model = ModelFactory.create_model(model_option, model_path)

    return model
