import  os
from typing import List

from fastapi import Depends
import tensorflow as tf

from helpers.decorators import calculate_execution_time



NUM_CANDIDATES = 5


async def get_retrieval_model():
    retrieval_model = None

    async def load_retrieval_model():
        nonlocal retrieval_model
        if retrieval_model is None:
            model_path = os.path.join(os.path.dirname(__file__), 'retrieval_model')
            retrieval_model = tf.saved_model.load(model_path)
        return retrieval_model

    return await load_retrieval_model()

def is_model_loaded(model):
    return model is not None

@calculate_execution_time
async def generate_candidates(customer_features: List[str]):
                              #model = Depends(get_retrieval_model)):
    user_id = customer_features[0]
    model = await get_retrieval_model()

    affinity_scores, item_ids = model(
        tf.constant([user_id])
    )

    candidates = [item.decode() for item in item_ids[0, :NUM_CANDIDATES].numpy()]
    return candidates