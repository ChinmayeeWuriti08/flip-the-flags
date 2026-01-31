# Temporary experiment for ranking improvements
ENABLE_NEW_SEARCH = False

def search(query):
    if ENABLE_NEW_SEARCH:
        return experimental_search(query)
    return legacy_search(query)
