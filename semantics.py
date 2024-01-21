#!/usr/bin/env python3
import json
import random
import requests
from sentence_transformers import SentenceTransformer, util
import torch


def rescale(sim_score):
    """Rescale the similarity scores"""
    if sim_score >= 0.4:
        scale_factor = 1 - sim_score
        return sim_score * (1 + scale_factor)
    if sim_score >= 0.25:
        scale_factor = 1 + sim_score
        return sim_score * scale_factor
    else:
        return sim_score * 0.5


def random_word_generator():
    """Generate random words and their synonyms"""
    api_url = "https://random-word-api.vercel.app/api?words=1"

    # Only return random word if its synonyms exist
    synonyms_exist = False
    while synonyms_exist == False:
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            # Return the random word
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
            # Return the thesaurus dictionary
            thes_dict = json.loads(response_thes.text)
            print(thes_dict)
            if len(thes_dict["synonyms"]) >= 1:
                synonyms_exist = True
        else:
            print("Error:", response.status_code, response.text)

    return {"random_word": random_word, "synonyms": thes_dict["synonyms"]}


def semantics(word, input_word):
    """
    Compute word embeddings and compute cosine similarity score between them to return a similarity score
    """

    # Define the model
    model = SentenceTransformer("all-mpnet-base-v2")

    # Compute the embeddings for input word
    embeddings_word = model.encode(word)
    embeddings_input = model.encode(input_word)

    # Compute the cosine simularity score
    similarity_matrix_same = util.cos_sim(embeddings_word, embeddings_word)
    similarity_matrix_input = util.cos_sim(embeddings_word, embeddings_input)

    # Rescale the scores
    rescaled_scores = [rescale(i) for i in similarity_matrix_input.tolist()[0]]

    # Output the word and score to dictionary
    semant_dict = dict(
        zip(
            input_word if isinstance(input_word, list) else [input_word],
            rescaled_scores,
        )
    )
    return semant_dict


def provide_hint(random_word, synonyms, highest_score):
    """Compute rescaled similarity score of the synonyms and return tuple of the next highest based on the highest score"""

    # Compute rescaled similarity scores of the synonyms
    syn_scores = semantics(random_word, synonyms)

    # Return dictionary of synonyms higher than current highest score
    syn_scores_higher = {
        synonym: score for synonym, score in syn_scores.items() if score > highest_score
    }

    # Sort the syn_scores_higher dictionary
    sorted_syn_scores_higher = sorted(syn_scores_higher.items(), key=lambda x: x[1])

    if sorted_syn_scores_higher:
        synonym, synonym_score = sorted_syn_scores_higher[0]
        return (synonym, synonym_score)
    else:
        return ("No higher score exists!", 0)


def main(random_word, your_input):
    """C ompute the rescaled similarity score of the input word"""
    while True:
        try:
            res = semantics(random_word, your_input)
            return res
        except KeyboardInterrupt:
            print(" Exiting...")
            break
