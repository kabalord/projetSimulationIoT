# projetSimulationIoT

## config.txt file

1. première ligne : période pendant laquelle si le leader n'a pas répondu, le nœud suppose que le leader est mort.
2. deuxième ligne : période pendant laquelle si le nœud n'a pas reçu de message correct, il suppose que c'est le leader.
3. troisième ligne : nombre de machines (n) dans le réseau.
4. les n lignes suivantes sont le ip_port pour la machine et sa priorité.

## comment démarrer 

exécuter le fichier main.py dans chaque machine et donnez-lui son ip_port comme paramètre par exemple :
```sh
$ python main.py 127.0.0.1:1111
```
