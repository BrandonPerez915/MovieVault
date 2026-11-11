"""
MovieVault - Menú Interactivo por Features (main.py).
Estructurado por dominios y funcionalidades de la plataforma.
"""

import sys
import os


def clear_screen() -> None:
    """Limpia la pantalla en terminales interactivas."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def print_banner(subtitle: str = "Plataforma de Exploración, Reseñas y Recomendaciones") -> None:
    print(r"""
========================================================================
   __  ___           _    _   __            _ _   
  /  |/  /___ _  __ (_)__ | | / /___ ___ __ | | |_ 
 / /|_/ // _ \ |/ // // -_)| |/ // _ `/ // /| |  _/
/_/  /_/ \___/___//_/ \__/ |___/ \_,_/ \_,_/|_|\__| 
""" + f"   {subtitle}\n" + "=" * 72)


# ==============================================================================
# SUBMENÚ: PELÍCULAS
# ==============================================================================

def submenu_movies() -> None:
    while True:
        clear_screen()
        print_banner("Módulo: Películas")
        print("CONSULTAS DE PELÍCULAS:")
        print("  1. Películas por título, década e idioma (ordenadas por impacto)")
        print("  2. Películas por género y país (y director)")
        print("  3. Películas por rating, director y década")
        print("  4. Películas por palabras clave en sinopsis")
        print("  5. Películas por actor y/o director")
        print("  0. <-- Volver al menú principal")
        print("=" * 72)

        choice = input("Selecciona una opción [0-5]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[Sección Activa] Has entrado a: Películas por título, década e idioma.")
            pass
        elif choice == "2":
            print("\n[Sección Activa] Has entrado a: Películas por género y país.")
            pass
        elif choice == "3":
            print("\n[Sección Activa] Has entrado a: Películas por rating, director y década.")
            pass
        elif choice == "4":
            print("\n[Sección Activa] Has entrado a: Películas por palabras clave en sinopsis.")
            pass
        elif choice == "5":
            print("\n[Sección Activa] Has entrado a: Películas por actor y/o director.")
            pass
        else:
            print("\n[!] Opción inválida.")

        input("\nPresiona [Enter] para continuar...")


# ==============================================================================
# SUBMENÚ: RESEÑAS
# ==============================================================================

def submenu_reviews() -> None:
    while True:
        clear_screen()
        print_banner("Módulo: Reseñas y Comunidad")
        print("CONSULTAS DE RESEÑAS:")
        print("  1. Reseñas por palabras clave en texto (ordenadas por likes y comentarios)")
        print("  0. <-- Volver al menú principal")
        print("=" * 72)

        choice = input("Selecciona una opción [0-1]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[Sección Activa] Has entrado a: Reseñas por palabras clave en texto.")
            pass
        else:
            print("\n[!] Opción inválida.")

        input("\nPresiona [Enter] para continuar...")


# ==============================================================================
# SUBMENÚ: ACTIVIDAD RECIENTE Y FEED
# ==============================================================================

def submenu_activity() -> None:
    while True:
        clear_screen()
        print_banner("Módulo: Actividad Reciente y Feed")
        print("FEED DE ACTIVIDAD Y RESEÑAS RECIENTES:")
        print("  1. Reseñas más recientes publicadas por la comunidad")
        print("  2. Reseñas recientes de amigos y usuarios que sigues")
        print("  3. Registro de interacciones y likes recientes")
        print("  0. <-- Volver al menú principal")
        print("=" * 72)

        choice = input("Selecciona una opción [0-5]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[Sección Activa] Has entrado a: Reseñas más recientes de la comunidad.")
            pass
        elif choice == "2":
            print("\n[Sección Activa] Has entrado a: Reseñas recientes de amigos y seguidos.")
            pass
        elif choice == "3":
            print("\n[Sección Activa] Has entrado a: Registro de interacciones y likes recientes.")
            pass
        else:
            print("\n[!] Opción inválida.")

        input("\nPresiona [Enter] para continuar...")


# ==============================================================================
# SUBMENÚ: TALENTO (ACTORES Y DIRECTORES)
# ==============================================================================

def submenu_talent() -> None:
    while True:
        clear_screen()
        print_banner("Módulo: Actores y Directores")
        print("CONSULTAS DE TALENTO:")
        print("  1. Agregación de impacto de actor (carrera, décadas, géneros y colaboradores)")
        print("  2. Consultar perfil de actor y filmografía")
        print("  3. Consultar perfil de director y películas dirigidas")
        print("  0. <-- Volver al menú principal")
        print("=" * 72)

        choice = input("Selecciona una opción [0-3]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[Sección Activa] Has entrado a: Agregación de impacto de actor.")
            pass
        elif choice == "2":
            print("\n[Sección Activa] Has entrado a: Perfil de actor y filmografía.")
            pass
        elif choice == "3":
            print("\n[Sección Activa] Has entrado a: Perfil de director y películas dirigidas.")
            pass
        else:
            print("\n[!] Opción inválida.")

        input("\nPresiona [Enter] para continuar...")


# ==============================================================================
# SUBMENÚ: USUARIOS Y ESTADÍSTICAS
# ==============================================================================

def submenu_users() -> None:
    while True:
        clear_screen()
        print_banner("Módulo: Usuarios y Estadísticas")
        print("ESTADÍSTICAS DE USUARIO:")
        print("  1. Agregación estadísticas de usuario (resumen histórico estilo Spotify Wrapped)")
        print("  0. <-- Volver al menú principal")
        print("=" * 72)

        choice = input("Selecciona una opción [0-1]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[Sección Activa] Has entrado a: Estadísticas de usuario (Spotify Wrapped).")
            pass
        else:
            print("\n[!] Opción inválida.")

        input("\nPresiona [Enter] para continuar...")


# ==============================================================================
# SUBMENÚ: MOTOR DE RECOMENDACIONES
# ==============================================================================

def submenu_recommendations() -> None:
    while True:
        clear_screen()
        print_banner("Módulo: Motor de Recomendaciones")
        print("RECOMENDACIONES:")
        print("  1. Recomendación de usuarios porque les gustó mi reseña")
        print("  2. Recomendación de películas que vieron recientemente amigos y le dieron rating")
        print("  3. Recomendación de películas del mismo género que no aparezcan en lista propia")
        print("  4. Recomendación de películas que le gustaron a un usuario que dio like a mi reseña")
        print("  5. Recomendación de películas que comparten actor con favorita del usuario")
        print("  6. Recomendación de posibles amigos con base en gustos compartidos (ratings >= 4)")
        print("  7. Recomendación de películas en lista propia vistas y likeadas por amigos")
        print("  8. Recomendación de películas por combinación de actor y director")
        print("  0. <-- Volver al menú principal")
        print("=" * 72)

        choice = input("Selecciona una opción [0-8]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[Sección Activa] Has entrado a: Recomendación de usuarios por likes en reseña.")
            pass
        elif choice == "2":
            print("\n[Sección Activa] Has entrado a: Películas vistas recientemente por amigos con rating.")
            pass
        elif choice == "3":
            print("\n[Sección Activa] Has entrado a: Películas del mismo género fuera de lista propia.")
            pass
        elif choice == "4":
            print("\n[Sección Activa] Has entrado a: Películas que gustaron a amigos con el mismo director.")
            pass
        elif choice == "5":
            print("\n[Sección Activa] Has entrado a: Películas que comparten actor con favorita.")
            pass
        elif choice == "6":
            print("\n[Sección Activa] Has entrado a: Posibles amigos con base en gustos compartidos.")
            pass
        elif choice == "7":
            print("\n[Sección Activa] Has entrado a: Películas en lista propia likeadas por amigos.")
            pass
        elif choice == "8":
            print("\n[Sección Activa] Has entrado a: Películas por combinación de actor y director.")
            pass
        else:
            print("\n[!] Opción inválida.")

        input("\nPresiona [Enter] para continuar...")


# ==============================================================================
# MENÚ PRINCIPAL
# ==============================================================================

def main() -> None:
    while True:
        clear_screen()
        print_banner()
        print("MENÚ PRINCIPAL (POR FEATURES):")
        print("  1. Películas                  -> Búsquedas, filtros por género, país, rating y elenco")
        print("  2. Reseñas                    -> Búsqueda de reseñas por palabras clave y popularidad")
        print("  3. Actividad Reciente y Feed  -> Reseñas recientes y actividad social")
        print("  4. Actores y Directores       -> Impacto de actores, filmografías y perfiles de directores")
        print("  5. Usuarios y Estadísticas    -> Resumen histórico anual y estadísticas estilo Wrapped")
        print("  6. Motor de Recomendaciones   -> Algoritmos de recomendación social y de contenido")
        print("  0. Salir")
        print("=" * 72)

        choice = input("Selecciona un módulo [0-6]: ").strip()

        if choice == "0":
            print("\n¡Gracias por usar MovieVault! Hasta pronto.\n")
            sys.exit(0)
        elif choice == "1":
            submenu_movies()
        elif choice == "2":
            submenu_reviews()
        elif choice == "3":
            submenu_activity()
        elif choice == "4":
            submenu_talent()
        elif choice == "5":
            submenu_users()
        elif choice == "6":
            submenu_recommendations()
        else:
            print("\n[!] Opción inválida. Elige entre 0 y 6.")
            input("Presiona [Enter] para reintentar...")


if __name__ == "__main__":
    main()
