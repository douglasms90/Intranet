from flask import abort, render_template, request
from datetime import date, timedelta
import flask_excel as excel

from intranet.ext.database import dbConn
from intranet.ext.forms import commForms


def index():
  form = commForms()
  conn = dbConn()
  if form.comm.data == 'os':
    rows = conn.consult("""SELECT json_build_object('ID', os.codos), json_build_object('DEFEITO', df.descricao_defeito), json_build_object('DESCRIÇÃO', tp.descricao), json_build_object('GERADA', os.data_abertura), json_build_object('CLIENTE', cl.nome_razaosocial), json_build_object('CIDADE', cd.cidade), json_build_object('BAIRRO', ba.bairro), json_build_object('DESCRIÇÃO', os.defeito_reclamado)
      FROM mk_os os
      FULL OUTER JOIN mk_os_tipo tp ON os.tipo_os = tp.codostipo
      JOIN mk_pessoas cl ON os.cliente = cl.codpessoa
      JOIN mk_os_defeitos df ON os.defeito_associado = df.coddefeito
      JOIN mk_cidades cd ON os.cd_cidade = cd.codcidade
      JOIN mk_bairros ba ON os.cd_bairro = ba.codbairro
      WHERE status='1' AND tipo_os in ('4','15','18') AND fechamento_tecnico='N' ORDER BY cd.cidade asc""")
    print(rows)
    return render_template("index.html", form=form, rows = rows)
  if form.comm.data == 're':
    rows = conn.consult("""SELECT os.codos, df.descricao_defeito, tp.descricao, os.data_fechamento, cl.nome_razaosocial, os.operador_fech_tecnico, os.servico_prestado
      FROM mk_os os
      FULL OUTER JOIN mk_os_tipo tp ON os.tipo_os = tp.codostipo
      JOIN mk_pessoas cl ON os.cliente = cl.codpessoa
      JOIN mk_os_defeitos df ON os.defeito_associado = df.coddefeito
      WHERE  tipo_os in ('4','15','18') AND data_fechamento = CURRENT_DATE AND servico_prestado LIKE '%ugl%' ORDER BY os.data_fechamento desc""")
    return render_template("index.html", form=form, rows = rows)
  if request.method == "POST":
    tomorrow = date.today() + timedelta(days=1)
    return excel.make_response_from_array(rows, "xlsx", file_name = tomorrow.strftime('%d.%m.%Y'))
  return render_template("index.html", form=form)