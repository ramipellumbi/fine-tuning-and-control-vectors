from typing import Optional

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


def get_model_from_options(model_option: Models, path_option: ModelTypes):
    model_path = get_model_path_from_option(path_option)
    model = ModelFactory.create_model(model_option, model_path)

    return model
