from manim import *
import numpy as np
from biblioteca import *
from mnspy import Nodo, Viga


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
        mg = EnsambleAnimacion([e_1, e_2, e_3])
        matriz_global_base = mg.sistema_ecuaciones_matriz_rigidez_global(EI_cte=True, reducida=False)
        matriz_global = matriz_global_base.copy().scale(0.5).arrange(RIGHT)
        matriz_global_reducida_inicial = mg.sistema_ecuaciones_matriz_rigidez_global(EI_cte=True, reducida=True)
        matriz_global_reducida = matriz_global_reducida_inicial.copy().scale(0.5).arrange(RIGHT)
        matriz_global_reducida_final = VGroup(matriz_global_reducida_inicial[6].copy(), ecuacion_signo_igual(),
                                              ecuacion_EI(), matriz_global_reducida_inicial[3].copy(),
                                              matriz_global_reducida_inicial[4].copy()).scale(0.5).arrange(RIGHT)
        matriz = matriz_global_reducida_inicial[3].copy()
        vec_k_reduc_inverso = ecuacion_array_a_matriz(np.linalg.inv(np.array(mg._union._k.obtener_matriz(True))),
                                                      h_buff=2.8)
        sol = np.linalg.inv(np.array(mg._union._k.obtener_matriz(True))) @ np.array(mg._union._k.obtener_fuerzas(True))
        solucion_reducida = ecuacion_array_a_matriz(sol, formato_num='{x:.8f}', left_bracket=r"\{", right_bracket=r"\}")
        superindice = MathTex("-1").next_to(matriz, RIGHT, aligned_edge=UP, buff=0.1)
        matriz_global_reducida_final_2 = VGroup(ecuacion_EI_inv(),
                                                VGroup(matriz_global_reducida_inicial[3].copy(), superindice),
                                                matriz_global_reducida_inicial[6].copy(),
                                                ecuacion_signo_igual(), matriz_global_reducida_inicial[4].copy()).scale(
            0.5).arrange(RIGHT)
        matriz_global_reducida_final_3 = VGroup(ecuacion_EI_inv(), vec_k_reduc_inverso,
                                                matriz_global_reducida_inicial[6].copy(),
                                                ecuacion_signo_igual(),
                                                matriz_global_reducida_inicial[4].copy()).scale(
            0.5).arrange(RIGHT)
        matriz_global_reducida_final_4 = VGroup(ecuacion_EI_inv(), solucion_reducida.copy(), ecuacion_signo_igual(),
                                                matriz_global_reducida_inicial[4].copy()).scale(
            0.5).arrange(RIGHT)
        sol_1 = VGroup(MathTex(r'{\phi_2}').set_color(BLUE), ecuacion_signo_igual(),
                       MathTex(r'\dfrac{' + f'{sol[0][0]:.8f}' + '}{EI}')).scale(0.5).arrange(RIGHT)
        sol_2 = VGroup(MathTex(r'{\phi_3}').set_color(BLUE), ecuacion_signo_igual(),
                       MathTex(r'\dfrac{' + f'{sol[1][0]:.8f}' + '}{EI}')).scale(0.5).arrange(RIGHT).next_to(sol_1,
                                                                                                             DOWN)
        # Grados de libertad
        n_1_gdl = VGroup(mg.get_grados_libertad(n_1, 'y', offset=0.0, longitud=0.8),
                         mg.get_grados_libertad(n_1, 'eje_z', longitud=1, offset=90))
        n_1_labels_gdl = elemento_label_grados_libertad(n_1)
        n_2_gdl = VGroup(mg.get_grados_libertad(n_2, 'y', offset=0.0, longitud=0.8),
                         mg.get_grados_libertad(n_2, 'eje_z', longitud=1, offset=-90))
        n_2_labels_gdl = elemento_label_grados_libertad(n_2)
        n_3_gdl = VGroup(mg.get_grados_libertad(n_3, 'y', offset=0.0, longitud=0.8),
                         mg.get_grados_libertad(n_3, 'eje_z', longitud=1, offset=-90))
        n_3_labels_gdl = elemento_label_grados_libertad(n_3)
        n_4_gdl = VGroup(mg.get_grados_libertad(n_4, 'y', offset=0.0, longitud=0.8),
                         mg.get_grados_libertad(n_4, 'eje_z', longitud=1, offset=90))
        n_4_labels_gdl = elemento_label_grados_libertad(n_4)
        vector_desplazamientos_el_1_modificado = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_1, EI_cte=True,
                                                                                                       reducida=False)
        vector_desplazamientos_el_2_modificado = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_2, EI_cte=True,
                                                                                                       reducida=False)
        vector_desplazamientos_el_3_modificado = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_3, EI_cte=True,
                                                                                                       reducida=False)
        ##########################################################################################
        mg.solucionar_por_gauss_y_calcular_reacciones()
        sol_final = np.array(mg._union._k.obtener_matriz(False)) @ np.array(mg._union._k.obtener_desplazamientos(False))
        sol_final_resta = sol_final - mg._union._k.obtener_fuerzas(False)
        solucion = ecuacion_array_a_matriz(sol_final, formato_num='{x:.8f}', left_bracket=r"\{", right_bracket=r"\}")

        matriz_global_final_base = mg.sistema_ecuaciones_matriz_rigidez_global(EI_cte=True, reducida=False)
        matriz_global_final = matriz_global_final_base.copy().scale(0.35).arrange(RIGHT)
        matriz_global_final_2 = matriz_global_final_base.copy()
        matriz_global_final_2[0] = matriz_global_base.copy()[0]
        matriz_global_final_2.scale(0.35).arrange(RIGHT)
        matriz_global_final_3 = matriz_global_final_base.copy()
        matriz_global_final_3[0] = matriz_global_base.copy()[0]
        matriz_global_final_3.submobjects.pop(2)
        matriz_global_final_3.submobjects.pop(2)
        matriz_global_final_3[2] = solucion
        matriz_global_final_4 = matriz_global_final_3.copy()
        matriz_global_final_3.scale(0.35).arrange(RIGHT)
        matriz_global_final_4.submobjects.pop(2)
        matriz_global_final_4.submobjects.pop(2)
        matriz_global_final_4[2] = ecuacion_array_a_matriz(sol_final_resta, formato_num='{x:.8f}', left_bracket=r"\{",
                                                           right_bracket=r"\}")
        matriz_global_final_4.scale(0.35).arrange(RIGHT)

        ############

        # ejes = mg.ejes
        cargas_puntuales = mg.get_cargas_puntuales(longitud=2.0)
        cargas_distribuidas = mg.get_cargas_distribuidas(longitud=1.0)
        cargas = cargas_puntuales + cargas_distribuidas
        # cargas = VGroup()
        # for carga_puntual in mg._lista_cargas_puntuales:
        #     cp = elemento_carga((carga_puntual[1][0][0] + carga_puntual[2], 0.0, 0.0), ejes, 2, ang=90, saliente=False,
        #                         h=0.25 / 2)
        #     valor = MathTex(str(abs(carga_puntual[0])) + r"\,kN").next_to(cp, UP, buff=0.1).scale(0.5)
        #     cargas.add(cp)
        #     cargas.add(valor)
        # for carga_distribuida in mg._lista_cargas_distribuidas:
        #     cp = elemento_carga_distribuida((carga_distribuida[1][0][0], 0.0, 0.0),
        #                                     (carga_distribuida[1][1][0], 0.0, 0.0), ejes, 0.25 / 2,
        #                                     saliente=False, longitud=1, n_cargas=20)
        #     valor_1 = MathTex(str(abs(carga_distribuida[0][0])) + r"\,kN/m").next_to(cp, UL, buff=0.0).scale(0.5).shift(
        #         RIGHT * 0.7)
        #     valor_2 = MathTex(str(abs(carga_distribuida[0][1])) + r"\,kN/m").next_to(cp, UR, buff=0.0).scale(0.5).shift(
        #         LEFT * 0.7)
        #     cargas.add(cp)
        #     cargas.add(valor_1)
        #     cargas.add(valor_2)

        # mg.solucion()
        # mg.diagrama_cargas()
        nodos, label_nodos, soportes = mg.get_nodos_y_soportes()
        # nodos = VGroup()
        # label_nodos = VGroup().set_z_index(1.5)
        # soportes = VGroup().set_z_index(1)
        # for n in mg._lista_nodos:
        #     nodos.add(Dot(ejes.c2p(n.punto), color=BLUE_A))
        #     label_nodos.add(
        #         LabeledDot(MathTex(n.nombre, color=WHITE), color=GREEN, stroke_color=GREEN, stroke_width=1,
        #                    fill_opacity=0.8).next_to(ejes.c2p(n.punto), DR, buff=-0.1).scale(
        #             0.5))
        #     tipo_sop = n.get_soporte()
        #     if len(tipo_sop) == 2:
        #         tipo, estilo = tipo_sop
        #         if tipo == 0:  # pivotado
        #             if estilo == 0:  # móvil
        #                 soportes.add(elemento_soporte(n.punto, ejes, 0, ang=0))
        #             elif estilo == 1:  # fijo
        #                 soportes.add(elemento_soporte(n.punto, ejes, 1, ang=0))
        #             elif estilo == 2:  # móvil
        #                 soportes.add(elemento_soporte(n.punto, ejes, 0, ang=180))
        #             elif estilo == 3:  # fijo
        #                 soportes.add(elemento_soporte(n.punto, ejes, 1, ang=180))
        #             elif estilo == 4:  # móvil
        #                 soportes.add(elemento_soporte(n.punto, ejes, 0, ang=270))
        #             elif estilo == 5:  # fijo
        #                 soportes.add(elemento_soporte(n.punto, ejes, 1, ang=270))
        #             elif estilo == 6:  # móvil
        #                 soportes.add(elemento_soporte(n.punto, ejes, 0, ang=90))
        #             elif estilo == 7:  # fijo
        #                 soportes.add(elemento_soporte(n.punto, ejes, 1, ang=90))
        #         elif tipo == 1:  # empotrado
        #             if estilo == 0:  # izquierda
        #                 soportes.add(elemento_soporte(n.punto, ejes, 2, ang=0))
        #             elif estilo == 1:  # derecha
        #                 soportes.add(elemento_soporte(n.punto, ejes, 2, ang=180))
        #             elif estilo == 2:  # abajo
        #                 soportes.add(elemento_soporte(n.punto, ejes, 2, ang=90))
        #             elif estilo == 3:  # arriba
        #                 soportes.add(elemento_soporte(n.punto, ejes, 2, ang=270))
        #             elif estilo == 4:  # izquierda con deslizadera
        #                 soportes.add(elemento_soporte(n.punto, ejes, 3, ang=0))
        #             elif estilo == 5:  # derecha con deslizadera
        #                 soportes.add(elemento_soporte(n.punto, ejes, 3, ang=180))
        #             elif estilo == 6:  # abajo con deslizadera
        #                 soportes.add(elemento_soporte(n.punto, ejes, 3, ang=90))
        #             elif estilo == 7:  # arriba con deslizadera
        #                 soportes.add(elemento_soporte(n.punto, ejes, 3, ang=270))
        # elementos = VGroup()
        # label_elementos = VGroup().set_z_index(1.5)
        # for el in mg._lista_elementos:
        #     elementos.add(elemento_viga(el.get_nodo_inicial().punto[0], el.get_nodo_final().punto[0], 0.25, ejes))
        #     punto_medio = ejes.c2p((np.array(el.get_nodo_inicial().punto) + np.array(el.get_nodo_final().punto)) / 2)
        #     # 1. Crear solo el texto
        #     texto = MathTex(el.nombre, color=WHITE)
        #
        #     # 2. Crear el fondo que envuelve automáticamente al texto
        #     fondo = SurroundingRectangle(
        #         texto,
        #         color=RED,  # Color del fondo
        #         fill_opacity=0.8,  # Opacidad
        #         stroke_width=1,  # Sin línea de borde
        #         buff=0.1  # Padding
        #     )
        #     # 3. Agrupar, escalar y posicionar
        #     etiqueta_completa = VGroup(fondo, texto).scale(0.5)
        #     etiqueta_completa.move_to(punto_medio).shift(DOWN * 0.4)
        #     # 4. Añadir a la colección
        #     label_elementos.add(etiqueta_completa)
        elementos, label_elementos = mg.get_elementos()
        cotas = VGroup()
        p_1 = mg.c2p([0.0, 0.0, 0.0]) + DOWN
        p_2 = mg.c2p([6.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_1, p_2, r'6\,m', GRAY))
        p_3 = mg.c2p([10.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_2, p_3, r'4\,m', GRAY))
        p_4 = mg.c2p([20.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_3, p_4, r'10\,m', GRAY))
        p_5 = mg.c2p([25.0, 0.0, 0.0]) + DOWN
        cotas.add(crear_cota(p_4, p_5, r'5\,m', GRAY))
        enunciado = Tex(
            r"Determine las reacciones y las fuerzas en los extremos\\",
            r"de los elementos de la viga continua de tres vanos mostrada\\",
            r"en la Figura utilizando el método de rigidez matricial. $EI$= cte.",
            tex_environment="flushleft",  # Esto alinea el texto a la izquierda
            font_size=36
        ).to_edge(UP + LEFT)
        viga = elemento_viga(0.0, 25.0, 0.25, mg.ejes)
        viga.set_color(GRAY_D)
        ### Grado libertad nodos
        # gdl_y_1, label_y_1, gdl_eje_z_1, label_eje_z_1 = (
        #     mg.get_grados_libertad(n_1,{'y': [{'offset': 0.0, 'longitud': 0.8}],
        #                                                                          'eje_z': {'offset': 90,
        #                                                                                    'longitud': 1.0}}, ))
        # gdl_y_1 = elemento_grado_libertad(n_1.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        # gdl_eje_z_1 = elemento_grado_libertad(n_1.punto, ejes, gdl='eje_z', libre=False, longitud=1, offset=90)
        # gdl_y_2 = elemento_grado_libertad(n_2.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        # gdl_eje_z_2 = elemento_grado_libertad(n_2.punto, ejes, gdl='eje_z', libre=True, longitud=1, offset=-90)
        # gdl_y_3 = elemento_grado_libertad(n_3.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        # gdl_eje_z_3 = elemento_grado_libertad(n_3.punto, ejes, gdl='eje_z', libre=True, longitud=1, offset=-90)
        # gdl_y_4 = elemento_grado_libertad(n_4.punto, ejes, gdl='y', libre=False, offset=0.0, longitud=0.8)
        # gdl_eje_z_4 = elemento_grado_libertad(n_4.punto, ejes, gdl='eje_z', libre=False, longitud=1, offset=90)
        # label_y_1 = MathTex(r'v_{1}=0', color=RED).next_to(gdl_y_1, UP, buff=0.02).scale(0.5)
        # label_eje_z_1 = MathTex(r'\phi_{1}=0', color=RED).next_to(gdl_eje_z_1, DR, buff=-0.4).scale(0.5)
        # label_y_2 = MathTex(r'v_{2}=0', color=RED).next_to(gdl_y_2, DOWN, buff=0.02).scale(0.5)
        # label_eje_z_2 = MathTex(r'\phi_{2}', color=GREEN).next_to(gdl_eje_z_2, UR, buff=-0.25).scale(0.5)
        # label_y_3 = MathTex(r'v_{3}=0', color=RED).next_to(gdl_y_3, DOWN, buff=0.02).scale(0.5)
        # label_eje_z_3 = MathTex(r'\phi_{3}', color=GREEN).next_to(gdl_eje_z_3, UR, buff=-0.25).scale(0.5)
        # label_y_4 = MathTex(r'v_{4}=0', color=RED).next_to(gdl_y_4, UP, buff=0.02).scale(0.5)
        # label_eje_z_4 = MathTex(r'\phi_{4}=0', color=RED).next_to(gdl_eje_z_4, DOWN, buff=0.0).scale(0.5)
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
        f_1_0 = elemento_carga(n_1.punto, mg.ejes, longitud=1, saliente=False, ang=90)
        label_f_1_0 = MathTex(str(abs(e_1._fuerzas_i[0, 0])) + r"\,kN").next_to(f_1_0, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_1_0 = elemento_momento(n_1.punto, mg.ejes, positivo=False)
        label_m_1_0 = MathTex(str(abs(e_1._fuerzas_i[1, 0])) + r"\,kN\cdot m").next_to(m_1_0, UP, buff=0.0).scale(
            0.5).shift(
            RIGHT * 0.7)
        f_2_0 = elemento_carga(n_2.punto, mg.ejes, longitud=1, saliente=False, ang=90)
        label_f_2_0 = MathTex(str(abs(e_1._fuerzas_j[0, 0])) + r"\,kN").next_to(f_2_0, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_2_0 = elemento_momento(n_2.punto, mg.ejes, positivo=True, ang=0)
        label_m_2_0 = MathTex(str(abs(e_1._fuerzas_j[1, 0])) + r"\,kN\cdot m").next_to(m_2_0, UP, buff=0.0).scale(
            0.5).shift(
            LEFT * 0.7)
        ### Cargas en elemento 1
        cargas_eq_1 = VGroup(f_1_0.copy(), m_1_0.copy(), f_2_0.copy(), m_2_0.copy())
        label_cargas_eq_1 = VGroup(label_f_1_0.copy(), label_m_1_0.copy(), label_f_2_0.copy(), label_m_2_0.copy())
        ### Grados de libertad en elemento 1
        grados_el_1 = VGroup(*n_1_gdl.copy(), *n_2_gdl.copy())
        label_etiquetas_grados_el_1 = VGroup(*n_1_labels_gdl.copy(), *n_2_labels_gdl.copy())
        label_etiquetas_grados_el_1[0].next_to(grados_el_1[0], UP, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_1[1].next_to(grados_el_1[1], DR, buff=-0.4).scale(0.5)
        label_etiquetas_grados_el_1[2].next_to(grados_el_1[2], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_1[3].next_to(grados_el_1[3], UR, buff=-0.25).scale(0.5)
        # grados_el_1 = VGroup(gdl_y_1.copy(), gdl_eje_z_1.copy(), gdl_y_2.copy(), gdl_eje_z_2.copy())
        # label_etiquetas_grados_el_1 = VGroup(label_y_1.copy(), label_eje_z_1.copy(), label_y_2.copy(),
        #                                      label_eje_z_2.copy())
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
        # vector_desplazamientos_el_1_modificado = Matrix(
        #     [["v_{1}=0"], [r"\phi_{1}=0"], ["v_{2}=0"], [r"\phi_{2}"]],
        #     left_bracket=r"\{",  # Llave izquierda
        #     right_bracket=r"\}",  # Llave derecha
        #     element_to_mobject_config={
        #         "tex_to_color_map": {
        #             r"\phi_{2}": BLUE
        #         }
        #     }
        # )
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
        f_2_0 = elemento_carga(n_2.punto, mg.ejes, longitud=1, saliente=False, ang=90)
        label_f_2_0 = MathTex(str(abs(e_2._fuerzas_i[0, 0])) + r"\,kN").next_to(f_2_0, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_2_0 = elemento_momento(n_2.punto, mg.ejes, positivo=True, ang=0)
        label_m_2_0 = MathTex(str(abs(e_2._fuerzas_i[1, 0])) + r"\,kN\cdot m").next_to(m_2_0, UP, buff=0.0).scale(
            0.5).shift(
            LEFT * 0.7)
        f_3_0 = elemento_carga(n_3.punto, mg.ejes, longitud=1, saliente=False, ang=90)
        label_f_3_0 = MathTex(str(abs(e_2._fuerzas_j[0, 0])) + r"\,kN").next_to(f_3_0, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_3_0 = elemento_momento(n_3.punto, mg.ejes, positivo=True, ang=0)
        label_m_3_0 = MathTex(str(abs(e_2._fuerzas_j[1, 0])) + r"\,kN\cdot m").next_to(m_3_0, UP, buff=0.0).scale(
            0.5).shift(
            LEFT * 0.7)
        ### Cargas en elemento 2
        cargas_eq_2 = VGroup(f_2_0.copy(), m_2_0.copy(), f_3_0.copy(), m_3_0.copy())
        label_cargas_eq_2 = VGroup(label_f_2_0.copy(), label_m_2_0.copy(), label_f_3_0.copy(), label_m_3_0.copy())
        ### Grados de libertad en elemento 2
        grados_el_2 = VGroup(*n_2_gdl.copy(), *n_3_gdl.copy())
        label_etiquetas_grados_el_2 = VGroup(*n_2_labels_gdl.copy(), *n_3_labels_gdl.copy())
        label_etiquetas_grados_el_2[0].next_to(grados_el_2[0], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_2[1].next_to(grados_el_2[1], UL, buff=-0.15).scale(0.5)
        label_etiquetas_grados_el_2[2].next_to(grados_el_2[2], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_2[3].next_to(grados_el_2[3], UR, buff=-0.25).scale(0.5)
        f_internas_elemento_1 = mg.elemento_fuerza_interna_viga(e_1, mostrar_valores=True)
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
        # vector_desplazamientos_el_2_modificado = Matrix(
        #     [["v_{2}=0"], [r"\phi_{2}"], ["v_{3}=0"], [r"\phi_{3}"]],
        #     left_bracket=r"\{",  # Llave izquierda
        #     right_bracket=r"\}",  # Llave derecha
        #     element_to_mobject_config={
        #         "tex_to_color_map": {
        #             r"\phi_{2}": BLUE,
        #             r"\phi_{3}": BLUE
        #         }
        #     }
        # )
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
        ecuacion_local_viga_3 = ecuacion_local_viga.copy()
        matriz_k_3 = ecuacion_vector_fuerza_viga(3, 3, 4)
        ### Cargas nodales equivalentes
        # Ninguna
        ### Cargas en elemento 3
        # Ninguna
        ### Grados de libertad en elemento 3
        grados_el_3 = VGroup(*n_3_gdl.copy(), *n_4_gdl.copy())
        label_etiquetas_grados_el_3 = VGroup(*n_3_labels_gdl.copy(), *n_4_labels_gdl.copy())
        label_etiquetas_grados_el_3[0].next_to(grados_el_3[0], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_3[1].next_to(grados_el_3[1], UR, buff=-0.25).scale(0.5)
        label_etiquetas_grados_el_3[2].next_to(grados_el_3[2], UP, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_3[3].next_to(grados_el_3[3], DOWN, buff=0.0).scale(0.5)

        f_internas_elemento_2 = mg.elemento_fuerza_interna_viga(e_2, unidades=['', ''])
        # grados_el_3 = VGroup(gdl_y_3.copy(), gdl_eje_z_3.copy(), gdl_y_4.copy(), gdl_eje_z_4.copy())
        # label_etiquetas_grados_el_3 = VGroup(label_y_3.copy(), label_eje_z_3.copy(), label_y_4.copy(),
        #                                      label_eje_z_4.copy())
        ### Escena elemento 3
        escena_elemento_3 = VGroup(elementos[2], nodos[2:4], soportes[2:4], label_elementos[2], label_nodos[2:4])
        factor_matrix_rigidez_3_1 = MathTex(r'\dfrac{EI}{125}')
        factor_matrix_rigidez_3_2 = MathTex('EI')
        factor_matrix_rigidez_3_3 = factor_matrix_rigidez_3_2.copy()
        factor_matrix_rigidez_3_4 = factor_matrix_rigidez_3_2.copy()
        matrix_rigidez_3_1 = Matrix(
            [['12', '30', '-12', '30'],
             ['30', '100', '-30', '50'],
             ['-12', '-30', '12', '-30'],
             ['63', '50', '-30', '100']]
        )
        # matrix_rigidez_3_2 = Matrix(
        #     [['0.012', '0.06', '-0.012', '0.06'],
        #      ['0.06', '0.4', '-0.06', '0.2'],
        #      ['-0.012', '-0.06', '0.012', '-0.06'],
        #      ['0.06', '0.2', '-0.060', '0.4']],
        #     h_buff=1.8
        # )
        matrix_rigidez_3_2 = ecuacion_array_a_matriz(e_3.get_matriz_rigidez(), h_buff=1.8)
        matrix_rigidez_3_3 = matrix_rigidez_3_2.copy()
        matrix_rigidez_3_4 = matrix_rigidez_3_2.copy()
        vector_desplazamientos_el_3 = ecuacion_vector_desplazamiento_viga(3, 4)
        # vector_desplazamientos_el_3_modificado = Matrix(
        #     [["v_{3}=0"], [r"\phi_{3}"], ["v_{4}=0"], [r"\phi_{4}=0"]],
        #     left_bracket=r"\{",  # Llave izquierda
        #     right_bracket=r"\}",  # Llave derecha
        #     element_to_mobject_config={
        #         "tex_to_color_map": {
        #             r"\phi_{3}": BLUE
        #         }
        #     }
        # )
        vector_desplazamientos_modificado_3_3 = vector_desplazamientos_el_3_modificado.copy()
        vector_desplazamientos_modificado_3_4 = vector_desplazamientos_el_3_modificado.copy()
        vector_fuerza_nodal_equivalente_viga_3 = ecuacion_array_a_matriz(e_3._obtener_fuerzas(), left_bracket=r"\{",
                                                                         right_bracket=r"\}")
        mr_elemento_3 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez.copy(),
                               matrix_rigidez.copy(),
                               vector_desplazamientos_el_3.copy(), ecuacion_signo_menos().copy(),
                               ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_3.to_edge(DOWN).scale(0.5)
        mr_elemento_3_1 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_1,
                                 matrix_rigidez_3_1, vector_desplazamientos_el_3.copy(), ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_3_1.to_edge(DOWN).scale(0.5)
        mr_elemento_3_2 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_2,
                                 matrix_rigidez_3_2, vector_desplazamientos_el_3.copy(), ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT,
                                                                                                     buff=0.2)
        mr_elemento_3_2.to_edge(DOWN).scale(0.5)
        mr_elemento_3_3 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_3,
                                 matrix_rigidez_3_3, vector_desplazamientos_modificado_3_3,
                                 ecuacion_signo_menos().copy(),
                                 ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT,
                                                                                                     buff=0.2)
        mr_elemento_3_3.to_edge(DOWN).scale(0.5)
        mr_elemento_3_4 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_4,
                                 matrix_rigidez_3_4, vector_desplazamientos_modificado_3_4,
                                 ecuacion_signo_menos().copy(),
                                 vector_fuerza_nodal_equivalente_viga_3).arrange(RIGHT,
                                                                                 buff=0.2)
        mr_elemento_3_4.to_edge(DOWN).scale(0.5)
        f_internas_elemento_3 = mg.elemento_fuerza_interna_viga(e_3, unidades=['', ''])
        ## Elementos intermedios
        # sum_1 = e_1+e_2+e_3
        # matrix_rigidez_sum_1 = ecuacion_array_a_matriz(sum_1.get_matriz_rigidez(), h_buff=1.8).scale(0.5)
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
        self.play(Create(mg.ejes), run_time=2)
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
                  ReplacementTransform(label_etiquetas_grados_el_1[0], mr_elemento_1_3[4].get_entries()[0]),
                  ReplacementTransform(label_etiquetas_grados_el_1[1], mr_elemento_1_3[4].get_entries()[1]),
                  ReplacementTransform(label_etiquetas_grados_el_1[2], mr_elemento_1_3[4].get_entries()[2]),
                  ReplacementTransform(label_etiquetas_grados_el_1[3], mr_elemento_1_3[4].get_entries()[3]),
                  Unwrite(grados_el_1), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(cargas[0:2], VGroup(cargas_eq_1, label_cargas_eq_1)), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(mr_elemento_1_3[6].get_brackets(), mr_elemento_1_4[6].get_brackets()),
                  ReplacementTransform(mr_elemento_1_3[0:6], mr_elemento_1_4[0:6]),
                  FadeOut(mr_elemento_1_3[6].get_entries()),
                  ReplacementTransform(label_cargas_eq_1[0], mr_elemento_1_4[6].get_entries()[0]),
                  ReplacementTransform(label_cargas_eq_1[1], mr_elemento_1_4[6].get_entries()[1]),
                  ReplacementTransform(label_cargas_eq_1[2], mr_elemento_1_4[6].get_entries()[2]),
                  ReplacementTransform(label_cargas_eq_1[3], mr_elemento_1_4[6].get_entries()[3]),
                  Unwrite(cargas_eq_1), run_time=2)
        self.wait(5)
        self.play(FadeIn(f_internas_elemento_1))
        self.wait(2)
        self.play(FadeOut(f_internas_elemento_1))
        self.play(FadeOut(elementos[0], nodos[0:2], label_elementos[0], label_nodos[0:2]), FadeOut(mr_elemento_1_4))
        ## Análisis Elemento 2
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
                  ReplacementTransform(label_etiquetas_grados_el_2[0], mr_elemento_2_3[4].get_entries()[0]),
                  ReplacementTransform(label_etiquetas_grados_el_2[1], mr_elemento_2_3[4].get_entries()[1]),
                  ReplacementTransform(label_etiquetas_grados_el_2[2], mr_elemento_2_3[4].get_entries()[2]),
                  ReplacementTransform(label_etiquetas_grados_el_2[3], mr_elemento_2_3[4].get_entries()[3]),
                  Unwrite(grados_el_2), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(cargas[2:5], VGroup(cargas_eq_2, label_cargas_eq_2)), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(mr_elemento_2_3[6].get_brackets(), mr_elemento_2_4[6].get_brackets()),
                  ReplacementTransform(mr_elemento_2_3[0:6], mr_elemento_2_4[0:6]),
                  FadeOut(mr_elemento_2_3[6].get_entries()),
                  ReplacementTransform(label_cargas_eq_2[0], mr_elemento_2_4[6].get_entries()[0]),
                  ReplacementTransform(label_cargas_eq_2[1], mr_elemento_2_4[6].get_entries()[1]),
                  ReplacementTransform(label_cargas_eq_2[2], mr_elemento_2_4[6].get_entries()[2]),
                  ReplacementTransform(label_cargas_eq_2[3], mr_elemento_2_4[6].get_entries()[3]),
                  Unwrite(cargas_eq_2), run_time=2)
        self.wait(5)
        self.play(FadeIn(f_internas_elemento_2))
        self.wait(2)
        self.play(FadeOut(f_internas_elemento_2))
        self.play(FadeOut(elementos[1], nodos[1:3], label_elementos[1], label_nodos[1:3]), FadeOut(mr_elemento_2_4))
        ## Análisis Elemento 3
        self.play(FadeIn(escena_elemento_3), run_time=2)
        self.wait(1)
        self.play(Write(ecuacion_local_viga_3), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_local_viga_3, mr_elemento_3), run_time=2)
        self.play(ReplacementTransform(mr_elemento_3, mr_elemento_3_1), run_time=2)
        self.play(ReplacementTransform(mr_elemento_3_1, mr_elemento_3_2), run_time=2)
        self.wait(2)
        self.play(FadeOut(soportes[2:4]), run_time=2)
        self.play(FadeIn(grados_el_3), run_time=2)
        self.play(Write(label_etiquetas_grados_el_3), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(mr_elemento_3_2[4].get_brackets(), mr_elemento_3_3[4].get_brackets()),
                  ReplacementTransform(mr_elemento_3_2[0:4], mr_elemento_3_3[0:4]),
                  ReplacementTransform(mr_elemento_3_2[5:7], mr_elemento_3_3[5:7]),
                  FadeOut(mr_elemento_3_2[4].get_entries()),
                  ReplacementTransform(label_etiquetas_grados_el_3[0], mr_elemento_3_3[4].get_entries()[0]),
                  ReplacementTransform(label_etiquetas_grados_el_3[1], mr_elemento_3_3[4].get_entries()[1]),
                  ReplacementTransform(label_etiquetas_grados_el_3[2], mr_elemento_3_3[4].get_entries()[2]),
                  ReplacementTransform(label_etiquetas_grados_el_3[3], mr_elemento_3_3[4].get_entries()[3]),
                  Unwrite(grados_el_3), run_time=2)
        self.wait(1)
        f_0_0 = MathTex('0').move_to(mr_elemento_3_4[6].get_entries()[0]).scale(0.5)
        f_0_1 = MathTex('0').move_to(mr_elemento_3_4[6].get_entries()[1]).scale(0.5)
        f_0_2 = MathTex('0').move_to(mr_elemento_3_4[6].get_entries()[2]).scale(0.5)
        f_0_3 = MathTex('0').move_to(mr_elemento_3_4[6].get_entries()[3]).scale(0.5)
        self.play(ReplacementTransform(mr_elemento_3_3[6].get_brackets(), mr_elemento_3_4[6].get_brackets()),
                  ReplacementTransform(mr_elemento_3_3[0:6], mr_elemento_3_4[0:6]),
                  FadeOut(mr_elemento_3_3[6].get_entries()),
                  ReplacementTransform(f_0_0, mr_elemento_3_4[6].get_entries()[0]),
                  ReplacementTransform(f_0_1, mr_elemento_3_4[6].get_entries()[1]),
                  ReplacementTransform(f_0_2, mr_elemento_3_4[6].get_entries()[2]),
                  ReplacementTransform(f_0_3, mr_elemento_3_4[6].get_entries()[3]), run_time=2)
        self.wait(5)
        self.play(FadeIn(f_internas_elemento_3))
        self.wait(2)
        self.play(FadeOut(f_internas_elemento_3))
        self.play(FadeOut(elementos[2], nodos[2:4], label_elementos[2], label_nodos[2:4]), FadeOut(mr_elemento_3_4),
                  FadeOut(mg.ejes))
        self.wait(2)
        m_1 = mr_elemento_1_4.copy()
        m_2 = mr_elemento_2_4.copy()
        m_3 = mr_elemento_3_4.copy()
        self.play(FadeIn(m_1.to_edge(UP)), FadeIn(m_2.move_to(ORIGIN)), FadeIn(m_3.to_edge(DOWN)))
        self.wait(2)
        self.play(
            ReplacementTransform(VGroup(m_1[0].get_brackets()[0], m_2[0].get_brackets()[0], m_3[0].get_brackets()[0]),
                                 matriz_global[0].get_brackets()[0]),
            ReplacementTransform(VGroup(m_1[0].get_brackets()[1], m_2[0].get_brackets()[1], m_3[0].get_brackets()[1]),
                                 matriz_global[0].get_brackets()[1]),
            runtime=4)
        self.play(
            ReplacementTransform(m_1[0].get_entries()[:2], matriz_global[0].get_entries()[:2]),
            ReplacementTransform(VGroup(m_1[0].get_entries()[2:], m_2[0].get_entries()[:2]),
                                 matriz_global[0].get_entries()[2:4]),
            ReplacementTransform(VGroup(m_2[0].get_entries()[2:], m_3[0].get_entries()[:2]),
                                 matriz_global[0].get_entries()[4:6]),
            ReplacementTransform(m_3[0].get_entries()[2:], matriz_global[0].get_entries()[6:]),
            runtime=4)
        self.play(
            ReplacementTransform(VGroup(m_1[1], m_2[1], m_3[1]), matriz_global[1]),
            ReplacementTransform(VGroup(m_1[2], m_2[2], m_3[2]), matriz_global[2]),
            runtime=4)
        self.play(
            ReplacementTransform(VGroup(m_1[3].get_brackets()[0], m_2[3].get_brackets()[0], m_3[3].get_brackets()[0]),
                                 matriz_global[3].get_brackets()[0]),
            ReplacementTransform(VGroup(m_1[3].get_brackets()[1], m_2[3].get_brackets()[1], m_3[3].get_brackets()[1]),
                                 matriz_global[3].get_brackets()[1]),
            m_1[4:].animate.next_to(matriz_global[3], RIGHT, buff=0.5).align_to(m_1[4:], UP),
            m_2[4:].animate.next_to(matriz_global[3], RIGHT, buff=0.5).align_to(m_2[4:], UP),
            m_3[4:].animate.next_to(matriz_global[3], RIGHT, buff=0.5).align_to(m_3[4:], UP),
            runtime=4)
        self.play(
            ReplacementTransform(m_1[3].get_entries()[0:4], matriz_global[3].get_entries()[0:4]),
            ReplacementTransform(m_1[3].get_entries()[4:8], matriz_global[3].get_entries()[8:12]),
            ReplacementTransform(m_1[3].get_entries()[8:10], matriz_global[3].get_entries()[16:18]),
            ReplacementTransform(m_1[3].get_entries()[12:14], matriz_global[3].get_entries()[24:26]),
            ReplacementTransform(
                VGroup(m_1[3].get_entries()[10:12], m_1[3].get_entries()[14:16], m_2[3].get_entries()[:2],
                       m_2[3].get_entries()[4:6]),
                VGroup(matriz_global[3].get_entries()[18:20], matriz_global[3].get_entries()[26:28])),
            ReplacementTransform(m_2[3].get_entries()[2:4], matriz_global[3].get_entries()[20:22]),
            ReplacementTransform(m_2[3].get_entries()[6:8], matriz_global[3].get_entries()[28:30]),
            ReplacementTransform(m_2[3].get_entries()[8:10], matriz_global[3].get_entries()[34:36]),
            ReplacementTransform(m_2[3].get_entries()[12:14], matriz_global[3].get_entries()[42:44]),
            ReplacementTransform(
                VGroup(m_2[3].get_entries()[10:12], m_2[3].get_entries()[14:16], m_3[3].get_entries()[:2],
                       m_3[3].get_entries()[4:6]),
                VGroup(matriz_global[3].get_entries()[36:38], matriz_global[3].get_entries()[44:46])),
            ReplacementTransform(m_3[3].get_entries()[2:4], matriz_global[3].get_entries()[38:40]),
            ReplacementTransform(m_3[3].get_entries()[6:8], matriz_global[3].get_entries()[46:48]),
            ReplacementTransform(m_3[3].get_entries()[8:12], matriz_global[3].get_entries()[52:56]),
            ReplacementTransform(m_3[3].get_entries()[12:16], matriz_global[3].get_entries()[60:64]),
            runtime=4)
        self.play(
            FadeIn(matriz_global[3].get_entries()[4:8]),
            FadeIn(matriz_global[3].get_entries()[12:16]),
            FadeIn(matriz_global[3].get_entries()[22:24]),
            FadeIn(matriz_global[3].get_entries()[30:32]),
            FadeIn(matriz_global[3].get_entries()[32:34]),
            FadeIn(matriz_global[3].get_entries()[40:42]),
            FadeIn(matriz_global[3].get_entries()[48:52]),
            FadeIn(matriz_global[3].get_entries()[56:60]),
            runtime=4)
        self.play(
            ReplacementTransform(VGroup(m_1[4].get_brackets()[0], m_2[4].get_brackets()[0], m_3[4].get_brackets()[0]),
                                 matriz_global[4].get_brackets()[0]),
            ReplacementTransform(VGroup(m_1[4].get_brackets()[1], m_2[4].get_brackets()[1], m_3[4].get_brackets()[1]),
                                 matriz_global[4].get_brackets()[1]),
            ReplacementTransform(m_1[4].get_entries()[:2], matriz_global[4].get_entries()[:2]),
            ReplacementTransform(VGroup(m_1[4].get_entries()[2:], m_2[4].get_entries()[:2]),
                                 matriz_global[4].get_entries()[2:4]),
            ReplacementTransform(VGroup(m_2[4].get_entries()[2:], m_3[4].get_entries()[:2]),
                                 matriz_global[4].get_entries()[4:6]),
            ReplacementTransform(m_3[4].get_entries()[2:], matriz_global[4].get_entries()[6:]),
            runtime=4)
        self.play(
            ReplacementTransform(VGroup(m_1[6].get_brackets()[0], m_2[6].get_brackets()[0], m_3[6].get_brackets()[0]),
                                 matriz_global[6].get_brackets()[0]),
            ReplacementTransform(VGroup(m_1[6].get_brackets()[1], m_2[6].get_brackets()[1], m_3[6].get_brackets()[1]),
                                 matriz_global[6].get_brackets()[1]),
            ReplacementTransform(m_1[6].get_entries()[:2], matriz_global[6].get_entries()[:2]),
            ReplacementTransform(VGroup(m_1[6].get_entries()[2:], m_2[6].get_entries()[:2]),
                                 matriz_global[6].get_entries()[2:4]),
            ReplacementTransform(VGroup(m_2[6].get_entries()[2:], m_3[6].get_entries()[:2]),
                                 matriz_global[6].get_entries()[4:6]),
            ReplacementTransform(m_3[6].get_entries()[2:], matriz_global[6].get_entries()[6:]),
            ReplacementTransform(VGroup(m_1[5], m_2[5], m_3[5]), matriz_global[5]),
            runtime=4)
        # self.play(FadeOut(mr_elemento_1_4[:2]),FadeOut(mr_elemento_2_4[:2]),FadeOut(mr_elemento_3_4[:2]))
        # self.wait(2)
        # self.play(FadeOut(mr_elemento_1_4[2:]), FadeOut(mr_elemento_2_4[2:]), FadeOut(mr_elemento_3_4[2:]))
        # self.wait(2)
        # self.play(FadeIn(matriz_global))
        self.wait(5)
        items_reducida = [3, 5]
        elementos_reducida = list()
        elementos_no_reducida = list()
        for f in items_reducida:
            for c, elem in enumerate(matriz_global[3].get_rows()[f]):
                if c in items_reducida:
                    elementos_reducida.append(elem)
                else:
                    elementos_no_reducida.append(elem)
        self.play(ReplacementTransform(matriz_global[0].get_brackets(), matriz_global_reducida[0].get_brackets()),
                  ReplacementTransform(matriz_global[3].get_brackets(), matriz_global_reducida[3].get_brackets()),
                  ReplacementTransform(matriz_global[4].get_brackets(), matriz_global_reducida[4].get_brackets()),
                  ReplacementTransform(matriz_global[6].get_brackets(), matriz_global_reducida[6].get_brackets()),
                  FadeOut(matriz_global[0].get_rows()[:3], matriz_global[3].get_rows()[:3],
                          matriz_global[4].get_rows()[:3], matriz_global[6].get_rows()[:3]),
                  FadeOut(matriz_global[0].get_rows()[4], matriz_global[3].get_rows()[4],
                          matriz_global[4].get_rows()[4],
                          matriz_global[6].get_rows()[4]),
                  FadeOut(matriz_global[0].get_rows()[6:], matriz_global[3].get_rows()[6:],
                          matriz_global[4].get_rows()[6:],
                          matriz_global[6].get_rows()[6:]),
                  *[FadeOut(elem) for elem in elementos_no_reducida],
                  ReplacementTransform(matriz_global[1], matriz_global_reducida[1]),
                  ReplacementTransform(matriz_global[2], matriz_global_reducida[2]),
                  ReplacementTransform(matriz_global[5], matriz_global_reducida[5]),
                  ReplacementTransform(matriz_global[0].get_entries()[3], matriz_global_reducida[0].get_entries()[0]),
                  ReplacementTransform(matriz_global[0].get_entries()[5], matriz_global_reducida[0].get_entries()[1]),
                  ReplacementTransform(elementos_reducida[0], matriz_global_reducida[3].get_entries()[0]),
                  ReplacementTransform(elementos_reducida[1], matriz_global_reducida[3].get_entries()[1]),
                  ReplacementTransform(elementos_reducida[2], matriz_global_reducida[3].get_entries()[2]),
                  ReplacementTransform(elementos_reducida[3], matriz_global_reducida[3].get_entries()[3]),
                  ReplacementTransform(matriz_global[4].get_entries()[3], matriz_global_reducida[4].get_entries()[0]),
                  ReplacementTransform(matriz_global[4].get_entries()[5], matriz_global_reducida[4].get_entries()[1]),
                  ReplacementTransform(matriz_global[6].get_entries()[3], matriz_global_reducida[6].get_entries()[0]),
                  ReplacementTransform(matriz_global[6].get_entries()[5], matriz_global_reducida[6].get_entries()[1]),
                  run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(matriz_global_reducida[6], matriz_global_reducida_final[0]),
                  ReplacementTransform(matriz_global_reducida[1], matriz_global_reducida_final[1]),
                  ReplacementTransform(matriz_global_reducida[2], matriz_global_reducida_final[2]),
                  ReplacementTransform(matriz_global_reducida[3], matriz_global_reducida_final[3]),
                  ReplacementTransform(matriz_global_reducida[4], matriz_global_reducida_final[4]),
                  FadeOut(matriz_global_reducida[0], matriz_global_reducida[5]), run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(matriz_global_reducida_final[3], matriz_global_reducida_final_2[1][0]),
                  ReplacementTransform(matriz_global_reducida_final[0], matriz_global_reducida_final_2[2]),
                  ReplacementTransform(matriz_global_reducida_final[2], matriz_global_reducida_final_2[0]),
                  ReplacementTransform(matriz_global_reducida_final[1], matriz_global_reducida_final_2[3]),
                  ReplacementTransform(matriz_global_reducida_final[4], matriz_global_reducida_final_2[4]),
                  FadeIn(matriz_global_reducida_final_2[1][1]), run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(matriz_global_reducida_final_2[1][0].get_brackets(),
                                       matriz_global_reducida_final_3[1].get_brackets()),
                  ReplacementTransform(matriz_global_reducida_final_2[1][0].get_entries(),
                                       matriz_global_reducida_final_3[1].get_entries()),
                  ReplacementTransform(matriz_global_reducida_final_2[0], matriz_global_reducida_final_3[0]),
                  ReplacementTransform(matriz_global_reducida_final_2[2], matriz_global_reducida_final_3[2]),
                  ReplacementTransform(matriz_global_reducida_final_2[3], matriz_global_reducida_final_3[3]),
                  ReplacementTransform(matriz_global_reducida_final_2[4], matriz_global_reducida_final_3[4]),

                  FadeOut(matriz_global_reducida_final_2[1][1]), run_time=4)
        self.wait(2)
        # self.play(ReplacementTransform(matriz_global_reducida_final_3[1].get_brackets(),
        #                                matriz_global_reducida_final_4[1].get_brackets()),
        #           ReplacementTransform(matriz_global_reducida_final_3[1].get_entries(),
        #                                matriz_global_reducida_final_4[1].get_entries()),
        #           ReplacementTransform(matriz_global_reducida_final_3[0], matriz_global_reducida_final_4[0]),
        #           ReplacementTransform(matriz_global_reducida_final_3[3], matriz_global_reducida_final_4[2]),
        #           ReplacementTransform(matriz_global_reducida_final_3[4], matriz_global_reducida_final_4[3]),
        #           FadeOut(matriz_global_reducida_final_3[2]),
        #           run_time=4)
        self.play(ReplacementTransform(VGroup(matriz_global_reducida_final_3[1].get_entries(), matriz_global_reducida_final_3[2].get_entries()),
                                       matriz_global_reducida_final_4[1].get_entries()),
                  ReplacementTransform(matriz_global_reducida_final_3[1].get_brackets()[0],
                                       matriz_global_reducida_final_4[1].get_brackets()[0]),
                  ReplacementTransform(matriz_global_reducida_final_3[2].get_brackets()[1],
                                       matriz_global_reducida_final_4[1].get_brackets()[1]),
                  FadeOut(matriz_global_reducida_final_3[1].get_brackets()[1]),
                  FadeOut(matriz_global_reducida_final_3[2].get_brackets()[0]),

                  ReplacementTransform(matriz_global_reducida_final_3[0], matriz_global_reducida_final_4[0]),
                  ReplacementTransform(matriz_global_reducida_final_3[3], matriz_global_reducida_final_4[2]),
                  ReplacementTransform(matriz_global_reducida_final_3[4], matriz_global_reducida_final_4[3]),

                  # FadeOut(matriz_global_reducida_final_3[2]),
                  run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(matriz_global_reducida_final_4[1].get_entries()[0], sol_1[2]),
                  ReplacementTransform(matriz_global_reducida_final_4[1].get_entries()[1], sol_2[2]),
                  ReplacementTransform(matriz_global_reducida_final_4[2], VGroup(sol_1[1], sol_2[1])),
                  ReplacementTransform(matriz_global_reducida_final_4[3].get_entries()[0], sol_1[0]),
                  ReplacementTransform(matriz_global_reducida_final_4[3].get_entries()[1], sol_2[0]),
                  FadeOut(matriz_global_reducida_final_4[1].get_brackets()),
                  FadeOut(matriz_global_reducida_final_4[3].get_brackets()),
                  FadeOut(matriz_global_reducida_final_4[0]),
                  run_time=4)
        self.wait(2)
        self.play(FadeOut(sol_1), FadeOut(sol_2))
        self.wait(2)
        self.play(FadeIn(matriz_global_final_2))
        self.wait(2)
        self.play(ReplacementTransform(VGroup(matriz_global_final_2[0:2]), VGroup(matriz_global_final_3[0:2])),
                  ReplacementTransform(
                      VGroup(matriz_global_final_2[3].get_entries(), matriz_global_final_2[4].get_entries()),
                      VGroup(matriz_global_final_3[2].get_entries())),
                  # ReplacementTransform(VGroup(matriz_global_final_2[2:5]), VGroup(matriz_global_final_3[2])),
                  ReplacementTransform(matriz_global_final_2[3].get_brackets()[0],
                                       matriz_global_final_3[2].get_brackets()[0]),
                  ReplacementTransform(matriz_global_final_2[4].get_brackets()[1],
                                       matriz_global_final_3[2].get_brackets()[1]),
                  FadeOut(matriz_global_final_2[3].get_brackets()[1]),
                  FadeOut(matriz_global_final_2[4].get_brackets()[0]),
                  FadeOut(matriz_global_final_2[2]),
                  ReplacementTransform(VGroup(matriz_global_final_2[5:7]), VGroup(matriz_global_final_3[3:5])),
                  # FadeOut(matriz_global_final_2),
                  run_time=4)
        self.wait(2)
        # self.play(ReplacementTransform(VGroup(matriz_global_final_3[0:2]), VGroup(matriz_global_final_4[0:2])),
        #           ReplacementTransform(VGroup(matriz_global_final_3[2:5]), VGroup(matriz_global_final_4[2])),
        #           run_time=4)
        self.play(ReplacementTransform(VGroup(matriz_global_final_3[0:2]), VGroup(matriz_global_final_4[0:2])),
                  ReplacementTransform(matriz_global_final_3[2].get_brackets()[0],
                                       matriz_global_final_4[2].get_brackets()[0]),
                  ReplacementTransform(matriz_global_final_3[4].get_brackets()[1],
                                       matriz_global_final_4[2].get_brackets()[1]),

                  ReplacementTransform(
                      VGroup(matriz_global_final_3[2].get_entries(), matriz_global_final_3[4].get_entries()),
                      VGroup(matriz_global_final_4[2].get_entries())),
                  FadeOut(matriz_global_final_3[3]),
                  FadeOut(matriz_global_final_3[2].get_brackets()[1]),
                  FadeOut(matriz_global_final_3[4].get_brackets()[0]),
                  run_time=4)
        self.wait(2)
        self.play(FadeOut(matriz_global_final_4))
        self.play(FadeIn(matriz_global_final))
        self.wait(5)
