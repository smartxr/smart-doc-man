import os

def get_params(search_resource: str, search_index: str, search_query: str):
    # SEARCH_INDEX_TYPE_EUGENIUS_GSC_SOURCEDOCS
    resource = search_resource.replace('-', '_').upper()
    index = search_index.replace("-", "_").upper()
    index_type = os.environ.get(f"SEARCH_INDEX_TYPE_{resource}_{index}")
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
