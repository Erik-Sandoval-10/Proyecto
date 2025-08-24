from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os
import database

PORT = 8000

class SGMHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.render_template("index.html")
        elif self.path == "/clientes":
            self.mostrar_clientes()
        elif self.path == "/equipos":
            self.mostrar_equipos()
        elif self.path == "/tecnicos":
            self.mostrar_tecnicos()
        elif self.path == "/ordenes":
            self.mostrar_ordenes()
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == "/clientes/agregar":
            self.agregar_cliente()
        elif self.path == "/equipos/agregar":
            self.agregar_equipo()
        elif self.path == "/tecnicos/agregar":
            self.agregar_tecnico()
        elif self.path == "/ordenes/agregar":
            self.agregar_orden()
        else:
            self.send_error(404, "Ruta no encontrada")

    # ---------- Utilidad para renderizar HTML ----------
    def render_template(self, filename, content=""):
        filepath = os.path.join("templates", filename)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{{content}}", content)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    # ---------- CLIENTES ----------
    def mostrar_clientes(self):
        conn = database.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
        conn.close()

        rows = "".join([f"<tr><td>{c['id']}</td><td>{c['nombre']}</td><td>{c['email'] or ''}</td><td>{c['telefono'] or ''}</td></tr>" for c in clientes])
        content = f"""
        <h2>Clientes</h2>
        <form method='POST' action='/clientes/agregar'>
            Nombre: <input name='nombre'> Email: <input name='email'> 
            Teléfono: <input name='telefono'>
            <button type='submit'>Agregar</button>
        </form>
        <table><tr><th>ID</th><th>Nombre</th><th>Email</th><th>Teléfono</th></tr>{rows}</table>
        """
        self.render_template("clientes.html", content)

    def agregar_cliente(self):
        data = self.parse_post()
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes (nombre, email, telefono) VALUES (%s,%s,%s,%s)",
                    (data.get("nombre"), data.get("email"), data.get("telefono")))
        conn.commit(); conn.close()
        self.redirect("/clientes")

    # ---------- EQUIPOS ----------
    def mostrar_equipos(self):
        conn = database.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT e.id, e.marca, e.modelo, c.nombre as cliente FROM equipos e JOIN clientes c ON e.cliente_id=c.id")
        equipos = cur.fetchall()
        conn.close()

        rows = "".join([f"<tr><td>{e['id']}</td><td>{e['marca']}</td><td>{e['modelo']}</td><td>{e['cliente']}</td></tr>" for e in equipos])
        content = f"""
        <h2>Equipos</h2>
        <form method='POST' action='/equipos/agregar'>
            Cliente ID: <input name='cliente_id'> Marca: <input name='marca'> 
            Modelo: <input name='modelo'> Serie: <input name='serie'> Tipo: <input name='tipo'>
            <button type='submit'>Agregar</button>
        </form>
        <table><tr><th>ID</th><th>Marca</th><th>Modelo</th><th>Cliente</th></tr>{rows}</table>
        """
        self.render_template("equipos.html", content)

    def agregar_equipo(self):
        data = self.parse_post()
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO equipos (cliente_id, marca, modelo, serie, tipo) VALUES (%s,%s,%s,%s,%s)",
                    (data.get("cliente_id"), data.get("marca"), data.get("modelo"), data.get("serie"), data.get("tipo")))
        conn.commit(); conn.close()
        self.redirect("/equipos")

    # ---------- TECNICOS ----------
    def mostrar_tecnicos(self):
        conn = database.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM tecnicos")
        tecnicos = cur.fetchall()
        conn.close()

        rows = "".join([f"<tr><td>{t['id']}</td><td>{t['nombre']}</td><td>{t['email'] or ''}</td></tr>" for t in tecnicos])
        content = f"""
        <h2>Técnicos</h2>
        <form method='POST' action='/tecnicos/agregar'>
            Nombre: <input name='nombre'> Email: <input name='email'> 
            Teléfono: <input name='telefono'>
            <button type='submit'>Agregar</button>
        </form>
        <table><tr><th>ID</th><th>Nombre</th><th>Email</th></tr>{rows}</table>
        """
        self.render_template("tecnicos.html", content)

    def agregar_tecnico(self):
        data = self.parse_post()
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tecnicos (nombre, email, telefono) VALUES (%s,%s,%s)",
                    (data.get("nombre"), data.get("email"), data.get("telefono")))
        conn.commit(); conn.close()
        self.redirect("/tecnicos")

    # ---------- ORDENES ----------
    def mostrar_ordenes(self):
        conn = database.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT o.id, o.tipo, o.estado, c.nombre as cliente FROM ordenes o JOIN equipos e ON o.equipo_id=e.id JOIN clientes c ON e.cliente_id=c.id")
        ordenes = cur.fetchall()
        conn.close()

        rows = "".join([f"<tr><td>{o['id']}</td><td>{o['tipo']}</td><td>{o['estado']}</td><td>{o['cliente']}</td></tr>" for o in ordenes])
        content = f"""
        <h2>Órdenes</h2>
        <form method='POST' action='/ordenes/agregar'>
            Equipo ID: <input name='equipo_id'> Técnico ID: <input name='tecnico_id'>
            Tipo: <input name='tipo'> Descripción: <input name='descripcion'>
            <button type='submit'>Agregar</button>
        </form>
        <table><tr><th>ID</th><th>Tipo</th><th>Estado</th><th>Cliente</th></tr>{rows}</table>
        """
        self.render_template("ordenes.html", content)

    def agregar_orden(self):
        data = self.parse_post()
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO ordenes (equipo_id, tecnico_id, tipo, descripcion) VALUES (%s,%s,%s,%s)",
                    (data.get("equipo_id"), data.get("tecnico_id"), data.get("tipo"), data.get("descripcion")))
        conn.commit(); conn.close()
        self.redirect("/ordenes")

    # ---------- UTILIDADES ----------
    def parse_post(self):
        length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(length).decode("utf-8")
        return {k: v[0] for k, v in urlparse.parse_qs(post_data).items()}

    def redirect(self, location):
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

httpd = HTTPServer(("", PORT), SGMHandler)
print(f"Servidor corriendo en http://localhost:{PORT}")
httpd.serve_forever()
