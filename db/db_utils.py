import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase, DuplicateTable

import subprocess
import shlex

import json

from django.conf import settings
from django.db import connection

from db.core.models import Tenant


def run_command(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)


def create_tenant_schema(company_name):
    schema_name = company_name.lower().replace(" ", "_")
    final_schema_name = schema_name + "_schema"

    db_settings = settings.DATABASE_HOST_SETTINGS 
    HOST = db_settings['HOST']
    PASSWORD = db_settings['PASSWORD']
    PORT = db_settings['PORT']
    USER = db_settings['USER']
    DB_NAME = db_settings["NAME"]

    con = psycopg2.connect(
        database=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    with con.cursor() as cur:
        cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(
            sql.Identifier(final_schema_name))
        )

    tenant_db = {
        schema_name: dict(
            OPTIONS={'options': f"-c search_path={final_schema_name}"},
            **db_settings
        )
    }
    tenant = Tenant.objects.get_or_create(
        company_name=company_name, 
        db_name=schema_name,
        db_conf=tenant_db    
    )
    
    if tenant[1]:
        run_command(f"python {settings.BASE_DIR}/manage.py runscript update_db_conf")
        run_command(f"python {settings.BASE_DIR}/manage.py migrate --database {schema_name}")
    
    return tenant


