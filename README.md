# AVICyT
Plataforma Web diseñada para Estudiantes y Docentes de la UDH para el manejo y control de las Tesis

# PREGUNTAS
- ¿Cuántas tesis puede estar asesorando un Docente a la vez?
- ¿El asesor debe trabajar con el estudiante antes de que este realice la Matriz de Consistencia?
- ¿Cómo manejar la eliminación del una tesis del sistema?
- ¿A qué se se refiere exactamente con clasificación?
- ¿Cómo debe ser la vista de los Docente de Tesis?

## FRAMEWORKS AND THINGYS
- FRONTEND: Angular o React
- BACKEND: Django
- IA: Python
- SERVIDOR: Hacer Pruebas en Amazon - Docker

## APIS
- Google: Para loggeo y para enviar notis por gmail
- UDH: Sistema de cuentas, maybe probably

## PERFILES
- Estudiante
- Asesor
- Admin/VRI
- Docente de Tesis

## COSAS DE LOGIN
- El sistema debe permitir loguearse (?) solo con un correo institucional de la UDH
- Permitir recuperar contraseña
- El sistema debe ser capaz de identificar una cuenta de estudiante y una de docente, ademas debe identificar la facultad del usuario que esta iniciando sesión

# Home
De momento es el Login creo

# Página Estudiante
## Formato de Matriz de Consistencia
Paso necesario para poder contactar con 1 o varios asesores, la plataforma debería apoyar al estudiante en cada paso
El asistente debe reaccionar positivamente al paso actual para poder pasar al siguiente
### Paso 1: Problema
La plataforma debe darle la lista de problemas de la DB al estudiante y guiarlo a presentar un problema poco afrontado.
### Paso 2: Título
El Asistente debe enfocarse en la estructura que debe tener el Título de la Investigación, dándole ejemplos de Tesis bien formuladas al Estudiante.
### Paso 3: Objetivos
Basándose en la información del problema propuesto y el título formulado, el Asistente debe analizar los objetivos que el Estudiante presente y encontrar una relación aceptable entre esta información. Debe dar ejemplos de Tesis bien formuladas.
El análisis es por cada Objetivo
### Paso 4: Variables
Basándose en la información hasta el momento, el Asistente debe analizar las variables que el Estudiante presente y encontrar una relación aceptable entre esta información. Debe dar ejemplos de Tesis bien formuladas.
El análisis es por cada Variable
### Paso 5: Clasificación
El Asistente debería dar un juicio inicial de qué metodologías puede usar, dando una lista de las existentes. Luego proponer una clasificación con los datos de los pasos anteriores.
El Estudiante define finalmente su clasificación.

## Subir a la plataforma
Luego de terminar su Matriz de Consistencia, el Estudiante puede dirigirse a la página de Asesores donde puede escoger contactar con 1 Asesor en específico o poner su Matriz en un listado para que los Asesores puedan revisar su Título y decidir asesorarlo o no.

## Lista de Asesores Disponibles
La vista muestra la Matriz subida actualmente y un listado de Asesores disponibles con la opción de contactarlos.

# Página de Asesor
El Asesor inicia viendo el listado de Tesis buscando Asesores y una bandeja de Solicitudes de Asesoría (mensajes directos de los Estudiantes).
El Asesor puede ver tanto las Matrices en busca de Asesoría como las Matrices de mensajes directos, lo que lo transfiere a:

## Página de Revisión
En esta se muestran los datos del estudiante y la Matriz Formulada.
El docente podrá Rechazar o Aceptar la Solicitud de un Estudiante que envió su Matriz via contacto directo.
El docente podrá Solicitar ser Asesor de cualquiera de las Tesis dentro del listado.
En ambas vistas, el Docente debe poder calificar la Matriz que revisa.

### Sistema de Calificaciones
Los Administradores de la VRI deben revisar las Calificaciones negativas y, en caso sea pertinente, aceptar la Calificación negativa. 
Si una Matriz tiene 3 calificaciones negativas aprobadas, esto se le notificará al Estudiante y se le pedirá que vuelva a realizar la Matriz.
Las Matrices de la Lista deberán ser ordenadas por calificaciones positivas

# Página VRI
Empezamos con una página con datos de la plataforma y con 2 listados:
## Calificaciones Negativas Enviadas
Se debe ver el listado de las calificaciones negativas enviadas por los Asesores, dando click pueden ver la página de "Anular o Validar" la calificación para completar el Sistema de Calificaciones

## Vista de Tesis y sus Observaciones (Pruebas) 
Pueden ver un report completo de los cambios realizados en cada observación de la Tesis

# Página Docente de Tesis
Ni idea, luego lo agragamos
