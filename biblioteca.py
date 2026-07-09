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


def elemento_soporte(nodo: tuple[float | int, float | int], ejes: Axes, tipo_soporte: int = 0,
                     ang: float = 0.0) -> VMobject:
    ang = np.deg2rad(ang)
    punto = ejes.c2p(*nodo)
    soporte = VGroup()
    achurado = VGroup()
    p_1 = punto + np.array([-0.3, -0.6, 0])
    p_2 = punto + np.array([0.3, -0.6, 0])
    if tipo_soporte == 0:  # pivotado móvil:
        pol = Polygon(punto, p_1, p_2, fill_color=GRAY_B, stroke_width=1, fill_opacity=0.95, color=WHITE)
        pol.rotate(ang, about_point=punto)
        for i in range(3):
            soporte.add(Circle(radius=0.1, color=WHITE, stroke_width=1).move_to(
                p_1 + np.array([i * 0.2 + 0.1, -0.1, 0.0])).rotate(ang, about_point=punto))
        soporte.add(pol)
    elif tipo_soporte == 1:  # pivotado fijo
        pol = Polygon(punto, p_1, p_2, fill_color=GRAY_B, stroke_width=1, fill_opacity=0.95, color=WHITE)
        pol.rotate(ang, about_point=punto)
        h = 0.2
        for p in np.linspace(p_1, p_2 + np.array([h, 0.0, 0.0]), 10):
            r = h
            q = 0.0
            delta_r = p[0] - p_1[0]
            delta_q = p[0] - p_2[0]
            r = delta_r if delta_r < r else r
            q = q if delta_q < 0 else delta_q
            linea = Line(p - q * np.array([1, 1, 0]), p - r * np.array([1, 1, 0]), color=WHITE, stroke_width=1)
            achurado.add(linea)
        achurado.rotate(ang, about_point=punto)
        soporte.add(pol, achurado)
    elif tipo_soporte == 2:  # empotrado por defecto empotrado izquierdo
        h = 0.3
        z = 0.5
        p_1 = punto + z * np.array([0, 1, 0])
        p_2 = punto - z * np.array([0, 1, 0])
        linea_base = Line(p_1, p_2, color=WHITE, stroke_width=4)
        linea_base.rotate(ang, about_point=punto)
        for p in np.linspace(p_1, p_2 + np.array([0.0, -h, 0.0]), 10):
            r = h
            q = 0.0
            delta_r = p_1[1] - p[1]
            delta_q = p_2[1] - p[1]
            r = delta_r if delta_r < r else r
            q = q if delta_q < 0 else delta_q
            linea = Line(p - q * np.array([1, -1, 0]), p - r * np.array([1, -1, 0]), color=WHITE, stroke_width=1)
            achurado.add(linea)
        achurado.rotate(ang, about_point=punto)
        soporte.add(linea_base, achurado)
    else: # empotrado con rodamientos por defecto empotrado izquierdo
        h = 0.3
        z = 0.5
        p_1 = punto + z * np.array([0, 1, 0])
        p_2 = punto - z * np.array([0, 1, 0])
        linea_base = Line(p_1, p_2, color=WHITE, stroke_width=4)
        linea_base.rotate(ang, about_point=punto)
        for p in np.linspace(p_1, p_2 + np.array([0.0, -h, 0.0]), 10):
            r = h
            q = 0.0
            delta_r = p_1[1] - p[1]
            delta_q = p_2[1] - p[1]
            r = delta_r if delta_r < r else r
            q = q if delta_q < 0 else delta_q
            linea = Line(p - q * np.array([1, -1, 0]), p - r * np.array([1, -1, 0]), color=WHITE, stroke_width=1)
            achurado.add(linea)
        achurado.rotate(ang, about_point=punto)
        n_rod=4
        for i in range(n_rod):
            soporte.add(Circle(radius=0.1, color=WHITE, stroke_width=1).move_to(
                p_1 + np.array([-(h+0.1), -(i * (2*z-0.2)/(n_rod-1) + 0.1), 0.0])).rotate(ang, about_point=punto))
        linea_base_2 = Line(p_1-np.array([h,0.0,0.0]), p_2-np.array([h,0.0,0.0]), color=WHITE, stroke_width=4)
        linea_base_2.rotate(ang, about_point=punto)
        soporte.add(linea_base, linea_base_2, achurado)
    return soporte


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
                               ejes: Axes, h: float | int = 0, longitud: float = 2.0, n_cargas: int = 10,
                               saliente=True) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0]) + np.pi / 2
    coord_i += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    coord_j += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    inicio_vec = np.linspace(coord_i, coord_j, n_cargas, axis=0)
    coord_f_i = coord_i + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    coord_f_j = coord_j + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    final_vec = np.linspace(coord_f_i, coord_f_j, n_cargas, axis=0)
    carga_distribuida = VGroup()
    for i in range(n_cargas):
        inicio = inicio_vec[i]
        final = final_vec[i]
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
                               ejes: Axes, h: float | int = 0, longitud_i: float = 2.0, longitud_f: float = 2.0,
                               n_cargas: int = 10, saliente=True) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0]) + np.pi / 2
    coord_i += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    coord_j += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    inicio_vec = np.linspace(coord_i, coord_j, n_cargas, axis=0)
    coord_f_i = coord_i + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud_i], [0.0], [0.0]])).flatten()
    coord_f_j = coord_j + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud_f], [0.0], [0.0]])).flatten()
    final_vec = np.linspace(coord_f_i, coord_f_j, n_cargas, axis=0)
    carga_trapezoidal = VGroup()
    for i in range(n_cargas):
        inicio = inicio_vec[i]
        final = final_vec[i]
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
            carga_d = elemento_carga_distribuida((0, 0), (5, 5), ejes, 0.5 / 2, 1, 20, saliente=False)
            carga_d2 = elemento_carga_trapezoidal((5, 5), (10, 2), ejes, 0.5 / 2, 0, 2.5, 20, saliente=False)
            carga_d2.set_color(BLUE)
            sop = elemento_soporte((1, 1), ejes, 0, 45)
            sop_2 = elemento_soporte((5, 2), ejes, 2, 0)
            sop_3 = elemento_soporte((6, 2), ejes, 3, 180)
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
            self.add(sop)
            self.add(sop_2)
            self.add(sop_3)
            self.wait(2)

    demo().render()


if __name__ == '__main__':
    main()
