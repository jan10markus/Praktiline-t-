CONFIG = open("config.txt", "r+")
a = CONFIG.read().split("\n")
print(a)
CONFIG.close()