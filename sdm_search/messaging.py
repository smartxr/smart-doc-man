from datetime import datetime
import json
import urllib.parse

__all__ = [
    "parse_search_request",
    "get_params",
    "get_params_standard",
    "get_params_standard_chunked",
    "parse_search_results",
]

def parse_search_request(parameters: dict):
    return (
        parameters.get("search_query", ""),
        parameters.get("search_resource", "none"),
        parameters.get("search_index", "none"),
        parameters.get("page", 1),
    )


def get_params(index_type: str, search_query: str):
    if index_type:
        if index_type == "standard-chunked":
            return get_params_standard_chunked(search_query)
        # elif index_type == 'standard-whole':
        #     return get_params_standard_whole(search_query)
        else:
            return get_params_standard(search_query)
    return get_params_standard(search_query)


def get_params_standard(search_request):
    return {
        "api-version": "2023-11-01",
        "search": search_request,  # 'music*',
        "queryType": "semantic",  # full, semantic
        "searchMode": "all",
        #'searchFields': 'content',
        "highlight": "content",
        "highlightPreTag": "<mark>",
        "highlightPostTag": "</mark>",
        #'queryLanguage': 'en-US',
        #'enableFuzzyMatching': 'true',
        #'fuzzyType': 'auto',
        #'speller': 'lexicon',
        #'scoringProfile': 'text',
        "captions": "extractive",
        #'answerFields': 'extractive',
        #'answers': 'extractive|count-3', # extractive%7Ccount-3
        "semanticConfiguration": "default",
        # 'semanticDistance': '2',
        # 'semanticScore': '0.5',
        # 'semanticHighlight': 'true',
        # 'semanticFilters': 'true',
        # 'semanticSort': 'true',
        "$count": "true",
        "$top": "50",
        "$skip": "0",
        "$select": "filename,url",  # filepath # *
        #'$filter': 'language eq \'en\''
    }


def get_params_standard_chunked(search_request):
    return {
        "api-version": "2023-11-01",
        "search": search_request,  # 'music*',
        "queryType": "semantic",  # full, semantic
        "searchMode": "all",
        #'searchFields': 'content',
        "highlight": "content",
        "highlightPreTag": "<mark>",
        "highlightPostTag": "</mark>",
        #'queryLanguage': 'en-US',
        #'enableFuzzyMatching': 'true',
        #'fuzzyType': 'auto',
        #'speller': 'lexicon',
        #'scoringProfile': 'text',
        "captions": "extractive",
        #'answerFields': 'extractive',
        #'answers': 'extractive|count-3', # extractive%7Ccount-3
        "semanticConfiguration": "default",
        # 'semanticDistance': '2',
        # 'semanticScore': '0.5',
        # 'semanticHighlight': 'true',
        # 'semanticFilters': 'true',
        # 'semanticSort': 'true',
        "$count": "true",
        "$top": "50",
        "$skip": "0",
        "$select": "filepath,url,chunk_id",
        # '$select': '*',
        #'$filter': 'language eq \'en\''
    }


def parse_search_results(payload: dict):
    results = []
    count = payload.get("@odata.count", "0")
    values = payload.get("value", [])

    for value in values:
        source_location = ">>>" + urllib.parse.unquote(
            value["url"][8:].split("/", 1)[1]
        )
        if "filename" in value:
            source_name = value["filename"]
        elif "filepath" in value:
            source_name = value["filepath"]
        else:
            source_name = "NOT IDENTIFIED"

        if "chunk_id" in value:
            source_name += f" (chunk {value['chunk_id']})"

        highlights = []
        if "@search.highlights" in value:
            for highlight in value["@search.highlights"].get("content", []):
                escape_value = "\n"
                highlights.append(f"{highlight.replace(escape_value, '<br>')}")

        captions = []
        if "@search.captions" in value:
            for caption in value["@search.captions"]:
                escape_value = "\n"
                captions.append(
                    f"{caption['highlights'].replace(escape_value, '<br>')}"
                )

        results.append(
            {
                "filename": source_name,
                "url": source_location,
                "highlights": highlights,
                "captions": captions,
            }
        )

    return {"count": count, "values": results}
