def get_sql(path):
    """
    读取SQL脚本
    :param path: SQL脚本路径
    :return: 返回SQL字符串
    """
    with open(path, 'r', encoding="utf-8") as f:
        data = f.read().encode("utf-8").decode("utf-8-sig")
        return data
