import os

def prepDir(root_dirs):
        for root_dir in root_dirs:
                #check if the directory exits
                if not os.path.isdir(root_dir):
                        os.makedirs(root_dir)
                else:
                        for entity in os.listdir(root_dir):
                                if os.path.isfile(os.path.join(root_dir, entity)):
                                        os.remove(os.path.join(root_dir, entity))
