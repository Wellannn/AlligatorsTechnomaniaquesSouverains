import os
import json

class StorageJSON:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)
        else:
            with open(self.filename, 'r') as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    # Fichier corrompu ou vide, le réinitialiser
                    with open(self.filename, 'w') as f_write:
                        json.dump({}, f_write)
