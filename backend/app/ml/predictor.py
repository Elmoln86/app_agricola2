from .models import DummyVisionModel, DummyTSModel
import uuid

class RecommendationEngine:
    def __init__(self):
        self.vision = DummyVisionModel()
        self.ts = DummyTSModel()

    def analyze_image_bytes(self, b: bytes):
        r = self.vision.predict(b)
        if r['praga'] == 'bicho-mineiro':
            plan = {
                'action': 'Aplicar bioinsumo X',
                'dose': '0.8 L/ha',
                'window': '24-48h'
            }
        else:
            plan = {'action': 'Monitorar', 'confidence': r['confidence']}
        return {'detection': r, 'plan': plan}

    def recommend_irrigation(self, weather: dict, talhao_id: int):
        irrig = False
        if weather['chuva_3h'] < 2 and weather['umidade'] < 60:
            irrig = True
        return {
            'talhao': talhao_id,
            'recommend': 'Irrigar 10mm' if irrig else 'Não irrigar',
            'weather': weather
        }

    def chat_with_producer(self, message: str, session_id: str = None):
        sid = session_id or str(uuid.uuid4())
        msg = message.lower()
        if 'irrig' in msg:
            text = 'Recomendo checar umidade do solo; se <60% irrigar 10mm amanhã às 6h.'
        elif 'praga' in msg or 'bicho' in msg:
            text = 'Detectamos sinais de bicho-mineiro em imagens recentes. Plano: aplicar bioinsumo X 0.8 L/ha.'
        else:
            text = 'Posso ajudar com recomendações de irrigação, controle de pragas, ou gerar relatório da lavoura. O que deseja?'
        return {'session_id': sid, 'response': text, 'report_url': None}
