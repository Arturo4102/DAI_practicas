Superuser: arturo4102
practicas,DAI


from django.contrib.auth.models import User

# Reemplaza 'nombre_de_usuario' con el nombre de usuario del usuario cuya contraseña deseas cambiar
user = User.objects.get(username='arturo4102')

# Cambia la contraseña a 'nueva_contraseña'
user.set_password('practicas,DAI')
user.save()


# Iniciar aplicación con npm para el móvil
npm run dev -- --host 0.0.0.0

