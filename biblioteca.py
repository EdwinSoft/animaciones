from manim import *
import numpy as np

# config.tex_template = TexTemplate()
# config.tex_template.add_to_preamble(r"\usepackage{cancel}")
# config.tex_template.add_to_preamble(r"\usepackage{xcolor}")

def elemento_viga(x_i: float, x_f: float, h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p((x_i, 0))
    coord_j = ejes.c2p((x_f, 0))
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    viga = Rectangle(height=h, width=L, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=1).move_to(centro)
    # nodo_i = Dot(coord_i, color=RED)
    # nodo_j = Dot(coord_j, color=RED)
    # return VGroup(viga, nodo_i, nodo_j)
    return viga


def elemento_armadura(nodo_i: tuple[float, float], nodo_j: tuple[float, float], h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0])

    # nodo_i = Dot(coord_i, color=RED)
    # nodo_j = Dot(coord_j, color=RED)
    armadura = RoundedRectangle(height=h, width=L + h, color=BLUE, fill_color=BLUE, fill_opacity=0.5,
                                corner_radius=h / 2, stroke_width=1)
    armadura.move_to(centro).rotate(angle=ang)
    # return VGroup(armadura, nodo_i, nodo_j)
    return armadura


def elemento_marco(nodo_i: tuple[float, float], nodo_j: tuple[float, float], h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0])

    # nodo_i = Dot(coord_i, color=BLUE_A)
    # nodo_j = Dot(coord_j, color=BLUE_A)
    armadura = RoundedRectangle(height=h, width=L + h, color=BLUE, fill_color=BLUE, fill_opacity=1,
                                corner_radius=h / 2, stroke_width=0)
    armadura.move_to(centro).rotate(angle=ang)
    # return VGroup(armadura, nodo_i, nodo_j)
    return armadura


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
        soporte.add(Circle(radius=0.05, color=WHITE, stroke_width=1).set_fill(BLACK, opacity=1).move_to(punto))
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
        soporte.add(Circle(radius=0.05, color=WHITE, stroke_width=1).set_fill(BLACK, opacity=1).move_to(punto))
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
    else:  # empotrado con rodamientos por defecto empotrado izquierdo
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
        n_rod = 4
        for i in range(n_rod):
            soporte.add(Circle(radius=0.1, color=WHITE, stroke_width=1).move_to(
                p_1 + np.array([-(h + 0.1), -(i * (2 * z - 0.2) / (n_rod - 1) + 0.1), 0.0])).rotate(ang,
                                                                                                    about_point=punto))
        linea_base_2 = Line(p_1 - np.array([h, 0.0, 0.0]), p_2 - np.array([h, 0.0, 0.0]), color=WHITE, stroke_width=4)
        linea_base_2.rotate(ang, about_point=punto)
        soporte.add(linea_base, linea_base_2, achurado)
    return soporte


def elemento_carga(nodo: tuple[float | int, float | int], ejes: Axes, longitud: float = 2.0, h: float | int = 0,
                   ang: float = 0.0, saliente: bool = True) -> VMobject:
    ang = np.deg2rad(ang)
    inicio = ejes.c2p(*nodo) + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    final = np.array(inicio) + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    if not saliente:
        inicio, final = final, inicio
    fuerza_arrow = Arrow(
        start=inicio,
        end=final,
        buff=0,  # ¡Fundamental para que toque los puntos exactamente!
        color=BLUE,
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
            color=BLUE_D,
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
                color=BLUE_D,
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
    centro = ejes.c2p(*nodo)
    inicio = np.array(centro) + (np.array(
        [[np.cos(ang_i), -np.sin(ang_i), 0.0], [np.sin(ang_i), np.cos(ang_i), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[radio], [0.0], [0.0]])).flatten()
    final = np.array(centro) + (np.array(
        [[np.cos(ang_f), -np.sin(ang_f), 0.0], [np.sin(ang_f), np.cos(ang_f), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[radio], [0.0], [0.0]])).flatten()
    if positivo:
        inicio, final = final, inicio
        ang_i, ang_f = ang_f, ang_i
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


def elemento_grado_libertad(nodo: tuple[float | int, float | int], ejes: Axes, longitud: float = 0.5,
                            offset: float = 0.0, gdl: str = 'x', libre: bool = True, color: None | str = None,
                            ang: float | int = 0.0) -> VMobject:
    if color is None:
        color = RED if not libre else GREEN
    if gdl == 'x':
        ang = np.deg2rad(ang)  # usado cuando el gdl está rotado
        inicio = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[-longitud / 2 + offset], [0.0], [0.0]])).flatten()
        final = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[longitud / 2 + offset], [0.0], [0.0]])).flatten()
        grado_libertad = DoubleArrow(
            start=inicio,
            end=final,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=color,
            stroke_width=4,  # Grosor de la línea
            tip_shape_start=StealthTip,
            tip_shape_end=StealthTip,
            max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
        )
    elif gdl == 'y':
        ang = np.deg2rad(ang)  # usado cuando el gdl está rotado
        inicio = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[0.0], [-longitud / 2 + offset], [0.0]])).flatten()
        final = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[0.0], [longitud / 2 + offset], [0.0]])).flatten()
        grado_libertad = DoubleArrow(
            start=inicio,
            end=final,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=color,
            stroke_width=4,  # Grosor de la línea
            tip_shape_start=StealthTip,
            tip_shape_end=StealthTip,
            max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
        )
    else:
        radio = longitud / 2
        ang_i = np.deg2rad(90)
        ang_f = np.deg2rad(270)
        ang = np.deg2rad(offset)
        centro = ejes.c2p(*nodo)
        inicio = np.array(centro) + (np.array(
            [[np.cos(ang_i), -np.sin(ang_i), 0.0], [np.sin(ang_i), np.cos(ang_i), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[radio], [0.0], [0.0]])).flatten()
        final = np.array(centro) + (np.array(
            [[np.cos(ang_f), -np.sin(ang_f), 0.0], [np.sin(ang_f), np.cos(ang_f), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[radio], [0.0], [0.0]])).flatten()

        grado_libertad = CurvedDoubleArrow(
            start_point=inicio,
            end_point=final,
            angle=ang_f - ang_i,  # Ángulo de la curvatura de la flecha
            stroke_width=4,  # Grosor de la línea
            tip_length=0.15,  # Controla el tamaño absoluto de la punta
            tip_shape_start=StealthTip,
            tip_shape_end=StealthTip,
            color=color
        ).move_arc_center_to(centro).rotate(ang, about_point=centro)
    return grado_libertad


def crear_cota(p1, p2, texto, color=WHITE, tamano_remate=0.15):
    grupo_cota = VGroup()

    # 1. La línea principal de la cota
    linea_principal = Line(p1, p2, color=color, stroke_width=2)

    # 2. Matemáticas para los remates (ticks) perpendiculares
    vector = p2 - p1
    # Calculamos el vector normal (perpendicular) rotando 90 grados
    normal = np.array([-vector[1], vector[0], 0])
    normal = normal / np.linalg.norm(normal)  # Normalizamos a longitud 1

    # 3. Crear los remates en ambos extremos
    remate_inicio = Line(
        p1 - normal * tamano_remate,
        p1 + normal * tamano_remate,
        color=color, stroke_width=2
    )
    remate_fin = Line(
        p2 - normal * tamano_remate,
        p2 + normal * tamano_remate,
        color=color, stroke_width=2
    )

    # 4. Configurar el texto (Etiqueta)
    etiqueta = MathTex(texto, color=color).scale(0.7)
    # Fondo para que la línea principal no tache el número
    etiqueta.add_background_rectangle(color=BLACK, opacity=1, buff=0.1)
    etiqueta.move_to(linea_principal.get_center())

    # 5. Rotar el texto para que se alinee con la cota
    angulo = np.arctan2(vector[1], vector[0])
    # Si la cota está "al revés", rotamos 180° extra para que el texto no quede de cabeza
    if abs(angulo) > PI / 2:
        angulo -= PI
    etiqueta.rotate(angulo)

    # 6. Agrupar todo
    grupo_cota.add(linea_principal, remate_inicio, remate_fin, etiqueta)
    return grupo_cota


def ecuacion_matriz_rigidez_viga() -> VMobject:
    factor_matrix_rigidez = MathTex(r'\dfrac{EI}{L^{3}}')
    matrix_rigidez = Matrix(
        [['12', '6L', '-12', '6L'],
         ['6L', '4L^{2}', '-6L', '2L^{2}'],
         ['-12', '-6L', '12', '-6L'],
         ['6L', '2L^{2}', '-6L', '4L^{2}']]
    )
    return VGroup(factor_matrix_rigidez, matrix_rigidez)


def ecuacion_vector_fuerza_viga(id_elemento: int | str = '1', id_nodo_inicial: int | str = '1',
                                id_nodo_final: int | str = '2') -> VMobject:
    str_elemento = str(id_elemento)
    str_nodo_ini = str(id_nodo_inicial)
    str_nodo_fin = str(id_nodo_final)
    vector_fuerzas = Matrix(
        [["f^{(" + str_elemento + ")}_{" + str_nodo_ini + "y}"],
         ["m^{(" + str_elemento + ")}_{" + str_nodo_ini + "}"],
         ["f^{(" + str_elemento + ")}_{" + str_nodo_fin + "y}"], ["m^{(" + str_elemento + ")}_{" + str_nodo_fin + "}"]],
        left_bracket=r"\{",  # Llave izquierda
        right_bracket=r"\}"  # Llave derecha
    )
    return vector_fuerzas


def ecuacion_vector_desplazamiento_viga(id_nodo_inicial: int | str = '1', id_nodo_final: int | str = '2') -> VMobject:
    str_nodo_ini = str(id_nodo_inicial)
    str_nodo_fin = str(id_nodo_final)
    vector_deformacion = Matrix(
        [["v_{" + str_nodo_ini + "}"],
         [r"\phi_{" + str_nodo_ini + "}"],
         ["v_{" + str_nodo_fin + "}"],
         [r"\phi_{" + str_nodo_fin + "}"]
         ],
        left_bracket=r"\{",  # Llave izquierda
        right_bracket=r"\}"  # Llave derecha
    )
    return vector_deformacion

def ecuacion_vector_fuerza_nodal_equivalente_viga(id_nodo_inicial: int | str = '1',id_nodo_final: int | str = '2') -> VMobject:
    str_nodo_ini = str(id_nodo_inicial)
    str_nodo_fin = str(id_nodo_final)
    vector_fuerzas_nodal = Matrix(
        [["f_{" + str_nodo_ini + "y_{0}}"],
         ["m_{" + str_nodo_ini + "_{0}}"],
         ["f_{" + str_nodo_fin + "y_{0}}"], ["m_{" + str_nodo_fin + "_{0}}"]],
        left_bracket=r"\{",  # Llave izquierda
        right_bracket=r"\}"  # Llave derecha
    )
    return vector_fuerzas_nodal


def ecuacion_array_a_matriz(arr: np.ndarray, formato_num: str = "{x:g}", **kwargs) -> VMobject:
    if arr.ndim == 1:
        kwargs.setdefault("left_bracket", r"\{")
        kwargs.setdefault("right_bracket", r"\}")
        # Usamos .format(x=x) para inyectar el valor en la plantilla
        data = [[formato_num.format(x=x)] for x in arr]
        return Matrix(data, **kwargs)

    data = [[formato_num.format(x=x) for x in row] for row in arr]
    return Matrix(data, **kwargs)


def ecuacion_signo_igual():
    return MathTex('=')
def ecuacion_signo_menos():
    return MathTex('-')
def ecuacion_signo_mas():
    return MathTex('+')
def ecuacion_EI():
    return MathTex('EI')
def ecuacion_EI_inv():
    return MathTex(r'\dfrac{1}{EI}')


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
            test = np.array([1, 2, 3])
            self.play(FadeIn(ecuacion_array_a_matriz(test, left_bracket=r"[", right_bracket=r"]")), run_time=2)
            mi_plantilla = TexTemplate()
            mi_plantilla.add_to_preamble(r"\usepackage{cancel}")

            # 2. Tu arreglo (nota el uso de r"" en \cancel para evitar errores de Python)
            test = np.array(['F_{1y}', 'M_{1}', 'F_{2y}', 'M_{2}', 'F_{3y}', r'\cancel{M_{3}}', 'F_{4y}', 'M_{4}']).reshape((-1,1))

            # 3. Crear la matriz pasando la plantilla a los elementos internos
            matriz = Matrix(
                test,
                left_bracket=r"[",
                right_bracket=r"]",
                # Esto le dice a Manim que use tu plantilla para compilar cada entrada
                element_to_mobject_config={"tex_template": mi_plantilla}
            )

            self.play(FadeIn(matriz), run_time=2)
            self.play(FadeIn(ejes), run_time=2)
            # self.play(FadeIn(viga[1], viga[2]), run_time=2)
            self.play(FadeIn(viga[0]), run_time=2)
            self.play(FadeIn(armadura), run_time=2)
            self.play(FadeIn(carga_d2), run_time=2)
            self.play(FadeIn(crear_cota(ejes.c2p([2, 1, 0]), ejes.c2p([8, 1, 0]), r'6\,m', GRAY, 0.15)), run_time=2)
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
