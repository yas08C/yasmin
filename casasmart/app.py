# CasaSmart - interface simples feita com Flask
# Para rodar: python app.py  e abrir http://localhost:5000

from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "casasmart123"


def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="yasmin",
        database="casasmart"
    )


# ---------- PAGINA INICIAL ----------
@app.route("/")
def index():
    conn = conectar()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM comodo")
    comodos = cur.fetchall()

    # para cada comodo, busca os sensores e os atuadores
    for c in comodos:
        cur.execute("SELECT * FROM sensor WHERE id_comodo = %s", (c["id"],))
        c["sensores"] = cur.fetchall()

        # pega a ultima leitura de cada sensor
        for s in c["sensores"]:
            cur.execute(
                "SELECT valor, data_hora FROM leitura WHERE id_sensor = %s ORDER BY data_hora DESC LIMIT 1",
                (s["id"],)
            )
            s["ultima"] = cur.fetchone()

        cur.execute("SELECT * FROM atuador WHERE id_comodo = %s", (c["id"],))
        c["atuadores"] = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("index.html", comodos=comodos)


# ---------- COMODOS ----------
@app.route("/comodos")
def comodos():
    conn = conectar()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comodo")
    lista = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("comodos.html", comodos=lista)


@app.route("/comodos/novo", methods=["POST"])
def novo_comodo():
    nome = request.form["nome"]
    conn = conectar()
    cur = conn.cursor()
    # usuario 1 fixo (ainda nao fiz o login)
    cur.execute("INSERT INTO comodo (nome, id_usuario) VALUES (%s, 1)", (nome,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Cômodo adicionado!")
    return redirect("/comodos")


@app.route("/comodos/<int:id>/renomear", methods=["POST"])
def renomear_comodo(id):
    nome = request.form["nome"]
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE comodo SET nome = %s WHERE id = %s", (nome, id))
    conn.commit()
    cur.close()
    conn.close()
    flash("Nome alterado!")
    return redirect("/comodos")


@app.route("/comodos/<int:id>/apagar", methods=["POST"])
def apagar_comodo(id):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM comodo WHERE id = %s", (id,))
        conn.commit()
        flash("Cômodo apagado!")
    except Exception:
        # da erro se o comodo ainda tem sensor ou atuador (chave estrangeira)
        flash("Não deu para apagar: esse cômodo ainda tem sensores ou atuadores.")
    cur.close()
    conn.close()
    return redirect("/comodos")


# ---------- ATUADORES ----------
@app.route("/atuadores")
def atuadores():
    conn = conectar()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT atuador.id, atuador.nome, atuador.tipo, atuador.estado, comodo.nome AS comodo "
        "FROM atuador JOIN comodo ON atuador.id_comodo = comodo.id"
    )
    lista = cur.fetchall()
    cur.execute("SELECT * FROM comodo")
    comodos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("atuadores.html", atuadores=lista, comodos=comodos)


@app.route("/atuadores/<int:id>/alternar", methods=["POST"])
def alternar_atuador(id):
    conn = conectar()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT estado FROM atuador WHERE id = %s", (id,))
    atuador = cur.fetchone()

    if atuador["estado"] == "ligado":
        novo_estado = "desligado"
    else:
        novo_estado = "ligado"

    cur.execute("UPDATE atuador SET estado = %s WHERE id = %s", (novo_estado, id))
    conn.commit()
    cur.close()
    conn.close()
    # volta para a pagina de onde veio
    return redirect(request.referrer or "/")


@app.route("/atuadores/novo", methods=["POST"])
def novo_atuador():
    nome = request.form["nome"]
    tipo = request.form["tipo"]
    id_comodo = request.form["id_comodo"]
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO atuador (nome, tipo, estado, id_comodo) VALUES (%s, %s, 'desligado', %s)",
        (nome, tipo, id_comodo)
    )
    conn.commit()
    cur.close()
    conn.close()
    flash("Atuador adicionado!")
    return redirect("/atuadores")


@app.route("/atuadores/<int:id>/apagar", methods=["POST"])
def apagar_atuador(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM atuador WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Atuador apagado!")
    return redirect("/atuadores")


# ---------- LEITURAS ----------
@app.route("/leituras")
def leituras():
    conn = conectar()
    cur = conn.cursor(dictionary=True)

    # se o usuario marcou "so acima de 28", filtra
    so_altas = request.args.get("altas")
    if so_altas:
        cur.execute(
            "SELECT leitura.id, leitura.valor, leitura.data_hora, sensor.nome AS sensor "
            "FROM leitura JOIN sensor ON leitura.id_sensor = sensor.id "
            "WHERE leitura.valor > 28 ORDER BY leitura.data_hora DESC"
        )
    else:
        cur.execute(
            "SELECT leitura.id, leitura.valor, leitura.data_hora, sensor.nome AS sensor "
            "FROM leitura JOIN sensor ON leitura.id_sensor = sensor.id "
            "ORDER BY leitura.data_hora DESC"
        )
    lista = cur.fetchall()

    cur.execute("SELECT COUNT(*) AS total FROM leitura")
    total = cur.fetchone()["total"]

    cur.execute("SELECT * FROM sensor")
    sensores = cur.fetchall()

    cur.close()
    conn.close()

    agora = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template("leituras.html", leituras=lista, total=total,
                           sensores=sensores, agora=agora, so_altas=so_altas)


@app.route("/leituras/nova", methods=["POST"])
def nova_leitura():
    valor = request.form["valor"]
    data_hora = request.form["data_hora"].replace("T", " ")
    id_sensor = request.form["id_sensor"]
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO leitura (valor, data_hora, id_sensor) VALUES (%s, %s, %s)",
        (valor, data_hora, id_sensor)
    )
    conn.commit()
    cur.close()
    conn.close()
    flash("Leitura registrada!")
    return redirect("/leituras")


@app.route("/leituras/<int:id>/apagar", methods=["POST"])
def apagar_leitura(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM leitura WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Leitura apagada!")
    return redirect("/leituras")


if __name__ == "__main__":
    app.run(debug=True)
