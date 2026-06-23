"""
Note 1:
    Ideally services and repositories should be kept in separate sub-directories 
    but to keep the project structure simple, I am keeping them together \
    under services/ for now.

Note 2:
    Db sessions should be passed on from routes to services, instead of \
    services creating their own db sessions. This ensures a single session \
    is being used for the overall request lifecycle.
"""
