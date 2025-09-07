class DummyVisionModel:
    def predict(self, image_bytes: bytes):
        return {"praga": "bicho-mineiro", "confidence": 0.78}

class DummyTSModel:
    def predict(self, features: dict):
        return {"produtividade_kg_ha": 2300}
