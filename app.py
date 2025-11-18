from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import db
import pyodbc

app = Flask(__name__)

# ============ RUTAS PRINCIPALES ============

@app.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('index.html')

# ============ PROVEEDORES ============

@app.route('/proveedores')
def proveedores():
    """Lista todos los proveedores"""
    query = "SELECT id_proveedor, nombre_proveedor FROM dbo.proveedores ORDER BY nombre_proveedor"
    resultados = db.ejecutar_query(query)
    
    proveedores_list = []
    if resultados:
        for row in resultados:
            proveedores_list.append({
                'id': row[0],
                'nombre': row[1]
            })
    
    return render_template('proveedores.html', proveedores=proveedores_list)

@app.route('/api/proveedores/crear', methods=['POST'])
def crear_proveedor():
    """Crea un nuevo proveedor"""
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        
        if not nombre:
            return jsonify({'error': 'El nombre es requerido'}), 400
        
        # NO insertamos el ID, SQL Server lo genera automáticamente
        comando = "INSERT INTO dbo.proveedores (nombre_proveedor) VALUES (?)"
        if db.ejecutar_comando(comando, (nombre,)):
            return jsonify({'success': True}), 201
        else:
            return jsonify({'error': 'Error al crear proveedor'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proveedores/<int:id>/actualizar', methods=['PUT'])
def actualizar_proveedor(id):
    """Actualiza un proveedor existente"""
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        
        if not nombre:
            return jsonify({'error': 'El nombre es requerido'}), 400
        
        comando = f"UPDATE dbo.proveedores SET nombre_proveedor = ? WHERE id_proveedor = {id}"
        if db.ejecutar_comando(comando, (nombre,)):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Error al actualizar proveedor'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proveedores/<int:id>/eliminar', methods=['DELETE'])
def eliminar_proveedor(id):
    """Elimina un proveedor (solo si no tiene artículos)"""
    try:
        # Verificar si tiene artículos
        query_check = f"SELECT COUNT(*) FROM dbo.articulos WHERE id_proveedor = {id}"
        resultado = db.ejecutar_query(query_check)
        
        if resultado and resultado[0][0] > 0:
            return jsonify({'error': 'No se puede eliminar: el proveedor tiene artículos asociados'}), 400
        
        comando = f"DELETE FROM dbo.proveedores WHERE id_proveedor = {id}"
        if db.ejecutar_comando(comando):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Error al eliminar proveedor'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proveedores/listar')
def listar_proveedores():
    """Lista todos los proveedores en JSON"""
    try:
        query = "SELECT id_proveedor, nombre_proveedor FROM dbo.proveedores ORDER BY nombre_proveedor"
        resultados = db.ejecutar_query(query)
        
        proveedores_list = []
        if resultados:
            for row in resultados:
                proveedores_list.append({
                    'id': row[0],
                    'nombre': row[1]
                })
        
        return jsonify({'proveedores': proveedores_list}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ ARTÍCULOS ============

@app.route('/articulos')
def articulos():
    """Lista todos los artículos"""
    query = """
    SELECT 
        a.id_articulo, 
        a.producto, 
        a.sku,
        a.marca,
        a.categoria,
        p.nombre_proveedor,
        a.costo_c_iva,
        a.tipo_moneda,
        a.iva
    FROM dbo.articulos a
    INNER JOIN dbo.proveedores p ON a.id_proveedor = p.id_proveedor
    ORDER BY a.producto
    """
    resultados = db.ejecutar_query(query)
    
    articulos_list = []
    if resultados:
        for row in resultados:
            articulos_list.append({
                'id': row[0],
                'producto': row[1],
                'sku': row[2],
                'marca': row[3],
                'categoria': row[4],
                'proveedor': row[5],
                'costo': row[6],
                'moneda': row[7],
                'iva': row[8]
            })
    
    # Traer lista de proveedores para el dropdown
    query_prov = "SELECT id_proveedor, nombre_proveedor FROM dbo.proveedores ORDER BY nombre_proveedor"
    proveedores_result = db.ejecutar_query(query_prov)
    proveedores_list = [(row[0], row[1]) for row in proveedores_result] if proveedores_result else []
    
    return render_template('articulos.html', articulos=articulos_list, proveedores=proveedores_list)

@app.route('/api/articulos/crear', methods=['POST'])
def crear_articulo():
    """Crea un nuevo artículo"""
    try:
        data = request.get_json()
        
        comando = """
        INSERT INTO dbo.articulos 
        (id_proveedor, marca, categoria, producto, sku, iva, costo_c_iva, tipo_moneda, fecha_ultima_modificacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
        """
        
        params = (
            int(data.get('id_proveedor')),
            data.get('marca', ''),
            data.get('categoria', ''),
            data.get('producto'),
            data.get('sku'),
            int(data.get('iva')),
            float(data.get('costo_c_iva')),
            data.get('tipo_moneda')
        )
        
        if db.ejecutar_comando(comando, params):
            return jsonify({'success': True}), 201
        else:
            return jsonify({'error': 'Error al crear artículo'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ DESCUENTOS ============

@app.route('/descuentos')
def descuentos():
    """Lista descuentos por proveedor"""
    query = """
    SELECT 
        dp.id_proveedor,
        p.nombre_proveedor,
        dp.descuento_1,
        dp.descuento_2,
        dp.pago_contado,
        dp.dto_financiero,
        dp.fecha_modificacion
    FROM dbo.descuentos_proveedor dp
    INNER JOIN dbo.proveedores p ON dp.id_proveedor = p.id_proveedor
    ORDER BY p.nombre_proveedor
    """
    resultados = db.ejecutar_query(query)
    
    descuentos_list = []
    if resultados:
        for row in resultados:
            descuentos_list.append({
                'id_proveedor': row[0],
                'proveedor': row[1],
                'descuento_1': row[2],
                'descuento_2': row[3],
                'pago_contado': row[4],
                'dto_financiero': row[5],
                'fecha': row[6]
            })
    
    # Traer lista de proveedores
    query_prov = "SELECT id_proveedor, nombre_proveedor FROM dbo.proveedores ORDER BY nombre_proveedor"
    proveedores_result = db.ejecutar_query(query_prov)
    proveedores_list = [(row[0], row[1]) for row in proveedores_result] if proveedores_result else []
    
    return render_template('descuentos.html', descuentos=descuentos_list, proveedores=proveedores_list)

@app.route('/api/descuentos/actualizar/<int:id_proveedor>', methods=['PUT'])
def actualizar_descuentos(id_proveedor):
    """Actualiza los descuentos de un proveedor"""
    try:
        data = request.get_json()
        
        # Verificar si existe
        query_check = f"SELECT COUNT(*) FROM dbo.descuentos_proveedor WHERE id_proveedor = {id_proveedor}"
        resultado = db.ejecutar_query(query_check)
        existe = resultado[0][0] > 0 if resultado else False
        
        if existe:
            # UPDATE
            comando = """
            UPDATE dbo.descuentos_proveedor
            SET descuento_1 = ?, descuento_2 = ?, pago_contado = ?, dto_financiero = ?, fecha_modificacion = GETDATE()
            WHERE id_proveedor = ?
            """
            params = (
                float(data.get('descuento_1')),
                float(data.get('descuento_2')),
                float(data.get('pago_contado')),
                float(data.get('dto_financiero')),
                id_proveedor
            )
        else:
            # INSERT
            comando = """
            INSERT INTO dbo.descuentos_proveedor
            (id_proveedor, descuento_1, descuento_2, pago_contado, dto_financiero, fecha_modificacion)
            VALUES (?, ?, ?, ?, ?, GETDATE())
            """
            params = (
                id_proveedor,
                float(data.get('descuento_1')),
                float(data.get('descuento_2')),
                float(data.get('pago_contado')),
                float(data.get('dto_financiero'))
            )
        
        if db.ejecutar_comando(comando, params):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Error al actualizar descuentos'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ DÓLAR ============

@app.route('/dolar')
def dolar():
    """Lista cotización de dólar por proveedor y oficial"""
    # Dólar por proveedor
    query_prov = """
    SELECT 
        dp.id_proveedor,
        p.nombre_proveedor,
        dp.dolar_proveedor,
        dp.fecha,
        dp.ultima_actualizacion
    FROM dbo.dolar_proveedor dp
    INNER JOIN dbo.proveedores p ON dp.id_proveedor = p.id_proveedor
    ORDER BY p.nombre_proveedor, dp.fecha DESC
    """
    resultados_prov = db.ejecutar_query(query_prov)
    
    dolar_prov_list = []
    if resultados_prov:
        for row in resultados_prov:
            dolar_prov_list.append({
                'id_proveedor': row[0],
                'proveedor': row[1],
                'valor': row[2],
                'fecha': row[3],
                'ultima_actualizacion': row[4]
            })
    
    # Dólar oficial (de tu tabla existente)
    query_oficial = """
    SELECT 
        tipo_cambio,
        fecha
    FROM dbo.hist_Dolar_Oficial
    ORDER BY fecha DESC
    """
    resultados_oficial = db.ejecutar_query(query_oficial)
    
    dolar_oficial_list = []
    if resultados_oficial:
        for row in resultados_oficial:
            dolar_oficial_list.append({
                'valor': row[0],
                'fecha': row[1]
            })
    
    # Traer lista de proveedores
    query_proveedores = "SELECT id_proveedor, nombre_proveedor FROM dbo.proveedores ORDER BY nombre_proveedor"
    proveedores_result = db.ejecutar_query(query_proveedores)
    proveedores_list = [(row[0], row[1]) for row in proveedores_result] if proveedores_result else []
    
    return render_template('dolar.html', 
                         dolar_prov=dolar_prov_list, 
                         dolar_oficial=dolar_oficial_list,
                         proveedores=proveedores_list)

@app.route('/api/dolar/cargar/<int:id_proveedor>', methods=['POST'])
def cargar_dolar(id_proveedor):
    """Carga/actualiza el dólar de un proveedor"""
    try:
        data = request.get_json()
        valor = float(data.get('valor'))
        
        if valor <= 0:
            return jsonify({'error': 'El valor debe ser positivo'}), 400
        
        # Eliminar registros antiguos y cargar nuevo
        comando_delete = f"DELETE FROM dbo.dolar_proveedor WHERE id_proveedor = {id_proveedor}"
        db.ejecutar_comando(comando_delete)
        
        comando_insert = """
        INSERT INTO dbo.dolar_proveedor
        (id_proveedor, dolar_proveedor, fecha, ultima_actualizacion)
        VALUES (?, ?, GETDATE(), GETDATE())
        """
        
        if db.ejecutar_comando(comando_insert, (id_proveedor, valor)):
            return jsonify({'success': True}), 201
        else:
            return jsonify({'error': 'Error al cargar dólar'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dolar/oficial/cargar', methods=['POST'])
def cargar_dolar_oficial():
    """Carga/actualiza el dólar oficial para una fecha específica en tu tabla existente"""
    try:
        data = request.get_json()
        valor = float(data.get('valor'))
        fecha = data.get('fecha')
        
        if valor <= 0:
            return jsonify({'error': 'El valor debe ser positivo'}), 400
        
        if not fecha:
            return jsonify({'error': 'La fecha es requerida'}), 400
        
        # Verificar si ya existe para esa fecha
        query_check = f"SELECT COUNT(*) FROM dbo.hist_Dolar_Oficial WHERE fecha = '{fecha}'"
        resultado = db.ejecutar_query(query_check)
        existe = resultado[0][0] > 0 if resultado else False
        
        if existe:
            # UPDATE
            comando = """
            UPDATE dbo.hist_Dolar_Oficial
            SET tipo_cambio = ?
            WHERE fecha = ?
            """
            params = (valor, fecha)
        else:
            # INSERT
            comando = """
            INSERT INTO dbo.hist_Dolar_Oficial
            (tipo_cambio, fecha)
            VALUES (?, ?)
            """
            params = (valor, fecha)
        
        if db.ejecutar_comando(comando, params):
            return jsonify({'success': True}), 201
        else:
            return jsonify({'error': 'Error al cargar dólar oficial'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dolar/oficial/<fecha>/eliminar', methods=['DELETE'])
def eliminar_dolar_oficial(fecha):
    """Elimina un registro de dólar oficial de tu tabla"""
    try:
        comando = f"DELETE FROM dbo.hist_Dolar_Oficial WHERE fecha = '{fecha}'"
        
        if db.ejecutar_comando(comando):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Error al eliminar'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ ERROR HANDLING ============

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ============ MAIN ============

if __name__ == '__main__':
    print("🚀 Iniciando aplicación...")
    print("Accede a: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)