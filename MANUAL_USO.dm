3.3 Manual de Uso y Pruebas
-Paso 1: Primero ingresamos al link de GitHub el cual contiene todos los programas e indicaciones para acceder a esta práctica de seguridad informática
Figura 26
Repositorio creado en GitHub

Nota.  En la figura se evidencia el repositorio que aparece al entrar en el link de GitHub
-Paso 2: Descargar el repositorio o crear una copia en la versión de Visual Studio que se tenga a la mano. De esta forma se tendrán todos los programas al alcance de la mano, trabajando de forma colaborativa.
Figura 27
Copia del Repositorio creado en GitHub

Nota.  En la figura se evidencia la copia el repositorio que aparece al entrar en el link de GitHub

3.3.1 Comandos de Instalación
Tabla 1
Comandos de instalación
Comando
Función
python --version
Verificar la instalación de python
python -m venv venv
Crear un entorno virtual
venv\Scripts\activate
Activar el entorno virtual
pip install flask
Instalar el Framework Flask

Nota. En la tabla se evidencian los comandos de instalación utilizados en la práctica. Fuente: Adaptado de
3.3.1.1 Uso del comando python --version
-Paso 1: Se abre el terminal de python y se pone al final python --version  con el fin de verificar la instalación.
Figura 28
Verificar instalación de la versión correcta de python
Nota. En la figura se muestra la verificación de la instalación correcta de python.
-Paso 2: Si sale el comando exitoso es porque se ha ejecutado la petición con éxito.
Figura 29
Comando funcionado con éxito


Nota. En la figura se muestra el comando funcionando de forma correcta.
3.3.1.2 Uso del comando python -m venv venv
-Paso 1: Se abre el terminal de python y se pone al final  python -m venv venv para crear un entorno virtual.
Figura 30
Comando  -m venv venv funcionado con éxito
Nota. En la figura se muestra el comando  -m venv venvfuncionando de forma correcta.
3.3.1.3 Uso del comando venv\Scripts\activate
-Paso 1: Se abre el terminal de python y se pone al final  python venv\Scripts\activate para activar el entorno virtual.
Figura 31
Comando  venv\Scripts\activate  funcionado con éxito
Nota. En la figura se muestra el comando  venv\Scripts\activate funcionando de forma correcta.
3.3.1.3 Uso del comando pip install flask
-Paso 1: Se abre el terminal de python y se pone al final pip install flask para instalar el Framework Flask
Figura 32
Comando  pip install flask funcionado con éxito







Nota. En la figura se muestra el comando  pip install flask funcionando de forma correcta.
3.3.2 Ejecución del servidor local
-Paso 1: Se hace clic derecho sobre el archivo app.py en el explorador del proyecto de PyCharm y se selecciona la opción Run ‘app’ para iniciar el servidor.
Figura 33
Ejecución del servidor local










Nota. En la figura se evidencia la ejecución del servidor local
     -Paso 2:La consola de PyCharm muestra la dirección donde quedó alojada la aplicación (http://127.0.0.1:5000). También informa que Flask corre en modo desarrollo y que el depurador está activo.





Figura 34
Respuesta correcta del servidor local

Nota. En la figura se evidencia la respuesta correcta del servidor local
-Paso 3: Al abrir esa dirección en el navegador aparece la aplicación del laboratorio “Cyber Lab”, con su pantalla de inicio de sesión.
Figura 35
Aplicación el el navegador

Nota. En la Figura se evidencia la aplicación en el navegador
3.3.3 Pruebas de ataque antes de la mitigación
3.3.3.1 Servidor web vulnerable con Flask y SQLite
-Paso 1: Con el servidor en ejecución, se ingresan un usuario y una contraseña en los campos del formulario de inicio de sesión.
Figura 36
Entrada de datos
Nota. En la figura se evidencia la entrada de los datos
-Paso 2: Si el sistema muestra el mensaje “Acceso concedido: admin”, significa que la aplicación procesó la solicitud. Sin embargo, esto también evidencia que el acceso se logra con una consulta vulnerable, por lo que es necesario aplicar cambios de seguridad.
Figura 37
Respuesta insegura del servidor




Nota. En la Figura se evidencia la respuesta insegura del servidor.
3.3.4 Validación del parche de seguridad con capturas de pantalla.
-Paso 1: Se detecta el problema de seguridad en el código. La consulta SQL se arma concatenando directamente los valores de usuario y password dentro del texto, lo que permite que un atacante manipule la consulta e ingrese sin autorización.





Figura 38
Validación del parche de seguridad

Nota. En la figura se evidencia la correcta ejecución de fallas para la aplicación del parche de seguridad.
-Paso 2: Se implementa el almacenamiento seguro de contraseñas mediante hash. Se eliminan las credenciales predeterminadas y se evita guardar contraseñas en texto plano. La tabla usuarios se crea con los campos id, usuario (único) y password, y la consulta del usuario admin pasa a usar un parámetro.
Figura 39
Implementación del parche de seguridad.

Nota. En la figura se evidencia la correcta implementación del parche de seguridad.
3.3.5 Rechazo del intento de sql injection
-Paso 1: Se vuelve a ingresar una cadena de inyección SQL en el campo de usuario del formulario.






Figura 40
Rechazo de intento de sql Injection.

Nota. En la Figura se evidencia el correcto rechazo de sql Injection
3.3.1 Consultas parametrizadas
-Paso 1: Se reemplaza la concatenación de texto por una consulta con marcadores de posición, por ejemplo "WHERE nombre LIKE ".
Paso 2: Los valores ingresados por el usuario se envían por separado como parámetros. Así la base de datos los interpreta únicamente como datos y nunca como código SQL.
Figura  41
Ingreso de consultas parametrizadas

Nota. En la Figura se evidencia el ingreso de consultas parametrizadas.





Figura 42
Resultado  de consultas parametrizadas

Nota. En la captura se observa el código modificado. La consulta ahora usa el marcador y los valores se pasan como parámetros en una tupla.
3.3.6 Respuesta del servidor
Figura 43
Respuesta del servidor

Nota. En la Figura se evidencia la respuesta del servidor después de la aplicación de consultas parametrizadas.
