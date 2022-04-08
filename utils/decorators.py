from functools import wraps


def singleton(cls):
    """
    生成单例的装饰器函数
    :param cls: 变成单例的类对象
    :return:
    """
    instance = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance
