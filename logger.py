import logging
import config
import time
import os


now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))


class logcls:
    # _singleton = None
    # logger = None

    def __init__(self, arg):
        # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        filename = "log\\"+str(arg)+"\\"+now + r"_log.txt"
        file_dir = os.path.split(filename)[0]
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        # if self._singleton is None:
        #     self._singleton = logcls(arg)
        logger = logging.getLogger(arg)
        if not logger.handlers:
            logger.setLevel(level=logging.DEBUG)
            handler = logging.FileHandler(filename)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self.logger = logger
        # return self._singleton

    def log(self, msg):
        #if logcls._singleton is None:
            #logcls._singleton = logcls()
        self.logger.info(str(msg) + '\n')
        # logger.debug(msg)
        # logger.warning(msg)
        # logger.info(msg)

    def debug(self, msg):
        self.logger.debug(str(msg) + '\n')




class rstcls:
    _singleton = None
    logger1 = None

    def __init__(self):
        pass

    @staticmethod
    def initial(arg):

        filename1 = "log\\"+now + r"_result.txt"
        if 'log' not in os.listdir(os.getcwd()):
            try:
                os.mkdir('log')
            except:
                pass
        if rstcls._singleton is None:
            rstcls._singleton = rstcls()
        logger1 = logging.getLogger(str(arg))

        if not logger1.handlers:
            logger1.setLevel(level=logging.INFO)
            handler = logging.FileHandler(filename1)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger1.addHandler(handler)
        rstcls.logger1 = logger1
        return rstcls._singleton


    @staticmethod
    def log(msg):
        #if logcls._singleton is None:
            #logcls._singleton = logcls()
        rstcls.logger1.info(str(msg))
        # logger.debug(msg)
        # logger.warning(msg)
        # logger.info(msg)
