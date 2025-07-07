# Desarrollo Backend prueba desarrollador fullstack 4thewords - Leider Solano Villamizar


## Instalación:

1. Si se desea creamos un entorno virtual para instalar las dependencias:

```bash
python3 -m venv venv
```

2. Posteriormente, para activar el entorno virtual(linux):

```bash
source venv/bin/activate

```
para el caso de Windows:

```bash
.\venv\Scripts\activate

```

3. Instalamos las dependencias:

```bash
pip install -r requirements.txt
```

4. Creamos la base de datos a partir del .sql que encontramos en la raiz del proyecto, en este se incluye la creación de la base de datos, la creación de las tablas y la creación de datos.

5. Creamos un archivo `.env`, donde incluiremos la url de la base de datos y las credenciales para la conexion a cloudinary:

```env
DATABASE_URL="mysql://root:tu_contraseña@localhost:3306/4thewords_prueba_leider_solano"
CLOUDINARY_CLOUD_NAME="dpqxu23gd"
CLOUDINARY_API_KEY="426369548666923"
CLOUDINARY_API_SECRET="gE3SPFBzTIARWR53ovDzACCfGRQ"
SECRET_KEY= "L31d3r1712@"
```

6. Iniciamos el servidor en el puerto 8080:

```bash
fastapi dev --port 8080
```

