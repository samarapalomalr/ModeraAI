"""
Script de seed para popular o banco SQLite local com dados de teste.
Permite testar os endpoints de histórico e a interface sem gastar cotas de APIs externas.
"""
import json
from datetime import datetime, timezone
from app.database import engine, Base, SessionLocal
from app.models import Audit

def seed():
    # Garante que as tabelas existem
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Verifica se já existem registros para não duplicar
        count = db.query(Audit).count()
        if count > 0:
            print(f"[SEED] Banco já possui {count} registros. Operação abortada para evitar duplicações.")
            return

        mock_audits = [
            Audit(
                platform="instagram",
                target_url="https://www.instagram.com/p/DB123456/",
                raw_content="Post patrocinado promovendo suplemento alimentar sem indicação clara de publi.",
                status="COMPLETED",
                summary="Violação de transparência publicitária: ausência de hashtag ou tag formal de parceria paga.",
                compliance_score=42,
                result_json=json.dumps({
                    "infractions": ["Falta de identificação de anúncio", "Alegações de saúde não comprovadas"],
                    "recommendation": "Adicionar #publi visível e aviso de consulta médica.",
                    "risk_level": "HIGH"
                }),
                created_at=datetime.now(timezone.utc)
            ),
            Audit(
                platform="instagram",
                target_url="https://www.instagram.com/p/DB654321/",
                raw_content="Vídeo institucional demonstrando linha de cosméticos veganos com selos de certificação.",
                status="COMPLETED",
                summary="Conformidade total com as diretrizes do CONAR e termos da plataforma.",
                compliance_score=98,
                result_json=json.dumps({
                    "infractions": [],
                    "recommendation": "Conteúdo aprovado para veiculação.",
                    "risk_level": "LOW"
                }),
                created_at=datetime.now(timezone.utc)
            ),
            Audit(
                platform="instagram",
                target_url="https://www.instagram.com/p/DB987654/",
                raw_content="Carrossel comparando dois produtos concorrentes com menção direta à marca rival.",
                status="COMPLETED",
                summary="Publicidade comparativa requer cautela quanto a depreciação de marca alheia.",
                compliance_score=70,
                result_json=json.dumps({
                    "infractions": ["Potencial depreciação desleal de concorrente"],
                    "recommendation": "Ajustar texto para focar exclusivamente nos atributos próprios.",
                    "risk_level": "MEDIUM"
                }),
                created_at=datetime.now(timezone.utc)
            ),
        ]

        db.add_all(mock_audits)
        db.commit()
        print(f"[SEED] Sucesso: {len(mock_audits)} auditorias de teste foram inseridas no banco SQLite!")

    except Exception as e:
        db.rollback()
        print(f"[SEED] Erro ao popular banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
