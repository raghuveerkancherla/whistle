"""
Provides abstraction for data persistence and retrieval. Support for different
databases can be done by implementing DB specific repos.
It is expected that for each entity/resource combination, a repo is implemented
"""


class BaseEntityRepo(object):
    pass
