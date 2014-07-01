from whistle.handler import Handler


def is_pipeline(pipeline):
    if isinstance(pipeline, list):
        handler_functions = filter(lambda x: isinstance(x, Handler), pipeline)
        return len(pipeline) == len(handler_functions)
    else:
        return False
