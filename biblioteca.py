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
        max_tip_length_to_length_ratio=0.15  # Controla el tamaño de la punta
    )
    return fuerza_arrow


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
        tip_length=0.15,  # Controla el tamaño absoluto de la punta
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
                    max_tip_length_to_length_ratio=0.2
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
                        max_tip_length_to_length_ratio=0.2
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
            fuerza = elemento_carga((10, 2), ejes, ang=30, saliente=False)
            momento = elemento_momento((5, 5), ejes, ang=0, positivo=False)
            self.play(FadeIn(ejes), run_time=2)
            self.play(FadeIn(viga[1], viga[2]), run_time=2)
            self.play(FadeIn(viga[0]), run_time=2)
            self.play(FadeIn(armadura), run_time=2)
            # self.add(ejes)
            # self.add(armadura)
            # self.add(viga)
            self.add(marco)
            self.add(fuerza)
            self.add(momento)
            self.wait(2)

    demo().render()


if __name__ == '__main__':
    main()
