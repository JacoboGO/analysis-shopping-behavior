"""
Carga un DataFrame de pandas procesado en PostgreSQL usando SQLAlchemy.

Requiere:
    pip install pandas sqlalchemy psycopg2-binary python-dotenv

Variables de entorno esperadas en un archivo .env (NO versionado, agrégalo a .gitignore):
    PG_HOST=localhost
    PG_PORT=5432
    PG_DB=customer_behavior
    PG_USER=postgres
    PG_PASSWORD=tu_password
"""

import os
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_engine(env_path: Optional[Union[str, Path]] = None) -> Engine:
    """
    Crea el engine de conexión a PostgreSQL a partir de variables de entorno.

    Args:
        env_path: ruta explícita al archivo .env. Si es None, load_dotenv()
            busca .env en el directorio de trabajo actual del kernel —
            en notebooks de VS Code eso NO siempre es la raíz del proyecto,
            así que se recomienda pasarlo explícito para evitar ambigüedad.
    """
    load_dotenv(dotenv_path=env_path)

    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "5432")
    db = os.getenv("PG_DB")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")

    if not all([db, user, password]):
        raise ValueError(
            "Faltan variables de entorno. Verifica PG_DB, PG_USER, PG_PASSWORD en tu .env"
        )

    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(
        connection_string,
        pool_pre_ping=True,
        # Fuerza los mensajes de error del servidor a inglés/ASCII para esta
        # sesión. Sin esto, un PostgreSQL con locale en español puede devolver
        # errores con «comillas angulares» (byte 0xab en Latin-1), que psycopg2
        # falla al decodificar como UTF-8 — enmascarando el error real detrás
        # de un UnicodeDecodeError. No requiere tocar postgresql.conf.
        connect_args={"options": "-c lc_messages=C"},
    )


def load_dataframe_to_postgres(
    df: pd.DataFrame,
    table_name: str,
    if_exists: str = "replace",
    chunksize: int = 5000,
    env_path: Optional[Union[str, Path]] = None,
) -> None:
    """
    Carga un DataFrame en PostgreSQL con validación previa y confirmación posterior.

    Args:
        df: DataFrame ya procesado y validado.
        table_name: nombre de la tabla destino en el esquema 'public'.
        if_exists: 'replace' | 'append' | 'fail'.
        chunksize: filas por lote de inserción.
        env_path: ruta explícita al .env (ver get_engine).
    """
    if df.empty:
        raise ValueError("El DataFrame está vacío; no hay nada que cargar.")

    engine = get_engine(env_path=env_path)

    try:
        # engine.begin() = transacción atómica: si algo falla, no queda
        # una tabla parcialmente cargada (el bug que viste en pgAdmin).
        with engine.begin() as conn:
            df.to_sql(
                name=table_name,
                con=conn,
                schema="public",
                if_exists=if_exists,
                index=False,
                chunksize=chunksize,
                method="multi",  # inserta en lotes en vez de fila por fila
            )

        # Verificación post-carga: nunca confíes en que "no hubo error" = "se cargó todo"
        with engine.connect() as conn:
            result = conn.execute(text(f'SELECT COUNT(*) FROM public."{table_name}"'))
            row_count = result.scalar()

        print(f"✓ Carga completada: {row_count} filas en '{table_name}' "
              f"(esperadas: {len(df)})")

        if row_count != len(df):
            print("⚠ El conteo no coincide con el DataFrame original. "
                  "Revisa duplicados, constraints o filtros silenciosos.")

    except Exception as e:
        print(f"✗ Error al cargar datos: {type(e).__name__}: {e}")
        raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    # Este bloque SOLO se ejecuta si corres el script directo desde terminal
    # (python load_df_to_postgres.py). Si lo importas en un notebook con
    # `from load_df_to_postgres import load_dataframe_to_postgres`,
    # este bloque NO se ejecuta — por eso es seguro dejarlo como referencia.
    #
    # Ajusta la ruta solo si de verdad guardaste un CSV intermedio en disco.
    csv_path = Path("data/processed/customer_shopping_behavior_processed.csv")
    if not csv_path.exists():
        raise FileNotFoundError(
            f"No se encontró {csv_path.resolve()}. "
            "Si tu DataFrame ya está en memoria en un notebook, no ejecutes "
            "este archivo completo: importa la función en su lugar (ver README)."
        )
    df = pd.read_csv(csv_path)

    load_dataframe_to_postgres(
        df=df,
        table_name="customer_behavior",
        if_exists="replace",
    )
