from manim import *
import numpy as np


def elemento_viga(x_i: float, x_f: float, h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p((x_i, 0))
    coord_j = ejes.c2p((x_f, 0))
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    viga = Rectangle(height=h, width=L, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=1).move_to(centro)
    nodo_i = Dot(coord_i, color=RED)
    nodo_j = Dot(coord_j, color=RED)
    return VGroup(viga, nodo_i, nodo_j)


def elemento_armadura(nodo_i: tuple[float, float], nodo_j: tuple[float, float], h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0])

    nodo_i = Dot(coord_i, color=RED)
    nodo_j = Dot(coord_j, color=RED)
    armadura = RoundedRectangle(height=h, width=L + h, color=BLUE, fill_color=BLUE, fill_opacity=0.5,
                                corner_radius=h / 2, stroke_width=1)
    armadura.move_to(centro).rotate(angle=ang)
    return VGroup(armadura, nodo_i, nodo_j)


def elemento_marco(nodo_i: tuple[float, float], nodo_j: tuple[float, float], h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0])

    nodo_i = Dot(coord_i, color=BLUE_A)
    nodo_j = Dot(coord_j, color=BLUE_A)
    armadura = RoundedRectangle(height=h, width=L + h, color=BLUE, fill_color=BLUE, fill_opacity=1,
                                corner_radius=h / 2, stroke_width=0)
    armadura.move_to(centro).rotate(angle=ang)
    return VGroup(armadura, nodo_i, nodo_j)


def elemento_carga(nodo: tuple[float | int, float | int], ejes: Axes, longitud: float = 2.0,
                   ang: float = 0.0, saliente: bool = True) -> VMobject:
    ang = np.deg2rad(ang)
    inicio = ejes.c2p(*nodo)
    final = np.array(inicio) + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    if not saliente:
        inicio, final = final, inicio
    fuerza_arrow = Arrow(
        start=inicio,
        end=final,
        buff=0,  # ¡Fundamental para que toque los puntos exactamente!
        color=RED,
        stroke_width=4,  # Grosor de la línea
        tip_shape=StealthTip,  # Aquí cambias la forma
        max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
    )
    return fuerza_arrow


def elemento_carga_distribuida(nodo_i: tuple[float | int, float | int], nodo_j: tuple[float | int, float | int],
                               ejes: Axes, h: float | int = 0, longitud: float = 2.0, n_cargas: int = 10, saliente=True) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0]) + np.pi/2
    coord_i += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    coord_j += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    inicio_vec = np.linspace(coord_i,coord_j,n_cargas, axis=0)
    coord_f_i = coord_i + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    coord_f_j = coord_j + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    final_vec= np.linspace(coord_f_i, coord_f_j, n_cargas, axis=0)
    carga_distribuida = VGroup()
    for i in range(n_cargas):
        inicio=inicio_vec[i]
        final=final_vec[i]
        if not saliente:
            inicio, final = final, inicio
        fuerza_arrow = Arrow(
            start=inicio,
            end=final,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=RED,
            stroke_width=4,  # Grosor de la línea
            tip_shape=StealthTip,  # Aquí cambias la forma
            max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
        )
        carga_distribuida.add(fuerza_arrow)
    return carga_distribuida

def elemento_carga_trapezoidal(nodo_i: tuple[float | int, float | int], nodo_j: tuple[float | int, float | int],
                               ejes: Axes, h: float | int = 0, longitud_i: float = 2.0, longitud_f: float = 2.0, n_cargas: int = 10, saliente=True) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0]) + np.pi/2
    coord_i += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    coord_j += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    inicio_vec = np.linspace(coord_i,coord_j,n_cargas, axis=0)
    coord_f_i = coord_i + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud_i], [0.0], [0.0]])).flatten()
    coord_f_j = coord_j + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud_f], [0.0], [0.0]])).flatten()
    final_vec= np.linspace(coord_f_i, coord_f_j, n_cargas, axis=0)
    carga_trapezoidal = VGroup()
    for i in range(n_cargas):
        inicio=inicio_vec[i]
        final=final_vec[i]
        longitud = np.linalg.norm(final - inicio)
        if not saliente:
            inicio, final = final, inicio
        if longitud > 0.05:
            fuerza_arrow = Arrow(
                start=inicio,
                end=final,
                buff=0,  # ¡Fundamental para que toque los puntos exactamente!
                color=RED,
                stroke_width=4,  # Grosor de la línea
                tip_shape=StealthTip,  # Aquí cambias la forma
                max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
            )
            carga_trapezoidal.add(fuerza_arrow)
    return carga_trapezoidal

def elemento_momento(nodo: tuple[float | int, float | int], ejes: Axes, radio: float = 0.5,
                     ang: float = 0.0, positivo: bool = True) -> VMobject:
    ang_i = np.deg2rad(90)
    ang_f = np.deg2rad(325)
    ang = np.deg2rad(ang)
    alfa = (ang_i + ang_f) / 2
    centro = ejes.c2p(*nodo)
    inicio = np.array(centro) + (np.array(
        [[np.cos(ang_i), -np.sin(ang_i), 0.0], [np.sin(ang_i), np.cos(ang_i), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[radio], [0.0], [0.0]])).flatten()
    final = np.array(centro) + (np.array(
        [[np.cos(ang_f), -np.sin(ang_f), 0.0], [np.sin(ang_f), np.cos(ang_f), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[radio], [0.0], [0.0]])).flatten()
    if positivo:
        inicio, final = final, inicio
    momento = CurvedArrow(
        start_point=inicio,
        end_point=final,
        angle=ang_f - ang_i,  # Ángulo de la curvatura de la flecha
        stroke_width=4,  # Grosor de la línea
        tip_length=0.25,  # Controla el tamaño absoluto de la punta
        tip_shape=StealthTip,  # Aquí cambias la forma
        color=GREEN
    ).move_arc_center_to(centro).rotate(ang, about_point=centro)
    return momento


class CargasDistribuidas(Scene):
    def construct(self):
        # ==========================================
        # 1. FUNCIÓN PARA CARGA RECTANGULAR
        # ==========================================
        def crear_carga_rectangular(longitud, magnitud, num_flechas=8, color=RED):
            grupo_carga = VGroup()

            # np.linspace crea 'num_flechas' puntos separados equitativamente desde 0 hasta 'longitud'
            posiciones_x = np.linspace(0, longitud, num_flechas)

            for x in posiciones_x:
                # La flecha apunta hacia abajo (hacia el eje X local)
                inicio = RIGHT * x + UP * magnitud
                fin = RIGHT * x

                flecha = Arrow(
                    start=inicio,
                    end=fin,
                    buff=0,
                    color=color,
                    tip_shape=ArrowTriangleFilledTip,
                    max_tip_length_to_length_ratio=0.2 / magnitud
                )
                grupo_carga.add(flecha)

            # Agregamos la línea superior horizontal que une todas las colas
            linea_superior = Line(
                start=UP * magnitud,
                end=RIGHT * longitud + UP * magnitud,
                color=color
            )
            grupo_carga.add(linea_superior)

            return grupo_carga

        # ==========================================
        # 2. FUNCIÓN PARA CARGA TRIANGULAR
        # ==========================================
        def crear_carga_triangular(longitud, magnitud_max, num_flechas=8, color=BLUE):
            grupo_carga = VGroup()
            posiciones_x = np.linspace(0, longitud, num_flechas)

            for x in posiciones_x:
                # Calculamos la altura de la flecha usando semejanza de triángulos (ecuación de la recta)
                altura_local = magnitud_max * (x / longitud)

                # TRUCO: Evitar el error de Manim al dibujar una flecha de longitud cero
                if altura_local > 0.05:
                    inicio = RIGHT * x + UP * altura_local
                    fin = RIGHT * x

                    flecha = Arrow(
                        start=inicio,
                        end=fin,
                        buff=0,
                        color=color,
                        tip_shape=ArrowTriangleFilledTip,
                        max_tip_length_to_length_ratio=0.2 / altura_local
                    )
                    grupo_carga.add(flecha)

            # Agregamos la línea superior diagonal (hipotenusa)
            linea_superior = Line(
                start=ORIGIN,
                end=RIGHT * longitud + UP * magnitud_max,
                color=color
            )
            grupo_carga.add(linea_superior)

            return grupo_carga

        # ==========================================
        # 3. CREACIÓN Y ALINEACIÓN EN LA ESCENA
        # ==========================================

        # Instanciamos nuestras cargas
        carga_rect = crear_carga_rectangular(longitud=4, magnitud=1.5)
        carga_tri = crear_carga_triangular(longitud=4, magnitud_max=2)

        # Una vez están en su VGroup, podemos alinearlas o moverlas donde queramos
        # Por ejemplo, las separamos para que se vean bien en pantalla
        carga_rect.shift(LEFT * 5 + DOWN * 1)
        carga_tri.shift(RIGHT * 1 + DOWN * 1)

        # Dibujar vigas simuladas (solo visuales) para que tengan donde apoyarse
        viga1 = Line(carga_rect.get_corner(DL), carga_rect.get_corner(DR), stroke_width=6)
        viga2 = Line(carga_tri.get_corner(DL), carga_tri.get_corner(DR), stroke_width=6)

        # Animamos
        self.play(Create(viga1), Create(viga2))
        self.play(Create(carga_rect), Create(carga_tri))
        self.wait(2)


def main():
    class demo(Scene):
        def construct(self):
            ejes_coordenados = Axes(
                x_range=[0, 16, 1],
                y_range=[0, 9, 1],
                x_length=16,
                y_length=9,
                axis_config={"include_tip": False, "stroke_width": 2}
            ).scale(0.8)
            ejes_planos = NumberPlane(
                x_range=[0, 10, 1],
                y_range=[0, 8, 1],
                background_line_style={
                    "stroke_opacity": 0.1  # Puedes atenuar las líneas de la cuadrícula si no las quieres ver
                }
            )
            ejes_planos.to_edge(DOWN + LEFT)
            ejes = ejes_planos
            viga = elemento_viga(5, 10, 0.5, ejes)
            armadura = elemento_armadura((0, 0), (5, 5), 0.5, ejes)
            marco = elemento_marco((5, 5), (10, 2), 0.5, ejes)
            fuerza = elemento_carga((10, 2), ejes, ang=30, saliente=False, longitud=4)
            momento = elemento_momento((5, 5), ejes, ang=90, positivo=False)
            carga_d = elemento_carga_distribuida((0,0), (5,5), ejes, 0.5/2, 1, 20, saliente=False)
            carga_d2 = elemento_carga_trapezoidal((5, 5), (10, 2), ejes, 0.5 / 2, 0, 2.5, 20, saliente=False)
            carga_d2.set_color(BLUE)
            self.play(FadeIn(ejes), run_time=2)
            self.play(FadeIn(viga[1], viga[2]), run_time=2)
            self.play(FadeIn(viga[0]), run_time=2)
            self.play(FadeIn(armadura), run_time=2)
            self.play(FadeIn(carga_d2), run_time=2)
            # self.add(ejes)
            # self.add(armadura)
            # self.add(viga)
            self.add(marco)
            self.add(fuerza)
            self.add(momento)
            self.add(carga_d)
            self.wait(2)

    demo().render()


if __name__ == '__main__':
    main()
