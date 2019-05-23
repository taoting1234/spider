import logging

# 创建一个logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(ch)
