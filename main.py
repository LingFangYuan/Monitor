import json, os, logging.config
import sendMail
import importlib

modules_dict = {}


def im_module(path='./conf/module.json'):
    """
    动态加载模块
    :param path: 模块配置文件路径
    :return:
    """
    with open(path, 'r') as f:
        mddict = json.load(f)
    for k in mddict:
        modules_dict[importlib.import_module(k)] = mddict[k]
    del mddict


def setup_logging(default_path='./conf/logging.json'):
    if not os.path.exists(default_path):
        default_path = './conf/logging.json'
    with open(default_path, 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)


if __name__ == '__main__':
    im_module()
    setup_logging()
    logger = logging.getLogger('error_file')
    try:

        # 执行动态模块中的函数，目前默认无参
        for k in modules_dict:
            for met in modules_dict[k]:
                getattr(k, met)()

    except Exception as e:
        try:
            sendMail.send('410982322@qq.com', 'E3+监控程序出错', str(e))
        except Exception as e1:
            logger.exception(e1)
        logger.exception(e)
