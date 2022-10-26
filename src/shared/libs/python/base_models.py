class Item:
    def __init__(self, pk, sk):
        print(f"Creando keys {pk}, {sk}")

        self.pk = pk
        self.sk = sk

    def get_keys(self):
        return {
            "PK": self.pk,
            "SK": self.sk
        }