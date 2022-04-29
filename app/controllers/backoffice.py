from flask import render_template
from datetime import date
import flask_excel as excel

from app import app
from app.models.tables import databaseConnection


@app.route("/backoffice", methods = ["GET"])
def backoffice():
  connect = databaseConnection("dbname='' user='' host='' password=''")
  database = connect.consult("""SELECT os.codos, df.descricao_defeito, tp.descricao, os.data_fechamento, cl.nome_razaosocial, os.operador_fech_tecnico, os.servico_prestado
    FROM mk_os os
    FULL OUTER JOIN mk_os_tipo tp ON os.tipo_os = tp.codostipo
    JOIN mk_pessoas cl ON os.cliente = cl.codpessoa
    JOIN mk_os_defeitos df ON os.defeito_associado = df.coddefeito
    WHERE  tipo_os in ('4','15','18') AND data_fechamento = CURRENT_DATE AND servico_prestado LIKE '%ug%' ORDER BY os.data_fechamento desc""")
  connect.close()
  return render_template("backoffice.html", rows = database)
