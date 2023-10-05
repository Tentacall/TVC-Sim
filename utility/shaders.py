import logging

def loadShaders(path):
    with open(path, 'r') as f:
        return f.read()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Running utility/shaders.py tests")
    
    s = loadShaders("/home/rupak/Desktop/github/SimModule/assets/shaders/vertex/vertex_v110.vs")
    print(type(s), s)
