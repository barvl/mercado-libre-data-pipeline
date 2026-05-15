import sqlalchemy as sa

# Datos del Session Pooler
DATABASE_URL = "postgresql://postgres.udbpzomalscregiythfy:#HolaZayn32@aws-1-us-east-1.pooler.supabase.com:5432/postgres"

try:
    engine = sa.create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(sa.text("SELECT version()"))
        print("✅ Conexión exitosa!")
        print(result.fetchone()[0])
except Exception as e:
    print(f"❌ Error: {e}")