from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM strumento"
        cursor.execute(query)

        strumenti = []
        for row in cursor:
            # Creazione dell'oggetto Strumento a partire dai campi del DB
            s = Strumento(
                codice=row["codice"],
                tipo=row["tipo"],
                marca=row["marca"],
                anno_acquisto=row["anno_acquisto"],
                valore=row["valore"],
                disponibile=bool(row["disponibile"]) if "disponibile" in row else True
            )
            strumenti.append(s)

        cursor.close()
        cnx.close()
        return strumenti

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        # Usiamo LOWER per rendere la ricerca case-insensitive
        query = "SELECT * FROM strumento WHERE LOWER(tipo) = LOWER(%s)"
        cursor.execute(query, (tipo.strip(),))

        strumenti = []
        for row in cursor:
            s = Strumento(
                codice=row["codice"],
                tipo=row["tipo"],
                marca=row["marca"],
                anno_acquisto=row["anno_acquisto"],
                valore=row["valore"],
                disponibile=bool(row["disponibile"]) if "disponibile" in row else True
            )
            strumenti.append(s)

        cursor.close()
        cnx.close()
        return strumenti
