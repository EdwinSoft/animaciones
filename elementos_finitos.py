from manim import *
import numpy as np
from biblioteca import *
from mnspy import Nodo, Viga, Ensamble


class EjemploVigasAnimacion(Scene):
    def construct(self):
        n_1 = Nodo('1', 0, grados_libertad={'y': False, 'eje_z': False})
        n_2 = Nodo('2', 10, grados_libertad={'y': False, 'eje_z': True})
        n_3 = Nodo('3', 20, grados_libertad={'y': False, 'eje_z': True})
        n_4 = Nodo('4', 25, grados_libertad={'y': False, 'eje_z': False})
        e_1 = Viga('1', n_1, n_2, E=1, I=1)
        e_2 = Viga('2', n_2, n_3, E=1, I=1)
        e_3 = Viga('3', n_3, n_4, E=1, I=1)
        e_1.agregar_carga_puntual(-80, 6.0)
        e_2.agregar_carga_distribuida(-24)
        mg = Ensamble([e_1, e_2, e_3])
        mg.solucionar_por_gauss_y_calcular_reacciones()
        ############
        ejes_coordenados = Axes(
            x_range=[0, 25, 1],
            y_range=[-6, 6, 1],
            x_length=25,
            y_length=12,
            axis_config={"include_tip": False, "stroke_width": 0}
        ).scale(0.5)
        ejes_planos = NumberPlane(
            x_range=[0, 25, 1],
            y_range=[-6, 6, 1],
            axis_config={
                "stroke_width": 0,  # Ejes más gruesos para resaltarlos
            },
            background_line_style={"stroke_opacity": 0.2
                                   # Puedes atenuar las líneas de la cuadrícula si no las quieres ver
                                   }
        ).scale(0.5)
        ejes = ejes_planos
        cargas = VGroup()
        for carga_puntual in mg._lista_cargas_puntuales:
            cp = elemento_carga((carga_puntual[1][0][0] + carga_puntual[2], 0.0, 0.0), ejes, 2, ang=90, saliente=False,
                                h=0.25 / 2)
            valor = MathTex(str(abs(carga_puntual[0])) + r"\,kN").next_to(cp, UP, buff=0.1).scale(0.5)
            cargas.add(cp)
            cargas.add(valor)
        for carga_distribuida in mg._lista_cargas_distribuidas:
            cp = elemento_carga_distribuida((carga_distribuida[1][0][0], 0.0, 0.0),
                                            (carga_distribuida[1][1][0], 0.0, 0.0), ejes, 0.25 / 2,
                                            saliente=False, longitud=1, n_cargas=20)
            valor_1 = MathTex(str(abs(carga_distribuida[0][0])) + r"\,kN").next_to(cp, UL, buff=0.0).scale(0.5).shift(
                RIGHT * 0.7)
            valor_2 = MathTex(str(abs(carga_distribuida[0][1])) + r"\,kN").next_to(cp, UR, buff=0.0).scale(0.5).shift(
                LEFT * 0.7)
            cargas.add(cp)
            cargas.add(valor_1)
            cargas.add(valor_2)
        # mg.solucion()
        mg.diagrama_cargas()

        nodos = VGroup()
        label_nodos = VGroup().set_z_index(1.5)
        soportes = VGroup().set_z_index(1)
        for n in mg._lista_nodos:
            nodos.add(Dot(ejes.c2p(n.punto), color=BLUE_A))
            label_nodos.add(
                LabeledDot(MathTex(n.nombre, color=WHITE), color=GREEN, stroke_color=GREEN, stroke_width=1,
                           fill_opacity=0.8).next_to(ejes.c2p(n.punto), DR, buff=-0.1).scale(
                    0.5))
            tipo_sop = n.get_soporte()
            if len(tipo_sop) == 2:
                tipo, estilo = tipo_sop
                if tipo == 0:  # pivotado
                    if estilo == 0:  # móvil
                        soportes.add(elemento_soporte(n.punto, ejes, 0, ang=0))
                    elif estilo == 1:  # fijo
                        soportes.add(elemento_soporte(n.punto, ejes, 1, ang=0))
                    elif estilo == 2:  # móvil
                        soportes.add(elemento_soporte(n.punto, ejes, 0, ang=180))
                    elif estilo == 3:  # fijo
                        soportes.add(elemento_soporte(n.punto, ejes, 1, ang=180))
                    elif estilo == 4:  # móvil
                        soportes.add(elemento_soporte(n.punto, ejes, 0, ang=270))
                    elif estilo == 5:  # fijo
                        soportes.add(elemento_soporte(n.punto, ejes, 1, ang=270))
                    elif estilo == 6:  # móvil
                        soportes.add(elemento_soporte(n.punto, ejes, 0, ang=90))
                    elif estilo == 7:  # fijo
                        soportes.add(elemento_soporte(n.punto, ejes, 1, ang=90))
                elif tipo == 1:  # empotrado
                    if estilo == 0:  # izquierda
                        soportes.add(elemento_soporte(n.punto, ejes, 2, ang=0))
                    elif estilo == 1:  # derecha
                        soportes.add(elemento_soporte(n.punto, ejes, 2, ang=180))
                    elif estilo == 2:  # abajo
                        soportes.add(elemento_soporte(n.punto, ejes, 2, ang=90))
                    elif estilo == 3:  # arriba
                        soportes.add(elemento_soporte(n.punto, ejes, 2, ang=270))
                    elif estilo == 4:  # izquierda con deslizadera
                        soportes.add(elemento_soporte(n.punto, ejes, 3, ang=0))
                    elif estilo == 5:  # derecha con deslizadera
                        soportes.add(elemento_soporte(n.punto, ejes, 3, ang=180))
                    elif estilo == 6:  # abajo con deslizadera
                        soportes.add(elemento_soporte(n.punto, ejes, 3, ang=90))
                    elif estilo == 7:  # arriba con deslizadera
                        soportes.add(elemento_soporte(n.punto, ejes, 3, ang=270))
        elementos = VGroup()
        label_elementos = VGroup().set_z_index(1.5)
        for el in mg._lista_elementos:
            elementos.add(elemento_viga(el.get_nodo_inicial().punto[0], el.get_nodo_final().punto[0], 0.25, ejes))
            punto_medio = ejes.c2p((np.array(el.get_nodo_inicial().punto) + np.array(el.get_nodo_final().punto)) / 2)
            # 1. Crear solo el texto
            texto = MathTex(el.nombre, color=WHITE)

            # 2. Crear el fondo que envuelve automáticamente al texto
            fondo = SurroundingRectangle(
                texto,
                color=RED,  # Color del fondo
                fill_opacity=0.8,  # Opacidad
                stroke_width=1,  # Sin línea de borde
                buff=0.1  # Padding
            )
            # 3. Agrupar, escalar y posicionar
            etiqueta_completa = VGroup(fondo, texto).scale(0.5)
            etiqueta_completa.move_to(punto_medio).shift(DOWN * 0.4)
            # 4. Añadir a la colección
            label_elementos.add(etiqueta_completa)
        cotas = VGroup()
        p_1 = ejes.c2p([0.0, 0.0, 0.0]) + DOWN
        p_2 = ejes.c2p([6.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_1, p_2, r'6\,m', GRAY))
        p_3 = ejes.c2p([10.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_2, p_3, r'4\,m', GRAY))
        p_4 = ejes.c2p([20.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_3, p_4, r'10\,m', GRAY))
        p_5 = ejes.c2p([25.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_4, p_5, r'5\,m', GRAY))
        enunciado = Tex(
            r"Determine las reacciones y las fuerzas en los extremos\\",
            r"de los elementos de la viga continua de tres vanos mostrada\\",
            r"en la Figura utilizando el método de rigidez matricial. $EI$= cte.",
            tex_environment="flushleft",  # Esto alinea el texto a la izquierda
            font_size=36
        ).to_edge(UP + LEFT)
        viga = elemento_viga(0.0, 25.0, 0.25, ejes)
        viga.set_color(GRAY_D)
        ### Grado libertad nodos
        gdl_y_1 = elemento_grado_libertad(n_1.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        gdl_eje_z_1 = elemento_grado_libertad(n_1.punto, ejes, gdl='eje_z', libre=False, longitud=1, offset=90)
        gdl_y_2 = elemento_grado_libertad(n_2.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        gdl_eje_z_2 = elemento_grado_libertad(n_2.punto, ejes, gdl='eje_z', libre=True, longitud=1, offset=-90)
        gdl_y_3 = elemento_grado_libertad(n_3.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        gdl_eje_z_3 = elemento_grado_libertad(n_3.punto, ejes, gdl='eje_z', libre=True, longitud=1, offset=-90)
        gdl_y_4 = elemento_grado_libertad(n_4.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        gdl_eje_z_4 = elemento_grado_libertad(n_4.punto, ejes, gdl='eje_z', libre=False, longitud=1, offset=90)
        label_y_1 = MathTex(r'v_{1}=0', color=RED).next_to(gdl_y_1, UP, buff=0.02).scale(0.5)
        label_eje_z_1 = MathTex(r'\phi_{1}=0', color=RED).next_to(gdl_eje_z_1, DR, buff=-0.4).scale(0.5)
        label_y_2 = MathTex(r'v_{2}=0', color=RED).next_to(gdl_y_2, DOWN, buff=0.02).scale(0.5)
        label_eje_z_2 = MathTex(r'\phi_{2}', color=GREEN).next_to(gdl_eje_z_2, UR, buff=-0.25).scale(0.5)
        label_y_3 = MathTex(r'v_{3}=0', color=RED).next_to(gdl_y_3, DOWN, buff=0.02).scale(0.5)
        label_eje_z_3 = MathTex(r'\phi_{3}', color=GREEN).next_to(gdl_eje_z_3, UR, buff=-0.25).scale(0.5)
        label_y_4 = MathTex(r'v_{4}=0', color=RED).next_to(gdl_y_4, UP, buff=0.02).scale(0.5)
        label_eje_z_4 = MathTex(r'\phi_{4}=0', color=RED).next_to(gdl_eje_z_4, DR, buff=-0.4).scale(0.5)
        # Ecuaciones generales de la viga
        ecuacion_local_viga = VGroup(Matrix([['f']], left_bracket=r"\{", right_bracket=r"\}"),
                                     ecuacion_signo_igual().copy(),
                                     Matrix([['k']]), Matrix([['d']], left_bracket=r"\{", right_bracket=r"\}"),
                                     ecuacion_signo_menos().copy(),
                                     Matrix([['f_0']], left_bracket=r"\{", right_bracket=r"\}")).arrange(RIGHT).move_to(
            DOWN * 2)

        factor_matrix_rigidez = MathTex(r'\dfrac{EI}{L^{3}}')
        matrix_rigidez = Matrix(
            [['12', '6L', '-12', '6L'],
             ['6L', '4L^{2}', '-6L', '2L^{2}'],
             ['-12', '-6L', '12', '-6L'],
             ['6L', '2L^{2}', '-6L', '4L^{2}']]
        )
        ## Ecuaciones Elemento 1
        ecuacion_local_viga_1 = ecuacion_local_viga.copy()
        matriz_k_1 = ecuacion_vector_fuerza_viga()
        ### Cargas nodales equivalentes
        f_1_0 = elemento_carga(n_1.punto, ejes, longitud=1, saliente=False, ang=90)
        label_f_1_0 = MathTex(str(abs(e_1._fuerzas_i[0, 0])) + r"\,kN").next_to(f_1_0, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_1_0 = elemento_momento(n_1.punto, ejes, positivo=False)
        label_m_1_0 = MathTex(str(abs(e_1._fuerzas_i[1, 0])) + r"\,kN\cdot m").next_to(m_1_0, UP, buff=0.0).scale(
            0.5).shift(
            RIGHT * 0.7)
        f_2_0 = elemento_carga(n_2.punto, ejes, longitud=1, saliente=False, ang=90)
        label_f_2_0 = MathTex(str(abs(e_1._fuerzas_j[0, 0])) + r"\,kN").next_to(f_2_0, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_2_0 = elemento_momento(n_2.punto, ejes, positivo=True, ang=0)
        label_m_2_0 = MathTex(str(abs(e_1._fuerzas_j[1, 0])) + r"\,kN\cdot m").next_to(m_2_0, UP, buff=0.0).scale(
            0.5).shift(
            LEFT * 0.7)
        ### Cargas en elemento 1
        cargas_eq_1 = VGroup(f_1_0, m_1_0, f_2_0, m_2_0)
        label_cargas_eq_1 = VGroup(label_f_1_0, label_m_1_0, label_f_2_0, label_m_2_0)
        ### Grados de libertad en elemento 1
        grados_el_1 = VGroup(gdl_y_1, gdl_eje_z_1, gdl_y_2, gdl_eje_z_2)
        label_etiquetas_grados_el_1 = VGroup(label_y_1, label_eje_z_1, label_y_2, label_eje_z_2)
        ### Escena elemento 1
        escena_elemento_1 = VGroup(elementos[0], nodos[0:2], soportes[0:2], label_elementos[0], label_nodos[0:2],
                                   cargas[0:2])
        factor_matrix_rigidez_1_1 = MathTex(r'\dfrac{EI}{1000}')
        factor_matrix_rigidez_1_2 = MathTex('EI')
        factor_matrix_rigidez_1_3 = factor_matrix_rigidez_1_2.copy()
        factor_matrix_rigidez_1_4 = factor_matrix_rigidez_1_2.copy()

        matrix_rigidez_1_1 = Matrix(
            [['12', '60', '-12', '60'],
             ['60', '400', '-60', '200'],
             ['-12', '-60', '12', '-60'],
             ['60', '200', '-60', '400']]
        )
        matrix_rigidez_1_2 = Matrix(
            [['0.012', '0.06', '-0.012', '0.06'],
             ['0.06', '0.4', '-0.06', '0.2'],
             ['-0.012', '-0.06', '0.012', '-0.06'],
             ['0.06', '0.2', '-0.060', '0.4']],
            h_buff=1.8
        )
        matrix_rigidez_1_3 = matrix_rigidez_1_2.copy()
        matrix_rigidez_1_4 = matrix_rigidez_1_2.copy()
        vector_desplazamientos_el_1 = ecuacion_vector_desplazamiento_viga()
        vector_desplazamientos_el_1_modificado = Matrix(
            [["v_{1}=0"], [r"\phi_{1}=0"], ["v_{2}=0"], [r"\phi_{2}"]],
            left_bracket=r"\{",  # Llave izquierda
            right_bracket=r"\}",  # Llave derecha
            element_to_mobject_config={
                "tex_to_color_map": {
                    r"\phi_{2}": BLUE
                }
            }
        )
        vector_desplazamientos_modificado_1_3 = vector_desplazamientos_el_1_modificado.copy()
        vector_desplazamientos_modificado_1_4 = vector_desplazamientos_el_1_modificado.copy()
        vector_fuerza_nodal_equivalente_viga_1 = ecuacion_array_a_matriz(e_1._obtener_fuerzas(), left_bracket=r"\{",
                                                                         right_bracket=r"\}")
        mr_elemento_1 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez.copy(),
                               matrix_rigidez.copy(),
                               vector_desplazamientos_el_1.copy(), ecuacion_signo_menos().copy(),
                               ecuacion_vector_fuerza_nodal_equivalente_viga().copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_1.to_edge(DOWN).scale(0.5)
        mr_elemento_1_1 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_1_1,
                                 matrix_rigidez_1_1, vector_desplazamientos_el_1.copy(), ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga().copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_1_1.to_edge(DOWN).scale(0.5)
        mr_elemento_1_2 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_1_2,
                                 matrix_rigidez_1_2, vector_desplazamientos_el_1.copy(), ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga().copy()).arrange(RIGHT,
                                                                                                 buff=0.2)
        mr_elemento_1_2.to_edge(DOWN).scale(0.5)
        mr_elemento_1_3 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_1_3,
                                 matrix_rigidez_1_3, vector_desplazamientos_modificado_1_3,
                                 ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga().copy()).arrange(RIGHT,
                                                                                                 buff=0.2)
        mr_elemento_1_3.to_edge(DOWN).scale(0.5)
        mr_elemento_1_4 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_1_4,
                                 matrix_rigidez_1_4, vector_desplazamientos_modificado_1_4,
                                 ecuacion_signo_menos().copy(),
                                 vector_fuerza_nodal_equivalente_viga_1).arrange(RIGHT,
                                                                                 buff=0.2)
        mr_elemento_1_4.to_edge(DOWN).scale(0.5)
        ## Ecuaciones Elemento 2
        ecuacion_local_viga_2 = ecuacion_local_viga.copy()
        matriz_k_2 = ecuacion_vector_fuerza_viga(2, 2, 3)
        ### Cargas nodales equivalentes
        # f_2_0 = elemento_carga(n_2.punto, ejes, longitud=1, saliente=False, ang=90)
        # label_f_2_0 = MathTex(str(abs(e_2._fuerzas_i[0, 0])) + r"\,kN").next_to(f_2_0, UP, buff=0.0).scale(0.5).shift(
        #     RIGHT * 0.0)
        # m_2_0 = elemento_momento(n_2.punto, ejes, positivo=True, ang=0)
        # label_m_2_0 = MathTex(str(abs(e_2._fuerzas_i[1, 0])) + r"\,kN\cdot m").next_to(m_2_0, UP, buff=0.0).scale(
        #     0.5).shift(
        #     LEFT * 0.7)
        f_3_0 = elemento_carga(n_3.punto, ejes, longitud=1, saliente=False, ang=90)
        label_f_3_0 = MathTex(str(abs(e_1._fuerzas_j[0, 0])) + r"\,kN").next_to(f_3_0, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_3_0 = elemento_momento(n_3.punto, ejes, positivo=True, ang=0)
        label_m_3_0 = MathTex(str(abs(e_1._fuerzas_j[1, 0])) + r"\,kN\cdot m").next_to(m_3_0, UP, buff=0.0).scale(
            0.5).shift(
            LEFT * 0.7)
        ### Cargas en elemento 2
        cargas_eq_2 = VGroup(f_2_0, m_2_0, f_3_0, m_3_0)
        label_cargas_eq_2 = VGroup(label_f_2_0, label_m_2_0, label_f_3_0, label_m_3_0)
        ### Grados de libertad en elemento 1
        grados_el_2 = VGroup(gdl_y_2, gdl_eje_z_2, gdl_y_3, gdl_eje_z_3)
        label_etiquetas_grados_el_2 = VGroup(label_y_2, label_eje_z_2, label_y_3, label_eje_z_3)
        ### Escena elemento 2
        escena_elemento_2 = VGroup(elementos[1], nodos[1:3], soportes[1:3], label_elementos[1], label_nodos[1:3],
                                   cargas[2:5])
        factor_matrix_rigidez_2_1 = MathTex(r'\dfrac{EI}{1000}')
        factor_matrix_rigidez_2_2 = MathTex('EI')
        factor_matrix_rigidez_2_3 = factor_matrix_rigidez_2_2.copy()
        factor_matrix_rigidez_2_4 = factor_matrix_rigidez_2_2.copy()

        matrix_rigidez_2_1 = Matrix(
            [['12', '60', '-12', '60'],
             ['60', '400', '-60', '200'],
             ['-12', '-60', '12', '-60'],
             ['60', '200', '-60', '400']]
        )
        matrix_rigidez_2_2 = Matrix(
            [['0.012', '0.06', '-0.012', '0.06'],
             ['0.06', '0.4', '-0.06', '0.2'],
             ['-0.012', '-0.06', '0.012', '-0.06'],
             ['0.06', '0.2', '-0.060', '0.4']],
            h_buff=1.8
        )
        matrix_rigidez_2_3 = matrix_rigidez_2_2.copy()
        matrix_rigidez_2_4 = matrix_rigidez_2_2.copy()
        vector_desplazamientos_el_2 = ecuacion_vector_desplazamiento_viga(2, 3)
        vector_desplazamientos_el_2_modificado = Matrix(
            [["v_{2}=0"], [r"\phi_{2}"], ["v_{3}=0"], [r"\phi_{3}"]],
            left_bracket=r"\{",  # Llave izquierda
            right_bracket=r"\}",  # Llave derecha
            element_to_mobject_config={
                "tex_to_color_map": {
                    r"\phi_{2}": BLUE,
                    r"\phi_{3}": BLUE
                }
            }
        )
        vector_desplazamientos_modificado_2_3 = vector_desplazamientos_el_2_modificado.copy()
        vector_desplazamientos_modificado_2_4 = vector_desplazamientos_el_2_modificado.copy()
        vector_fuerza_nodal_equivalente_viga_2 = ecuacion_array_a_matriz(e_2._obtener_fuerzas(), left_bracket=r"\{",
                                                                         right_bracket=r"\}")
        mr_elemento_2 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez.copy(),
                               matrix_rigidez.copy(),
                               vector_desplazamientos_el_2.copy(), ecuacion_signo_menos().copy(),
                               ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_2.to_edge(DOWN).scale(0.5)
        mr_elemento_2_1 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_1,
                                 matrix_rigidez_2_1, vector_desplazamientos_el_2.copy(), ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_2_1.to_edge(DOWN).scale(0.5)
        mr_elemento_2_2 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_2,
                                 matrix_rigidez_2_2, vector_desplazamientos_el_2.copy(), ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT,
                                                                                                     buff=0.2)
        mr_elemento_2_2.to_edge(DOWN).scale(0.5)
        mr_elemento_2_3 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_3,
                                 matrix_rigidez_2_3, vector_desplazamientos_modificado_2_3,
                                 ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT,
                                                                                                     buff=0.2)
        mr_elemento_2_3.to_edge(DOWN).scale(0.5)
        mr_elemento_2_4 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_4,
                                 matrix_rigidez_2_4, vector_desplazamientos_modificado_2_4,
                                 ecuacion_signo_menos().copy(),
                                 vector_fuerza_nodal_equivalente_viga_2).arrange(RIGHT,
                                                                                 buff=0.2)
        mr_elemento_2_4.to_edge(DOWN).scale(0.5)
        ## Ecuaciones Elemento 3

        ## Diagrama viga inicial
        escena_inicial = VGroup(viga, soportes, cargas, cotas)
        escena_inicial.save_state()
        escena_inicial.to_edge(DOWN + LEFT)
        escena = VGroup(nodos, elementos, soportes, label_elementos, label_nodos, cargas, cotas)

        # Animaciones
        ## Enunciado
        self.play(Write(enunciado), run_time=5)
        ## Diagrama de la viga
        self.play(FadeIn(escena_inicial), run_time=2)
        self.wait(5)
        self.play(FadeOut(enunciado), run_time=2)
        self.play(Restore(escena_inicial), run_time=2)
        self.wait(5)
        ## Discretización de la viga
        self.play(Create(ejes), run_time=2)
        self.play(FadeOut(viga), run_time=2)
        self.play(DrawBorderThenFill(nodos), DrawBorderThenFill(elementos), run_time=2)
        self.play(Write(label_nodos), Write(label_elementos), run_time=2)
        self.wait(5)
        ## Desvanecimiento de la viga
        self.play(FadeOut(escena), run_time=2)

        ## Análisis Elemento 1
        self.play(FadeIn(escena_elemento_1), run_time=2)
        self.wait(1)
        self.play(Write(ecuacion_local_viga_1), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_local_viga_1, mr_elemento_1), run_time=2)
        self.play(ReplacementTransform(mr_elemento_1, mr_elemento_1_1), run_time=2)
        self.play(ReplacementTransform(mr_elemento_1_1, mr_elemento_1_2), run_time=2)
        self.wait(2)
        self.play(FadeOut(soportes[0:2]), run_time=2)
        self.play(FadeIn(grados_el_1), run_time=2)
        self.play(Write(label_etiquetas_grados_el_1), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(mr_elemento_1_2[4].get_brackets(), mr_elemento_1_3[4].get_brackets()),
                  ReplacementTransform(mr_elemento_1_2[0:4], mr_elemento_1_3[0:4]),
                  ReplacementTransform(mr_elemento_1_2[5:7], mr_elemento_1_3[5:7]),
                  FadeOut(mr_elemento_1_2[4].get_entries()),
                  ReplacementTransform(label_y_1, mr_elemento_1_3[4].get_entries()[0]),
                  ReplacementTransform(label_eje_z_1, mr_elemento_1_3[4].get_entries()[1]),
                  ReplacementTransform(label_y_2, mr_elemento_1_3[4].get_entries()[2]),
                  ReplacementTransform(label_eje_z_2, mr_elemento_1_3[4].get_entries()[3]),
                  Unwrite(gdl_y_1), Unwrite(gdl_eje_z_1), Unwrite(gdl_y_2), Unwrite(gdl_eje_z_2), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(cargas[0:2], VGroup(cargas_eq_1, label_cargas_eq_1)), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(mr_elemento_1_3[6].get_brackets(), mr_elemento_1_4[6].get_brackets()),
                  ReplacementTransform(mr_elemento_1_3[0:6], mr_elemento_1_4[0:6]),
                  FadeOut(mr_elemento_1_3[6].get_entries()),
                  ReplacementTransform(label_f_1_0, mr_elemento_1_4[6].get_entries()[0]),
                  ReplacementTransform(label_m_1_0, mr_elemento_1_4[6].get_entries()[1]),
                  ReplacementTransform(label_f_2_0, mr_elemento_1_4[6].get_entries()[2]),
                  ReplacementTransform(label_m_2_0, mr_elemento_1_4[6].get_entries()[3]),
                  Unwrite(f_1_0), Unwrite(m_1_0), Unwrite(f_2_0), Unwrite(m_2_0), run_time=2)
        self.wait(5)
        self.play(FadeOut(elementos[0], nodos[0:2], label_elementos[0], label_nodos[0:2]), FadeOut(mr_elemento_1_4))
        ## Análisis Elemento 2
        gdl_y_2 = elemento_grado_libertad(n_2.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        gdl_eje_z_2 = elemento_grado_libertad(n_2.punto, ejes, gdl='eje_z', libre=True, longitud=1, offset=-90)
        self.play(FadeIn(escena_elemento_2), run_time=2)
        self.wait(1)
        self.play(Write(ecuacion_local_viga_2), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_local_viga_2, mr_elemento_2), run_time=2)
        self.play(ReplacementTransform(mr_elemento_2, mr_elemento_2_1), run_time=2)
        self.play(ReplacementTransform(mr_elemento_2_1, mr_elemento_2_2), run_time=2)
        self.wait(2)
        self.play(FadeOut(soportes[1:3]), run_time=2)
        self.play(FadeIn(grados_el_2), run_time=2)
        self.play(Write(label_etiquetas_grados_el_2), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(mr_elemento_2_2[4].get_brackets(), mr_elemento_2_3[4].get_brackets()),
                  ReplacementTransform(mr_elemento_2_2[0:4], mr_elemento_2_3[0:4]),
                  ReplacementTransform(mr_elemento_2_2[5:7], mr_elemento_2_3[5:7]),
                  FadeOut(mr_elemento_2_2[4].get_entries()),
                  ReplacementTransform(label_y_2, mr_elemento_2_3[4].get_entries()[0]),
                  ReplacementTransform(label_eje_z_2, mr_elemento_2_3[4].get_entries()[1]),
                  ReplacementTransform(label_y_3, mr_elemento_2_3[4].get_entries()[2]),
                  ReplacementTransform(label_eje_z_3, mr_elemento_2_3[4].get_entries()[3]),
                  Unwrite(gdl_y_2), Unwrite(gdl_eje_z_2), Unwrite(gdl_y_3), Unwrite(gdl_eje_z_3), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(cargas[2:5], VGroup(cargas_eq_2, label_cargas_eq_2)), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(mr_elemento_2_3[6].get_brackets(), mr_elemento_2_4[6].get_brackets()),
                  ReplacementTransform(mr_elemento_2_3[0:6], mr_elemento_2_4[0:6]),
                  FadeOut(mr_elemento_2_3[6].get_entries()),
                  ReplacementTransform(label_f_2_0, mr_elemento_2_4[6].get_entries()[0]),
                  ReplacementTransform(label_m_2_0, mr_elemento_2_4[6].get_entries()[1]),
                  ReplacementTransform(label_f_3_0, mr_elemento_2_4[6].get_entries()[2]),
                  ReplacementTransform(label_m_3_0, mr_elemento_2_4[6].get_entries()[3]),
                  Unwrite(f_2_0), Unwrite(m_2_0), Unwrite(f_3_0), Unwrite(m_3_0), run_time=2)
        self.wait(5)
        self.play(FadeOut(elementos[1], nodos[1:3], label_elementos[1], label_nodos[1:3]), FadeOut(mr_elemento_2_4))
        ## Análisis Elemento 3
