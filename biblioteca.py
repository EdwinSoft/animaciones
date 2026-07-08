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


def elemento_carga(nodo: tuple[float | int, float | int], ejes: Axes, longitud: float = 10.0,
                   ang: float = 0.0) -> VMobject:
    coord = ejes.c2p(*nodo)
    print(coord)
    final = np.array(coord)+  (np.array([[np.cos(ang), np.sin(ang), 0.0], [-np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    print(final)
    fuerza_arrow = Arrow(
        start=nodo,
        end=final,
        buff=0,  # ¡Fundamental para que toque los puntos exactamente!
        color=RED,
        stroke_width=4,  # Grosor de la línea
        max_tip_length_to_length_ratio=0.15  # Controla el tamaño de la punta
    )
    return fuerza_arrow


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
            fuerza = elemento_carga((10, 2), ejes)
            self.play(FadeIn(ejes), run_time=2)
            self.play(FadeIn(viga[1], viga[2]), run_time=2)
            self.play(FadeIn(viga[0]), run_time=2)
            self.play(FadeIn(armadura), run_time=2)
            # self.add(ejes)
            # self.add(armadura)
            # self.add(viga)
            self.add(marco)
            self.add(fuerza)
            self.wait(2)

    demo().render()


if __name__ == '__main__':
    main()
