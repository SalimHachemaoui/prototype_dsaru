import os
import schedule
from datetime import datetime

def delete_old_folder():
    # Chemin du dossier principal
    main_folder_path = '/storage_runs/'
    
    # Récupération de la liste des dossiers dans le dossier principal
    folders = os.listdir(main_folder_path)
    
    # Pour chaque dossier dans le dossier principal...
    for folder in folders:
        # Chemin complet du dossier
        folder_path = os.path.join(main_folder_path, folder)
        
        # Vérification de l'heure de création du dossier
        folder_ctime = os.stat(folder_path).st_ctime
        folder_ctime_datetime = datetime.fromtimestamp(folder_ctime)
        
        # Si le dossier a été créé il y a plus de 8 heures...
        if datetime.now() - folder_ctime_datetime > datetime.timedelta(hours=8):
            # Suppression du dossier et de tout son contenu
            os.rmtree(folder_path)
