from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

lista_usuarios_global = []

#PRINCIPAL MENU
# ==========================================
@app.route("/")
def principal():
    return render_template("index.html")

#REGISTRAR
# ==========================================
@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        not1 = request.form['not1']
        not2 = request.form['not2']
        not3 = request.form['not3']
        
        registro = (nombre, apellido, dni, not1, not2, not3)
        lista_usuarios_global.append(registro)
        
        return redirect(url_for('principal'))
        
    return render_template("registrar.html")

#BUSCAR
# ==========================================
@app.route("/buscar", methods=['GET', 'POST'])
def buscar():
    resultado = None
    buscado = False
    
    if request.method == 'POST':
        
        nombre_buscar = request.form['nombre_buscar']
        buscado = True
        
        for i in range(len(lista_usuarios_global)):
            
            if lista_usuarios_global[i][0] == nombre_buscar:
                
                resultado = lista_usuarios_global[i]
                
                break
                
    return render_template("buscar.html", resultado=resultado, buscado=buscado)

#EDITAR
# ==========================================
@app.route("/editar", methods=['GET', 'POST'])
def editar():
    resultado = None
    buscado = False
    
    if request.method == 'POST':
        
        if 'nombre_buscar' in request.form:
            
            nombre_buscar = request.form['nombre_buscar']
            
            buscado = True
            
            for i in range(len(lista_usuarios_global)):
                
                if lista_usuarios_global[i][0] == nombre_buscar:
                    resultado = lista_usuarios_global[i]
                    break
                    
        # Paso 2: Guardar los cambios usando la posición exacta
        elif 'nombre_antiguo' in request.form:
            n_not1 = request.form['nueva_nota1']
            n_not2 = request.form['nueva_nota2']
            n_not3 = request.form['nueva_nota3']
            
            # Buscamos la posición 'i' del registro viejo para moficarlo directamente
            for i in range(len(lista_usuarios_global)):
                if lista_usuarios_global[i][0] == nombre_buscar:
                    lista_usuarios_global[i] = (i[0], i[1], i[3], n_not1, n_not2, n_not3)
                    break
            return redirect(url_for('ver_usuarios'))
            
    return render_template("editar.html", resultado=resultado, buscado=buscado)

#ELIMINAR
# ==========================================
@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    resultado = None
    buscado = False
    eliminado = False
    
    if request.method == 'POST':
        
        if 'nombre_buscar' in request.form:
            nombre_buscar = request.form['nombre_buscar']
            buscado = True
            for i in range(len(lista_usuarios_global)):
                if lista_usuarios_global[i][0] == nombre_buscar:
                    resultado = lista_usuarios_global[i]
                    break
                    
        elif 'nombre_eliminar' in request.form:
            
            n_eliminar = request.form['nombre_eliminar']
            
            for i in range(len(lista_usuarios_global)):
                if lista_usuarios_global[i][0] == n_eliminar:
                    lista_usuarios_global.pop(i)
                    break
            eliminado = True
            
    return render_template("eliminar.html", resultado=resultado, buscado=buscado, eliminado=eliminado)

#VER REGISTRO
# ==========================================
@app.route("/usuarios")
def ver_usuarios():
    
    if not lista_usuarios_global:
        mensajes = ["No hay usuarios registrados todavía."]
        return render_template("usuarios.html", lista_usuarios=mensajes)
    
    return render_template("usuarios.html", lista_usuarios=lista_usuarios_global)

if __name__ == "__main__":
    app.run(debug=True, port=5017)
    