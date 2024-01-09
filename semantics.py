#!/usr/bin/env python3
import json
from py_thesaurus import Thesaurus
import random
import requests
from sentence_transformers import SentenceTransformer, util
import torch


def rescale(sim_score):
    if sim_score >= 0.4:
        scale_factor = 1 - sim_score
        return sim_score * (1 + scale_factor)
    if sim_score >= 0.25:
        scale_factor = 1 + sim_score
        return sim_score * scale_factor
    else:
        return sim_score * 0.5


def random_word_generator():
    api_url = "https://random-word-api.vercel.app/api?words=1"

    synonyms_exist = False
    while synonyms_exist == False:
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            random_word = response.text[2:-2]
            print(random_word)
        else:
            print("Error:", response.status_code, response.text)

        api_url_thes = f"https://api.api-ninjas.com/v1/thesaurus?word={random_word}"
        response_thes = requests.get(
            api_url_thes,
            headers={"X-Api-Key": "+XSDNplJlqtLJd9oMNSwkQ==c9VJ7riqTrFnZyGf"},
        )
        if response_thes.status_code == requests.codes.ok:
            thes_dict = json.loads(response_thes.text)
            print(thes_dict)
            if len(thes_dict["synonyms"]) >= 1:
                synonyms_exist = True
        else:
            print("Error:", response.status_code, response.text)

    return {"random_word": random_word, "thesaurus": thes_dict}


def semantics(word, input_word):
    model = SentenceTransformer("all-mpnet-base-v2")

    embeddings_word = model.encode(word)
    embeddings_input = model.encode(input_word)

    similarity_matrix_same = util.cos_sim(embeddings_word, embeddings_word)
    similarity_matrix_input = util.cos_sim(embeddings_word, embeddings_input)

    rescaled_score = rescale(similarity_matrix_input.item())

    similarity_percentage = (
        "{0:1.2f}".format((rescaled_score / similarity_matrix_same.item()) * 100) + " %"
    )

    return {"rescaled_score": rescaled_score, "percentage": similarity_percentage}


def main(your_input, random_word):
    while True:
        try:
            res = semantics(random_word, your_input)["percentage"]
            print(res)
            return res
        except KeyboardInterrupt:
            print(" Exiting...")
            break
