from manim import *
import numpy as np
import sympy as sp
from biblioteca import *
from mnspy import Nodo, Viga, Resorte


class EjemploVigasAnimacion(Scene):
    def construct(self):
        # Solución del ejercicio con mnspy
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
        ## Se guarda los objetos antes de la solución en mnspy
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
        ### Grados de libertad
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
        ## Se soluciona por mnspy
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
        cargas_puntuales = mg.get_cargas_puntuales(longitud=2.0)
        cargas_distribuidas = mg.get_cargas_distribuidas(longitud=1.3)
        cargas = cargas_puntuales + cargas_distribuidas
        cargas_e_1 = cargas[0:2].copy()
        cargas_e_2 = cargas[2:5].copy()

        ############
        nodos, label_nodos, soportes = mg.get_nodos_y_soportes()
        ############
        elementos, label_elementos = mg.get_elementos()
        ############
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
        ############
        enunciado = Tex(
            r"Determine las reacciones y las fuerzas en los extremos\\",
            r"de los elementos de la viga continua de tres vanos mostrada\\",
            r"en la Figura utilizando el método de rigidez matricial. $EI$= cte.",
            tex_environment="flushleft",  # Esto alinea el texto a la izquierda
            font_size=36
        ).to_edge(UP + LEFT)
        ############
        viga = elemento_viga(0.0, 25.0, 0.25, mg.ejes)
        viga.set_color(GRAY_D)
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
        grados_el_1 = VGroup(*n_1_gdl.copy(), *n_2_gdl.copy()).set_z_index(1)
        label_etiquetas_grados_el_1 = VGroup(*n_1_labels_gdl.copy(), *n_2_labels_gdl.copy())
        label_etiquetas_grados_el_1[0].next_to(grados_el_1[0], UP, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_1[1].next_to(grados_el_1[1], DR, buff=-0.4).scale(0.5)
        label_etiquetas_grados_el_1[2].next_to(grados_el_1[2], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_1[3].next_to(grados_el_1[3], UR, buff=-0.25).scale(0.5)
        #######################################################################################################
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
        mr_elemento_1_4_1 = mr_elemento_1_4.copy()
        mr_elemento_1_4_1[4] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_1, EI_cte=True,
                                                                                     reducida=False).scale(0.5)
        mr_elemento_1_4_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_1_4_2 = mr_elemento_1_4_1.copy()
        mr_elemento_1_4_2.submobjects.pop(2)
        mr_elemento_1_4_2.submobjects.pop(2)
        sol_el_1_1 = np.array(e_1._k.obtener_matriz(False)) @ np.array(e_1._k.obtener_desplazamientos(False))
        sol_el_1_2 = sol_el_1_1 - e_1._obtener_fuerzas()
        mr_elemento_1_4_2[2] = ecuacion_array_a_matriz(sol_el_1_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_1_4_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_1_4_3 = mr_elemento_1_4_2.copy()
        mr_elemento_1_4_3.submobjects.pop(2)
        mr_elemento_1_4_3.submobjects.pop(2)
        mr_elemento_1_4_3[2] = ecuacion_array_a_matriz(sol_el_1_2, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_1_4_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_1_4_4 = mr_elemento_1_4_1.copy()
        mr_elemento_1_4_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_viga(e_1, mostrar_valores=True,
                                                                                  formato='%.8g').scale(0.5)
        mr_elemento_1_4_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        ecuacion_v_e_1 = MathTex(sp.latex(e_1.ecuacion_de_cortante()), color=BLUE_A)
        ecuacion_m_e_1 = MathTex(sp.latex(e_1.ecuacion_de_momento()), color=GREEN_A)
        ec_e_1 = VGroup(ecuacion_v_e_1, ecuacion_m_e_1).arrange(DOWN, buff=0.2).scale(0.5).to_corner(DR, buff=0.5)
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
        grados_el_2 = VGroup(*n_2_gdl.copy(), *n_3_gdl.copy()).set_z_index(1)
        label_etiquetas_grados_el_2 = VGroup(*n_2_labels_gdl.copy(), *n_3_labels_gdl.copy())
        label_etiquetas_grados_el_2[0].next_to(grados_el_2[0], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_2[1].next_to(grados_el_2[1], UL, buff=-0.15).scale(0.5)
        label_etiquetas_grados_el_2[2].next_to(grados_el_2[2], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_2[3].next_to(grados_el_2[3], UR, buff=-0.25).scale(0.5)
        # f_internas_elemento_1 = mg.elemento_fuerza_interna_viga(e_1, mostrar_valores=True)
        f_internas_elemento_1 = mg.elemento_fuerza_interna_viga(e_1, unidades=['', ''])
        #######################################################################################################
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
        mr_elemento_2_4_1 = mr_elemento_2_4.copy()
        mr_elemento_2_4_1[4] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_2, EI_cte=True,
                                                                                     reducida=False).scale(0.5)
        mr_elemento_2_4_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_2_4_2 = mr_elemento_2_4_1.copy()
        mr_elemento_2_4_2.submobjects.pop(2)
        mr_elemento_2_4_2.submobjects.pop(2)
        sol_el_2_1 = np.array(e_2._k.obtener_matriz(False)) @ np.array(e_2._k.obtener_desplazamientos(False))
        sol_el_2_2 = sol_el_2_1 - e_2._obtener_fuerzas()
        mr_elemento_2_4_2[2] = ecuacion_array_a_matriz(sol_el_2_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_2_4_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_2_4_3 = mr_elemento_2_4_2.copy()
        mr_elemento_2_4_3.submobjects.pop(2)
        mr_elemento_2_4_3.submobjects.pop(2)
        mr_elemento_2_4_3[2] = ecuacion_array_a_matriz(sol_el_2_2, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_2_4_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_2_4_4 = mr_elemento_2_4_1.copy()
        mr_elemento_2_4_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_viga(e_1, mostrar_valores=True,
                                                                                  formato='%.8g').scale(0.5)
        mr_elemento_2_4_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        ecuacion_v_e_2 = MathTex(sp.latex(e_2.ecuacion_de_cortante()), color=BLUE_A)
        ecuacion_m_e_2 = MathTex(sp.latex(e_2.ecuacion_de_momento()), color=GREEN_A)
        ec_e_2 = VGroup(ecuacion_v_e_2, ecuacion_m_e_2).arrange(DOWN, buff=0.2).scale(0.5).to_corner(DR, buff=0.5)

        ## Ecuaciones Elemento 3
        ecuacion_local_viga_3 = ecuacion_local_viga.copy()
        matriz_k_3 = ecuacion_vector_fuerza_viga(3, 3, 4)
        ### Cargas nodales equivalentes
        # Ninguna
        ### Cargas en elemento 3
        # Ninguna
        ### Grados de libertad en elemento 3
        grados_el_3 = VGroup(*n_3_gdl.copy(), *n_4_gdl.copy()).set_z_index(1)
        label_etiquetas_grados_el_3 = VGroup(*n_3_labels_gdl.copy(), *n_4_labels_gdl.copy())
        label_etiquetas_grados_el_3[0].next_to(grados_el_3[0], DOWN, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_3[1].next_to(grados_el_3[1], UR, buff=-0.25).scale(0.5)
        label_etiquetas_grados_el_3[2].next_to(grados_el_3[2], UP, buff=0.02).scale(0.5)
        label_etiquetas_grados_el_3[3].next_to(grados_el_3[3], DOWN, buff=0.0).scale(0.5)

        f_internas_elemento_2 = mg.elemento_fuerza_interna_viga(e_2, unidades=['', ''])
        #######################################################################################################
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

        matrix_rigidez_3_2 = ecuacion_array_a_matriz(e_3.get_matriz_rigidez(), h_buff=1.8)
        matrix_rigidez_3_3 = matrix_rigidez_3_2.copy()
        matrix_rigidez_3_4 = matrix_rigidez_3_2.copy()
        vector_desplazamientos_el_3 = ecuacion_vector_desplazamiento_viga(3, 4)
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
        mr_elemento_3_4_1 = mr_elemento_3_4.copy()
        mr_elemento_3_4_1[4] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_3, EI_cte=True,
                                                                                     reducida=False).scale(0.5)
        mr_elemento_3_4_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_3_4_2 = mr_elemento_3_4_1.copy()
        mr_elemento_3_4_2.submobjects.pop(2)
        mr_elemento_3_4_2.submobjects.pop(2)
        sol_el_3_1 = np.array(e_3._k.obtener_matriz(False)) @ np.array(e_3._k.obtener_desplazamientos(False))
        sol_el_3_2 = sol_el_3_1 - e_3._obtener_fuerzas()
        mr_elemento_3_4_2[2] = ecuacion_array_a_matriz(sol_el_3_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_3_4_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_3_4_3 = mr_elemento_3_4_2.copy()
        mr_elemento_3_4_3.submobjects.pop(2)
        mr_elemento_3_4_3.submobjects.pop(2)
        mr_elemento_3_4_3[2] = ecuacion_array_a_matriz(sol_el_3_2, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_3_4_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_3_4_4 = mr_elemento_3_4_1.copy()
        mr_elemento_3_4_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_viga(e_3, mostrar_valores=True,
                                                                                  formato='%.8g').scale(0.5)
        mr_elemento_3_4_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        ecuacion_v_e_3 = MathTex(sp.latex(e_3.ecuacion_de_cortante()), color=BLUE_A)
        ecuacion_m_e_3 = MathTex(sp.latex(e_3.ecuacion_de_momento()), color=GREEN_A)
        ec_e_3 = VGroup(ecuacion_v_e_3, ecuacion_m_e_3).arrange(DOWN, buff=0.2).scale(0.5).to_corner(DR, buff=0.5)

        f_internas_elemento_3 = mg.elemento_fuerza_interna_viga(e_3, unidades=['', ''])
        ## Elementos intermedios
        ## Diagrama viga inicial
        escena_inicial = VGroup(viga, soportes, cargas, cotas)
        escena_inicial.save_state()
        escena_inicial.to_edge(DOWN + LEFT)
        escena = VGroup(nodos, elementos, soportes, label_elementos, label_nodos, cargas, cotas)

        # Animaciones

        tit = titulo("Método de Elementos Finitos", "Análisis de una viga")
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.play(FadeIn(tit[2], shift=UP))  # Sube ligeramente al aparecer
        self.wait(2)
        self.play(FadeOut(tit))

        ## Enunciado
        self.play(Write(enunciado), run_time=5)
        ## Diagrama de la viga
        self.play(FadeIn(escena_inicial), run_time=2)
        self.wait(5)
        self.play(FadeOut(enunciado), run_time=2)
        self.play(Restore(escena_inicial), run_time=2)
        self.wait(5)
        self.play(FadeOut(escena_inicial))
        self.wait(0.5)
        tit = titulo("Discretización de la viga", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(Restore(escena_inicial))
        self.wait(2)
        ## Discretización de la viga
        self.play(Create(mg.ejes), run_time=2)
        self.play(FadeOut(viga), run_time=2)
        self.play(DrawBorderThenFill(nodos), DrawBorderThenFill(elementos), run_time=2)
        self.play(Write(label_nodos), Write(label_elementos), run_time=2)
        etiquetas = [MathTex('Nodo'), MathTex('x[m]'), MathTex('GL[y]'), MathTex(r'GL[\phi]')]
        rows = [[1, 0.0, 'Restringido', 'Restringido'],
                [2, 10.0, 'Restringido', 'Libre'],
                [3, 20.0, 'Restringido', 'Libre'],
                [4, 25.0, 'Restringido', 'Restringido']]
        tab_nodos = elemento_tabla(etiquetas, rows).scale(0.5).to_edge(DOWN, buff=0.5)
        etiquetas = [MathTex('Elemento'), MathTex(r'Nodo_i'), MathTex(r'Nodo_j'), MathTex('L[m]'), MathTex('EI')]
        rows = [[1, 1, 2, 10, 'cte'],
                [2, 2, 3, 10, 'cte'],
                [3, 3, 4, 5, 'cte']]
        tab_elementos = elemento_tabla(etiquetas, rows).scale(0.5).to_edge(DOWN, buff=0.5)
        VGroup(tab_nodos, tab_elementos).arrange(RIGHT, buff=1).to_edge(DOWN, buff=0.5)
        self.play(Create(tab_nodos[1]), Create(tab_nodos[2]), run_time=1)
        self.play(FadeIn(tab_nodos[0].get_rows()))
        self.wait(2)
        self.play(Create(tab_elementos[1]), Create(tab_elementos[2]), run_time=1)
        self.play(FadeIn(tab_elementos[0].get_rows()))
        self.wait(5)
        self.play(FadeOut(tab_nodos, tab_elementos), FadeOut(escena), run_time=2)
        #######################################################################################################
        ## Análisis Elemento 1
        tit = titulo("Matriz de rigidez del elemento 1", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
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
        #######################################################################################################
        ## Análisis Elemento 2
        tit = titulo("Matriz de rigidez del elemento 2", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
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
        #######################################################################################################
        ## Análisis Elemento 3
        tit = titulo("Matriz de rigidez del elemento 3", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
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
        tit = titulo("Matriz de rigidez goblal (Ensamblaje)", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
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
        self.wait(5)
        self.play(FadeOut(matriz_global))
        tit = titulo("Matriz de rigidez goblal reducida", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(matriz_global))
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
        self.play(FadeOut(matriz_global_reducida))
        tit = titulo("Resolución de los desplazamientos desconocidos", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(matriz_global_reducida))

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
        self.play(ReplacementTransform(
            VGroup(matriz_global_reducida_final_3[1].get_entries(), matriz_global_reducida_final_3[2].get_entries()),
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
        tit = titulo("Resolución de las reacciones desconocidas", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
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
        tit = titulo("Matriz global solucionada", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(matriz_global_final))
        self.wait(5)
        self.play(FadeOut(matriz_global_final))
        tit = titulo("Fuerzas internas del elemento 1", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))

        self.play(FadeIn(elementos[0], nodos[0:2], label_elementos[0], label_nodos[0:2]), FadeIn(mr_elemento_1_4),
                  FadeIn(f_internas_elemento_1), FadeIn(cargas_e_1))
        self.play(
            ReplacementTransform(mr_elemento_1_4[0], mr_elemento_1_4_1[0]),
            ReplacementTransform(mr_elemento_1_4[1], mr_elemento_1_4_1[1]),
            ReplacementTransform(mr_elemento_1_4[2], mr_elemento_1_4_1[2]),
            ReplacementTransform(mr_elemento_1_4[3], mr_elemento_1_4_1[3]),
            ReplacementTransform(mr_elemento_1_4[4], mr_elemento_1_4_1[4]),
            ReplacementTransform(mr_elemento_1_4[5], mr_elemento_1_4_1[5]),
            ReplacementTransform(mr_elemento_1_4[6], mr_elemento_1_4_1[6]),
            run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(VGroup(mr_elemento_1_4_1[3].get_entries(), mr_elemento_1_4_1[4].get_entries()),
                                       mr_elemento_1_4_2[2].get_entries()),
                  ReplacementTransform(mr_elemento_1_4_1[3].get_brackets()[0],
                                       mr_elemento_1_4_2[2].get_brackets()[0]),
                  ReplacementTransform(mr_elemento_1_4_1[4].get_brackets()[1],
                                       mr_elemento_1_4_2[2].get_brackets()[1]),
                  ReplacementTransform(mr_elemento_1_4_1[0], mr_elemento_1_4_2[0]),
                  ReplacementTransform(mr_elemento_1_4_1[1], mr_elemento_1_4_2[1]),
                  ReplacementTransform(mr_elemento_1_4_1[5], mr_elemento_1_4_2[3]),
                  ReplacementTransform(mr_elemento_1_4_1[6], mr_elemento_1_4_2[4]),
                  FadeOut(mr_elemento_1_4_1[2]),
                  FadeOut(mr_elemento_1_4_1[3].get_brackets()[1]),
                  FadeOut(mr_elemento_1_4_1[4].get_brackets()[0]),
                  run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(VGroup(mr_elemento_1_4_2[2].get_entries(), mr_elemento_1_4_2[4].get_entries()),
                                       mr_elemento_1_4_3[2].get_entries()),
                  ReplacementTransform(mr_elemento_1_4_2[2].get_brackets()[0],
                                       mr_elemento_1_4_3[2].get_brackets()[0]),
                  ReplacementTransform(mr_elemento_1_4_2[4].get_brackets()[1],
                                       mr_elemento_1_4_3[2].get_brackets()[1]),
                  ReplacementTransform(mr_elemento_1_4_2[0], mr_elemento_1_4_3[0]),
                  ReplacementTransform(mr_elemento_1_4_2[1], mr_elemento_1_4_3[1]),
                  FadeOut(mr_elemento_1_4_2[3]),
                  FadeOut(mr_elemento_1_4_2[2].get_brackets()[1]),
                  FadeOut(mr_elemento_1_4_2[4].get_brackets()[0]),
                  run_time=4)
        self.wait(2)
        self.play(mr_elemento_1_4_3.animate.to_corner(DOWN + LEFT), run_time=4)
        self.wait(2)
        self.play(Write(ecuacion_v_e_1))
        self.wait(2)
        self.play(Write(ecuacion_m_e_1))
        self.wait(2)
        self.play(FadeOut(mr_elemento_1_4_3), FadeOut(ec_e_1),
                  FadeOut(elementos[0], nodos[0:2], label_elementos[0], label_nodos[0:2]),
                  FadeOut(f_internas_elemento_1), FadeOut(cargas_e_1))
        self.wait(2)
        mr_elemento_1_4_4.move_to(ORIGIN)
        self.play(FadeIn(mr_elemento_1_4_4))
        self.wait(2)
        self.play(FadeOut(mr_elemento_1_4_4))
        ####################################
        tit = titulo("Fuerzas internas del elemento 2", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(elementos[1], nodos[1:3], label_elementos[1], label_nodos[1:3]), FadeIn(mr_elemento_2_4),
                  FadeIn(cargas_e_2), FadeIn(f_internas_elemento_2))
        self.play(
            ReplacementTransform(mr_elemento_2_4[0], mr_elemento_2_4_1[0]),
            ReplacementTransform(mr_elemento_2_4[1], mr_elemento_2_4_1[1]),
            ReplacementTransform(mr_elemento_2_4[2], mr_elemento_2_4_1[2]),
            ReplacementTransform(mr_elemento_2_4[3], mr_elemento_2_4_1[3]),
            ReplacementTransform(mr_elemento_2_4[4], mr_elemento_2_4_1[4]),
            ReplacementTransform(mr_elemento_2_4[5], mr_elemento_2_4_1[5]),
            ReplacementTransform(mr_elemento_2_4[6], mr_elemento_2_4_1[6]),
            run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(VGroup(mr_elemento_2_4_1[3].get_entries(), mr_elemento_2_4_1[4].get_entries()),
                                       mr_elemento_2_4_2[2].get_entries()),
                  ReplacementTransform(mr_elemento_2_4_1[3].get_brackets()[0],
                                       mr_elemento_2_4_2[2].get_brackets()[0]),
                  ReplacementTransform(mr_elemento_2_4_1[4].get_brackets()[1],
                                       mr_elemento_2_4_2[2].get_brackets()[1]),
                  ReplacementTransform(mr_elemento_2_4_1[0], mr_elemento_2_4_2[0]),
                  ReplacementTransform(mr_elemento_2_4_1[1], mr_elemento_2_4_2[1]),
                  ReplacementTransform(mr_elemento_2_4_1[5], mr_elemento_2_4_2[3]),
                  ReplacementTransform(mr_elemento_2_4_1[6], mr_elemento_2_4_2[4]),
                  FadeOut(mr_elemento_2_4_1[2]),
                  FadeOut(mr_elemento_2_4_1[3].get_brackets()[1]),
                  FadeOut(mr_elemento_2_4_1[4].get_brackets()[0]),
                  run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(VGroup(mr_elemento_2_4_2[2].get_entries(), mr_elemento_2_4_2[4].get_entries()),
                                       mr_elemento_2_4_3[2].get_entries()),
                  ReplacementTransform(mr_elemento_2_4_2[2].get_brackets()[0],
                                       mr_elemento_2_4_3[2].get_brackets()[0]),
                  ReplacementTransform(mr_elemento_2_4_2[4].get_brackets()[1],
                                       mr_elemento_2_4_3[2].get_brackets()[1]),
                  ReplacementTransform(mr_elemento_2_4_2[0], mr_elemento_2_4_3[0]),
                  ReplacementTransform(mr_elemento_2_4_2[1], mr_elemento_2_4_3[1]),
                  FadeOut(mr_elemento_2_4_2[3]),
                  FadeOut(mr_elemento_2_4_2[2].get_brackets()[1]),
                  FadeOut(mr_elemento_2_4_2[4].get_brackets()[0]),
                  run_time=4)
        self.wait(2)
        self.play(mr_elemento_2_4_3.animate.to_corner(DOWN + LEFT), run_time=4)
        self.wait(2)
        self.play(Write(ecuacion_v_e_2))
        self.wait(2)
        self.play(Write(ecuacion_m_e_2))
        self.wait(2)
        self.play(FadeOut(mr_elemento_2_4_3), FadeOut(ec_e_2),
                  FadeOut(elementos[1], nodos[1:3], label_elementos[1], label_nodos[1:3]),
                  FadeOut(f_internas_elemento_2), FadeOut(cargas_e_2))
        self.wait(2)
        mr_elemento_2_4_4.move_to(ORIGIN)
        self.play(FadeIn(mr_elemento_2_4_4))
        self.wait(2)
        self.play(FadeOut(mr_elemento_2_4_4))
        ####################################
        tit = titulo("Fuerzas internas del elemento 3", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(elementos[2], nodos[2:4], label_elementos[2], label_nodos[2:4]), FadeIn(mr_elemento_3_4),
                  FadeIn(f_internas_elemento_3))
        self.play(
            ReplacementTransform(mr_elemento_3_4[0], mr_elemento_3_4_1[0]),
            ReplacementTransform(mr_elemento_3_4[1], mr_elemento_3_4_1[1]),
            ReplacementTransform(mr_elemento_3_4[2], mr_elemento_3_4_1[2]),
            ReplacementTransform(mr_elemento_3_4[3], mr_elemento_3_4_1[3]),
            ReplacementTransform(mr_elemento_3_4[4], mr_elemento_3_4_1[4]),
            ReplacementTransform(mr_elemento_3_4[5], mr_elemento_3_4_1[5]),
            ReplacementTransform(mr_elemento_3_4[6], mr_elemento_3_4_1[6]),
            run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(VGroup(mr_elemento_3_4_1[3].get_entries(), mr_elemento_3_4_1[4].get_entries()),
                                       mr_elemento_3_4_2[2].get_entries()),
                  ReplacementTransform(mr_elemento_3_4_1[3].get_brackets()[0],
                                       mr_elemento_3_4_2[2].get_brackets()[0]),
                  ReplacementTransform(mr_elemento_3_4_1[4].get_brackets()[1],
                                       mr_elemento_3_4_2[2].get_brackets()[1]),
                  ReplacementTransform(mr_elemento_3_4_1[0], mr_elemento_3_4_2[0]),
                  ReplacementTransform(mr_elemento_3_4_1[1], mr_elemento_3_4_2[1]),
                  ReplacementTransform(mr_elemento_3_4_1[5], mr_elemento_3_4_2[3]),
                  ReplacementTransform(mr_elemento_3_4_1[6], mr_elemento_3_4_2[4]),
                  FadeOut(mr_elemento_3_4_1[2]),
                  FadeOut(mr_elemento_3_4_1[3].get_brackets()[1]),
                  FadeOut(mr_elemento_3_4_1[4].get_brackets()[0]),
                  run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(VGroup(mr_elemento_3_4_2[2].get_entries(), mr_elemento_3_4_2[4].get_entries()),
                                       mr_elemento_3_4_3[2].get_entries()),
                  ReplacementTransform(mr_elemento_3_4_2[2].get_brackets()[0],
                                       mr_elemento_3_4_3[2].get_brackets()[0]),
                  ReplacementTransform(mr_elemento_3_4_2[4].get_brackets()[1],
                                       mr_elemento_3_4_3[2].get_brackets()[1]),
                  ReplacementTransform(mr_elemento_3_4_2[0], mr_elemento_3_4_3[0]),
                  ReplacementTransform(mr_elemento_3_4_2[1], mr_elemento_3_4_3[1]),
                  FadeOut(mr_elemento_3_4_2[3]),
                  FadeOut(mr_elemento_3_4_2[2].get_brackets()[1]),
                  FadeOut(mr_elemento_3_4_2[4].get_brackets()[0]),
                  run_time=4)
        self.wait(2)
        self.play(mr_elemento_3_4_3.animate.to_corner(DOWN + LEFT), run_time=4)
        self.wait(2)
        self.play(Write(ecuacion_v_e_3))
        self.wait(2)
        self.play(Write(ecuacion_m_e_3))
        self.wait(2)
        self.play(FadeOut(mr_elemento_3_4_3), FadeOut(ec_e_3),
                  FadeOut(elementos[2], nodos[2:4], label_elementos[2], label_nodos[2:4]),
                  FadeOut(f_internas_elemento_3))
        self.wait(2)
        mr_elemento_3_4_4.move_to(ORIGIN)
        self.play(FadeIn(mr_elemento_3_4_4))
        self.wait(2)
        self.play(FadeOut(mr_elemento_3_4_4))
        #######################################################################################################
        tit = titulo("Diagrama de cortantes", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        x = sp.Symbol('x')
        v_1 = e_1.ecuacion_de_cortante().rhs.args[0].args[0]
        v_2 = e_1.ecuacion_de_cortante().rhs.args[1].args[0]
        v_3 = e_2.ecuacion_de_cortante().rhs.args[0].args[0]
        v_4 = e_3.ecuacion_de_cortante().rhs.args[0].args[0]
        nuevos_argumentos = []
        for sub_piecewise, condicion_externa in mg.ecuacion_de_momento().rhs.args:
            nuevos_argumentos.extend(sub_piecewise.args)
        m = sp.Piecewise(*nuevos_argumentos)
        m_1 = e_1.ecuacion_de_momento().rhs.args[0].args[0]
        m_2 = e_1.ecuacion_de_momento().rhs.args[1].args[0]
        m_3 = e_2.ecuacion_de_momento().rhs.args[0].args[0]
        m_4 = e_3.ecuacion_de_momento().rhs.args[0].args[0]

        f_v_1 = sp.lambdify(x, v_1, 'numpy')
        f_v_2 = sp.lambdify(x, v_2, 'numpy')
        f_v_3 = sp.lambdify(x, v_3, 'numpy')
        f_v_4 = sp.lambdify(x, v_4, 'numpy')
        f_m = sp.lambdify(x, m, 'numpy')
        f_m_1 = sp.lambdify(x, m_1, 'numpy')
        f_m_2 = sp.lambdify(x, m_2, 'numpy')
        f_m_3 = sp.lambdify(x, m_3, 'numpy')
        f_m_4 = sp.lambdify(x, m_4, 'numpy')

        # 3. Crear los Ejes
        ejes_v = Axes(
            x_range=[0, 26, 5],
            y_range=[-120, 125, 25],
            axis_config={"include_numbers": True, "tip_shape": StealthTip, "font_size": 18, }
        )
        titulos_ejes_v = ejes_v.get_axis_labels(
            x_label=MathTex("x (m)", font_size=20),
            y_label=MathTex("Cortante (kN)", font_size=20)
        ).set_color(BLUE_A)
        # ejes_v.add_coordinates(
        #     x_label="x (m)",
        #     y_label="Cortante (kN)"
        # )
        titulo_v = Text("Diagrama de cortante", font_size=28)
        titulo_v.next_to(ejes_v, UP, buff=0.1)
        ejes_m = Axes(
            x_range=[0, 26, 5],
            y_range=[-180, 140, 25],
            axis_config={"include_numbers": True, "tip_shape": StealthTip, "font_size": 18, }
        )
        titulos_ejes_m = ejes_v.get_axis_labels(
            x_label=MathTex("x (m)", font_size=20),
            y_label=MathTex(r"Momento (kN \cdot m)", font_size=20)
        ).set_color(BLUE_A)
        # ejes_m.add_coordinates(
        #     x_label="x (m)",
        #     y_label=r"Momento (kN \cdot m)"
        # )
        titulo_m = Text("Diagrama de momento", font_size=28)
        titulo_m.next_to(ejes_m, UP, buff=0.1)
        curva_v_1 = ejes_v.plot(f_v_1, x_range=[0, 6], color=BLUE_E)
        curva_v_2 = ejes_v.plot(f_v_2, x_range=[6, 10], color=BLUE_E)
        curva_v_3 = ejes_v.plot(f_v_3, x_range=[10, 20], color=BLUE_E)
        curva_v_4 = ejes_v.plot(f_v_4, x_range=[20, 25], color=BLUE_E)
        label_v_1_1 = MathTex(f'{f_v_1(0):.3g}', color=ORANGE).next_to(ejes_v.c2p(0, f_v_1(0), 0), UP, buff=0.0).shift(
            RIGHT * 0.2).scale(0.35)
        label_v_1_2 = MathTex(f'{f_v_1(6):.3g}', color=ORANGE).next_to(ejes_v.c2p(6, f_v_1(6), 0), UP, buff=0.0).scale(
            0.35)
        label_v_2_1 = MathTex(f'{f_v_2(6):.3g}', color=ORANGE).next_to(ejes_v.c2p(6, f_v_2(6), 0), DOWN,
                                                                       buff=0.0).scale(0.35)
        label_v_2_2 = MathTex(f'{f_v_2(10):.3g}', color=ORANGE).next_to(ejes_v.c2p(10, f_v_2(10), 0), DOWN,
                                                                        buff=0.0).scale(0.35)
        label_v_3_1 = MathTex(f'{f_v_3(10):.3g}', color=ORANGE).next_to(ejes_v.c2p(10, f_v_3(10), 0), UP,
                                                                        buff=0.0).scale(0.35)
        label_v_3_2 = MathTex(f'{f_v_3(20):.3g}', color=ORANGE).next_to(ejes_v.c2p(20, f_v_3(20), 0), DOWN,
                                                                        buff=0.0).scale(0.35)
        label_v_4_1 = MathTex(f'{f_v_4(20):.3g}', color=ORANGE).next_to(ejes_v.c2p(20, f_v_4(20), 0), UP,
                                                                        buff=0.0).scale(0.35)
        label_v_4_2 = MathTex(f'{f_v_4(25):.3g}', color=ORANGE).next_to(ejes_v.c2p(25, f_v_4(25), 0), UP,
                                                                        buff=0.0).scale(0.35)
        curva_m = ejes_m.plot(f_m, x_range=[0, 25, 0.05], color=BLUE_E)
        # curva_m_1 = ejes_m.plot(f_m_1, x_range=[0, 6], color=BLUE_E)
        # curva_m_2 = ejes_m.plot(f_m_2, x_range=[6, 10], color=BLUE_E)
        # curva_m_3 = ejes_m.plot(f_m_3, x_range=[10, 20, 0.1], color=BLUE_E)
        # curva_m_4 = ejes_m.plot(f_m_4, x_range=[20, 25], color=BLUE_E)
        label_m_1_1 = MathTex(f'{f_m_1(0):.3g}', color=ORANGE).next_to(ejes_m.c2p(0, f_m_1(0), 0), DOWN,
                                                                       buff=0.0).shift(
            RIGHT * 0.2).scale(0.35)
        label_m_1_2 = MathTex(f'{f_m_1(6):.3g}', color=ORANGE).next_to(ejes_m.c2p(6, f_m_1(6), 0), UP, buff=0.0).scale(
            0.35)
        # label_m_2_1 = MathTex(f'{f_m_2(6):.3g}', color=ORANGE).next_to(ejes_m.c2p(6, f_m_2(6), 0), DOWN,
        #                                                                buff=0.0).scale(
        #     0.35)
        label_m_2_2 = MathTex(f'{f_m_2(10):.3g}', color=ORANGE).next_to(ejes_m.c2p(10, f_m_2(10), 0), DOWN,
                                                                        buff=0.0).scale(0.35)
        label_m_3_1 = MathTex(f'{f_m_3(15.0956521739130):.3g}', color=ORANGE).next_to(
            ejes_m.c2p(15.0956521739130, f_m_3(15.0956521739130), 0), UP,
            buff=0.0).scale(0.35)
        label_m_3_2 = MathTex(f'{f_m_3(20):.3g}', color=ORANGE).next_to(ejes_m.c2p(20, f_m_3(20), 0), DOWN,
                                                                        buff=0.0).scale(0.35)
        # label_m_4_1 = MathTex(f'{f_m_4(20):.3g}', color=ORANGE).next_to(ejes_m.c2p(20, f_m_4(20), 0), UP,
        #                                                                 buff=0.0).scale(0.35)
        label_m_4_2 = MathTex(f'{f_m_4(25):.3g}', color=ORANGE).next_to(ejes_m.c2p(25, f_m_4(25), 0), UP,
                                                                        buff=0.0).scale(0.35)
        self.play(Create(ejes_v), Write(titulos_ejes_v), Write(titulo_v), run_time=4)
        t_tracker_v = ValueTracker(0)

        def update_area_v_1():
            t = t_tracker_v.get_value()
            if t <= 0:
                return VGroup()
            return ejes_v.get_area(curva_v_1, x_range=(0, min(t, 6)), color=BLUE, opacity=0.3)

        area_1_dinamica_v = always_redraw(update_area_v_1)

        def update_area_v_2():
            t = t_tracker_v.get_value()
            if t <= 6:
                return VGroup()
            return ejes_v.get_area(curva_v_2, x_range=(6, min(t, 10)), color=BLUE, opacity=0.3)

        area_2_dinamica_v = always_redraw(update_area_v_2)

        def update_area_v_3():
            t = t_tracker_v.get_value()
            if t <= 10:
                return VGroup()
            return ejes_v.get_area(curva_v_3, x_range=(10, min(t, 20)), color=BLUE, opacity=0.3)

        area_3_dinamica_v = always_redraw(update_area_v_3)

        def update_area_v_4():
            t = t_tracker_v.get_value()
            if t <= 20:
                return VGroup()
            return ejes_v.get_area(curva_v_4, x_range=(20, min(t, 25)), color=BLUE, opacity=0.3)

        area_4_dinamica_v = always_redraw(update_area_v_4)
        self.add(area_1_dinamica_v, area_2_dinamica_v, area_3_dinamica_v, area_4_dinamica_v)
        self.play(Write(label_v_1_1))
        self.play(t_tracker_v.animate.set_value(6), run_time=4, rate_func=linear)
        self.play(Write(label_v_1_2))
        self.wait(0.5)
        self.play(Write(label_v_2_1))
        self.play(t_tracker_v.animate.set_value(10), run_time=4, rate_func=linear)
        self.play(Write(label_v_2_2))
        self.wait(0.5)
        self.play(Write(label_v_3_1))
        self.play(t_tracker_v.animate.set_value(20), run_time=4, rate_func=linear)
        self.play(Write(label_v_3_2))
        self.wait(0.5)
        self.play(Write(label_v_4_1))
        self.play(t_tracker_v.animate.set_value(25), run_time=4, rate_func=linear)
        self.play(Write(label_v_4_2))
        self.wait(2)
        self.play(
            FadeOut(titulos_ejes_v, titulo_v, ejes_v, label_v_1_1, label_v_1_2, label_v_2_1, label_v_2_2, label_v_3_1,
                    label_v_3_2, label_v_4_1,
                    label_v_4_2, curva_v_1, curva_v_2, curva_v_3, curva_v_4, area_1_dinamica_v, area_2_dinamica_v,
                    area_3_dinamica_v, area_4_dinamica_v))
        tit = titulo("Diagrama de momento", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(Create(ejes_m), Write(titulos_ejes_m), Write(titulo_m), run_time=4)
        t_tracker_m = ValueTracker(0)

        def update_area_m():
            t = t_tracker_m.get_value()
            if t <= 0:
                return VGroup()
            return ejes_m.get_area(curva_m, x_range=(0, min(t, 25)), color=BLUE, opacity=0.3)

        area_dinamica_m = always_redraw(update_area_m)

        # def update_area_m_1():
        #     t = t_tracker_m.get_value()
        #     if t <= 0:
        #         return VGroup()
        #     return ejes_m.get_area(curva_m_1, x_range=(0, min(t, 10)), color=BLUE, opacity=0.3)
        #
        # area_1_dinamica_m = always_redraw(update_area_m_1)
        #
        # def update_area_m_2():
        #     t = t_tracker_m.get_value()
        #     if t <= 10:
        #         return VGroup()
        #     return ejes_m.get_area(curva_m_3, x_range=(10, min(t, 20)), color=BLUE, opacity=0.3)
        #
        # area_2_dinamica_m = always_redraw(update_area_m_2)
        #
        # def update_area_m_3():
        #     t = t_tracker_m.get_value()
        #     if t <= 20:
        #         return VGroup()
        #     return ejes_m.get_area(curva_m_4, x_range=(20, min(t, 25)), color=BLUE, opacity=0.3)
        #
        # area_3_dinamica_m = always_redraw(update_area_m_3)

        # def update_area_m_4():
        #     t = t_tracker_m.get_value()
        #     if t <= 20:
        #         return VGroup()
        #     return ejes_m.get_area(curva_m_4, x_range=(20, min(t, 25)), color=BLUE, opacity=0.3)
        #
        # area_4_dinamica_m = always_redraw(update_area_m_4)
        self.add(area_dinamica_m)
        self.play(Write(label_m_1_1))
        self.play(t_tracker_m.animate.set_value(6), run_time=4, rate_func=linear)
        self.play(Write(label_m_1_2))
        self.wait(0.5)
        # self.play(Write(label_m_2_1))
        self.play(t_tracker_m.animate.set_value(10), run_time=4, rate_func=linear)
        self.play(Write(label_m_2_2))
        self.wait(0.5)
        self.play(t_tracker_m.animate.set_value(15.0956521739130), run_time=4, rate_func=linear)
        self.play(Write(label_m_3_1))
        self.wait(0.5)
        self.play(t_tracker_m.animate.set_value(20), run_time=4, rate_func=linear)
        self.play(Write(label_m_3_2))
        self.wait(0.5)
        # self.play(Write(label_m_4_1))
        self.play(t_tracker_m.animate.set_value(25), run_time=4, rate_func=linear)
        self.play(Write(label_m_4_2))
        self.wait(2)
        self.play(
            FadeOut(titulos_ejes_m, titulo_m, ejes_m, label_m_1_1, label_m_1_2, label_m_2_2, label_m_3_1, label_m_3_2,
                    label_m_4_2, curva_m, area_dinamica_m))


class EjemploResorteAnimacion(Scene):
    def construct(self):
        # Solución del ejercicio con mnspy
        n_1 = Nodo('1', grados_libertad={'x': False})
        n_2 = Nodo('2', grados_libertad={'x': False})
        n_3 = Nodo('3', grados_libertad={'x': True})
        n_4 = Nodo('4', grados_libertad={'x': True})
        #### Creación de los Elementos
        e_1 = Resorte('1', n_1, n_3, k=200)
        e_2 = Resorte('2', n_3, n_4, k=400)
        e_3 = Resorte('3', n_4, n_2, k=600)
        mg = EnsambleAnimacion([e_1, e_2, e_3])
        #### Cargas
        n_4.agregar_fuerza_externa(25000, 'x')
        ## Se guarda los objetos antes de la solución en mnspy
        matriz_global_base = mg.sistema_ecuaciones_matriz_rigidez_global(reducida=False)
        matriz_global = matriz_global_base.copy().scale(0.5).arrange(RIGHT)
        matriz_global_reducida_inicial = mg.sistema_ecuaciones_matriz_rigidez_global(reducida=True)
        matriz_global_reducida = matriz_global_reducida_inicial.copy().scale(0.5).arrange(RIGHT)
        matriz_global_reducida_final = VGroup(matriz_global_reducida_inicial[5].copy(), ecuacion_signo_igual(),
                                              matriz_global_reducida_inicial[2].copy(),
                                              matriz_global_reducida_inicial[3].copy()).scale(0.5).arrange(RIGHT)
        matriz = matriz_global_reducida_inicial[2].copy()
        vec_k_reduc_inverso = ecuacion_array_a_matriz(np.linalg.inv(np.array(mg._union._k.obtener_matriz(True))),
                                                      h_buff=2.8)

        sol = np.linalg.inv(np.array(mg._union._k.obtener_matriz(True))) @ np.array(mg._union._k.obtener_fuerzas(True))
        solucion_reducida = ecuacion_array_a_matriz(sol, formato_num='{x:.8f}', left_bracket=r"\{", right_bracket=r"\}")
        superindice = MathTex("-1").next_to(matriz, RIGHT, aligned_edge=UP, buff=0.1)
        matriz_global_reducida_final_2 = VGroup(VGroup(matriz_global_reducida_inicial[2].copy(), superindice),
                                                matriz_global_reducida_inicial[5].copy(),
                                                ecuacion_signo_igual(), matriz_global_reducida_inicial[3].copy()).scale(
            0.5).arrange(RIGHT)
        matriz_global_reducida_final_3 = VGroup(vec_k_reduc_inverso,
                                                matriz_global_reducida_inicial[5].copy(),
                                                ecuacion_signo_igual(),
                                                matriz_global_reducida_inicial[3].copy()).scale(
            0.5).arrange(RIGHT)
        matriz_global_reducida_final_4 = VGroup(solucion_reducida.copy(), ecuacion_signo_igual(),
                                                matriz_global_reducida_inicial[3].copy()).scale(
            0.5).arrange(RIGHT)

        sol_1 = VGroup(MathTex(r'{u_3}').set_color(BLUE), ecuacion_signo_igual(),
                       MathTex(f'{sol[0][0]:.8f}')).scale(0.5).arrange(RIGHT)
        sol_2 = VGroup(MathTex(r'{u_4}').set_color(BLUE), ecuacion_signo_igual(),
                       MathTex(f'{sol[1][0]:.8f}')).scale(0.5).arrange(RIGHT).next_to(sol_1, DOWN)

        ### Grados de libertad
        n_1_gdl = VGroup(mg.get_grados_libertad(n_1, 'x', offset=0.0, longitud=0.8))
        n_1_labels_gdl = elemento_label_grados_libertad(n_1).scale(0.5)
        n_2_gdl = VGroup(mg.get_grados_libertad(n_2, 'x', offset=0.0, longitud=0.8))
        n_2_labels_gdl = elemento_label_grados_libertad(n_2).scale(0.5)
        n_3_gdl = VGroup(mg.get_grados_libertad(n_3, 'x', offset=0.0, longitud=0.8))
        n_3_labels_gdl = elemento_label_grados_libertad(n_3).scale(0.5)
        n_4_gdl = VGroup(mg.get_grados_libertad(n_4, 'x', offset=0.0, longitud=0.8))
        n_4_labels_gdl = elemento_label_grados_libertad(n_4).scale(0.5)
        vector_desplazamientos_el_1_modificado = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_1,
                                                                                                       reducida=False)
        vector_desplazamientos_el_2_modificado = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_2,
                                                                                                       reducida=False)
        vector_desplazamientos_el_3_modificado = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_3,
                                                                                                       reducida=False)
        ## Se soluciona por mnspy
        mg.solucionar_por_gauss_y_calcular_reacciones()
        sol_final = np.array(mg._union._k.obtener_matriz(False)) @ np.array(mg._union._k.obtener_desplazamientos(False))
        sol_final_resta = sol_final - mg._union._k.obtener_fuerzas(False)
        solucion = ecuacion_array_a_matriz(sol_final, formato_num='{x:.8f}', left_bracket=r"\{", right_bracket=r"\}")

        matriz_global_final_base = mg.sistema_ecuaciones_matriz_rigidez_global(reducida=False)
        matriz_global_final = matriz_global_final_base.copy().scale(0.35).arrange(RIGHT)
        matriz_global_final_2 = matriz_global_final_base.copy()
        matriz_global_final_2[0] = matriz_global_base.copy()[0]
        matriz_global_final_2.scale(0.35).arrange(RIGHT)
        matriz_global_final_3 = matriz_global_final_base.copy()
        matriz_global_final_3[0] = matriz_global_base.copy()[0]
        matriz_global_final_3.submobjects.pop(2)
        matriz_global_final_3[2] = solucion

        matriz_global_final_4 = matriz_global_final_3.copy()
        matriz_global_final_3.scale(0.35).arrange(RIGHT)
        matriz_global_final_4.submobjects.pop(2)
        matriz_global_final_4.submobjects.pop(2)
        matriz_global_final_4[2] = ecuacion_array_a_matriz(sol_final_resta, formato_num='{x:.8f}', left_bracket=r"\{",
                                                           right_bracket=r"\}")
        matriz_global_final_4.scale(0.35).arrange(RIGHT)

        # ############
        cargas_puntuales = mg.get_cargas_puntuales_nodales(longitud=1.0, unidades=r"\,N").set_color(RED_D)
        cargas_puntuales[1].add_background_rectangle(
            color=BLACK,  # Color del recuadro
            opacity=0.9,  # Opacidad (0 es invisible, 1 es sólido)
            buff=0.04  # Margen/espacio entre el texto y el borde
        )
        # ############
        nodos, label_nodos, soportes = mg.get_nodos_y_soportes()
        nodos.set_color(RED)
        # ############
        elementos, label_elementos = mg.get_elementos()
        label_elementos.shift(0.4 * DOWN)
        k_1 = MathTex(r'k_1=200\,N/mm', color=WHITE).scale(0.7).next_to(elementos[0], UP)
        k_2 = MathTex(r'k_2=400\,N/mm', color=WHITE).scale(0.7).next_to(elementos[1], UP)
        k_3 = MathTex(r'k_3=600\,N/mm', color=WHITE).scale(0.7).next_to(elementos[2], UP)
        enunciado = Tex(
            r"Para el ensamblaje de resortes con nodos numerados arbitrariamente\\",
            r"que se muestra en la Figura, obtenga (a) la matriz de rigidez global,\\",
            r" (b) los desplazamientos de los nodos \textbf{3} y \textbf{4}, (c) las fuerzas de reacción\\",
            r"en los nodos \textbf{1} y \textbf{2}, y (d) las fuerzas en cada resorte. Se aplica una fuerza de $25\,kN$ en el nodo \textbf{4} en la dirección $x$.\\"
            r"Las constantes de los resortes se dan en la figura. Los nodos \textbf{1} y \textbf{2} están fijos.",
            tex_environment="flushleft",  # Esto alinea el texto a la izquierda
            font_size=36
        ).to_edge(UP + LEFT)
        # ############

        # Ecuaciones generales del resorte
        ecuacion_local_resorte = VGroup(Matrix([['f']], left_bracket=r"\{", right_bracket=r"\}"),
                                        ecuacion_signo_igual().copy(), Matrix([['k']]),
                                        Matrix([['d']], left_bracket=r"\{", right_bracket=r"\}")).arrange(
            RIGHT).move_to(DOWN * 2)

        matrix_rigidez = Matrix(
            [['k', '-k'],
             ['-k', 'k']]
        )
        ## Ecuaciones Elemento 1
        ecuacion_local_resorte_1 = ecuacion_local_resorte.copy()
        matriz_k_1 = ecuacion_vector_fuerza_resorte('1', '1', '3')
        ### Cargas en elemento 1
        ### Grados de libertad en elemento 1
        grados_el_1 = VGroup(*n_1_gdl.copy(), *n_3_gdl.copy()).set_z_index(1)
        label_etiquetas_grados_el_1 = VGroup(*n_1_labels_gdl.copy(), *n_3_labels_gdl.copy())
        label_etiquetas_grados_el_1[0].next_to(grados_el_1[0], UP, buff=0.1)
        label_etiquetas_grados_el_1[1].next_to(grados_el_1[1], RIGHT, buff=0.1)
        #######################################################################################################
        ### Escena elemento 1
        escena_elemento_1 = VGroup(elementos[0], nodos[0:2], soportes[0:1], label_elementos[0], label_nodos[0:2], k_1)
        matrix_rigidez_1_1 = Matrix(
            [['200', '-200'],
             ['-200', '200']]
        )
        matrix_rigidez_1_2 = matrix_rigidez_1_1.copy()
        matrix_rigidez_1_3 = matrix_rigidez_1_1.copy()
        vector_desplazamientos_el_1 = ecuacion_vector_desplazamiento_resorte('1', '3')
        vector_desplazamientos_modificado_1_3 = vector_desplazamientos_el_1_modificado.copy()
        mr_elemento_1 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(), matrix_rigidez.copy(),
                               vector_desplazamientos_el_1.copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_1.to_edge(DOWN).scale(0.5)
        mr_elemento_1_1 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(),
                                 matrix_rigidez_1_2, vector_desplazamientos_el_1.copy()).arrange(RIGHT,
                                                                                                 buff=0.2)
        mr_elemento_1_1.to_edge(DOWN).scale(0.5)
        mr_elemento_1_2 = VGroup(matriz_k_1.copy(), ecuacion_signo_igual().copy(),
                                 matrix_rigidez_1_3, vector_desplazamientos_modificado_1_3, ).arrange(RIGHT, buff=0.2)
        mr_elemento_1_2.to_edge(DOWN).scale(0.5)
        mr_elemento_1_2_1 = mr_elemento_1_2.copy()
        mr_elemento_1_2_1[3] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_1, reducida=False).scale(0.5)
        mr_elemento_1_2_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_1_2_2 = mr_elemento_1_2_1.copy()
        sol_el_1_1 = np.array(e_1._k.obtener_matriz(False)) @ np.array(e_1._k.obtener_desplazamientos(False))
        mr_elemento_1_2_2[2] = ecuacion_array_a_matriz(sol_el_1_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_1_2_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_1_2_3 = mr_elemento_1_2_2.copy()
        mr_elemento_1_2_3.submobjects.pop(2)
        mr_elemento_1_2_3[2] = ecuacion_array_a_matriz(sol_el_1_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_1_2_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_1_2_4 = mr_elemento_1_2_1.copy()
        mr_elemento_1_2_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_resorte(e_1, mostrar_valores=True,
                                                                                     formato='%.8g').scale(0.5)
        mr_elemento_1_2_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        f_internas_elemento_1 = mg.elemento_fuerza_interna_resorte(e_1, unidades='')
        #######################################################################################################
        ## Ecuaciones Elemento 2
        ecuacion_local_resorte_2 = ecuacion_local_resorte.copy()
        matriz_k_2 = ecuacion_vector_fuerza_resorte('2', '3', '4')
        ### Cargas en elemento 2
        ### Grados de libertad en elemento 2
        grados_el_2 = VGroup(*n_3_gdl.copy(), *n_4_gdl.copy()).set_z_index(1)
        label_etiquetas_grados_el_2 = VGroup(*n_3_labels_gdl.copy(), *n_4_labels_gdl.copy())
        label_etiquetas_grados_el_2[0].next_to(grados_el_2[0], LEFT, buff=0.1)
        label_etiquetas_grados_el_2[1].next_to(grados_el_2[1], RIGHT, buff=0.1)

        ### Escena elemento 2
        escena_elemento_2 = VGroup(elementos[1], nodos[1:3],
                                   # soportes[0:1],
                                   label_elementos[1], label_nodos[1:3], k_2)
        matrix_rigidez_2_1 = Matrix(
            [['400', '-400'],
             ['-400', '400']]
        )
        matrix_rigidez_2_2 = matrix_rigidez_2_1.copy()
        matrix_rigidez_2_3 = matrix_rigidez_2_1.copy()
        vector_desplazamientos_el_2 = ecuacion_vector_desplazamiento_resorte('3', '4')
        vector_desplazamientos_modificado_2_3 = vector_desplazamientos_el_2_modificado.copy()
        mr_elemento_2 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), matrix_rigidez.copy(),
                               vector_desplazamientos_el_2.copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_2.to_edge(DOWN).scale(0.5)
        mr_elemento_2_1 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(),
                                 matrix_rigidez_2_2, vector_desplazamientos_el_2.copy()).arrange(RIGHT,
                                                                                                 buff=0.2)
        mr_elemento_2_1.to_edge(DOWN).scale(0.5)
        mr_elemento_2_2 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(),
                                 matrix_rigidez_2_3, vector_desplazamientos_modificado_2_3, ).arrange(RIGHT, buff=0.2)
        mr_elemento_2_2.to_edge(DOWN).scale(0.5)
        mr_elemento_2_2_1 = mr_elemento_2_2.copy()
        mr_elemento_2_2_1[3] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_2, reducida=False).scale(0.5)
        mr_elemento_2_2_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_2_2_2 = mr_elemento_2_2_1.copy()
        sol_el_2_1 = np.array(e_2._k.obtener_matriz(False)) @ np.array(e_2._k.obtener_desplazamientos(False))
        mr_elemento_2_2_2[2] = ecuacion_array_a_matriz(sol_el_2_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_2_2_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_2_2_3 = mr_elemento_2_2_2.copy()
        mr_elemento_2_2_3.submobjects.pop(2)
        mr_elemento_2_2_3[2] = ecuacion_array_a_matriz(sol_el_2_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_2_2_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_2_2_4 = mr_elemento_2_2_1.copy()
        mr_elemento_2_2_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_resorte(e_2, mostrar_valores=True,
                                                                                     formato='%.8g').scale(0.5)
        mr_elemento_2_2_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        f_internas_elemento_2 = mg.elemento_fuerza_interna_resorte(e_2, unidades='')
        #######################################################################################################
        ## Ecuaciones Elemento 3
        ecuacion_local_resorte_3 = ecuacion_local_resorte.copy()
        matriz_k_3 = ecuacion_vector_fuerza_resorte('3', '4', '2')
        ### Cargas en elemento 3
        ### Grados de libertad en elemento 3
        grados_el_3 = VGroup(*n_4_gdl.copy(), *n_2_gdl.copy()).set_z_index(1)
        label_etiquetas_grados_el_3 = VGroup(*n_4_labels_gdl.copy(), *n_2_labels_gdl.copy())
        label_etiquetas_grados_el_3[0].next_to(grados_el_3[0], LEFT, buff=0.1)
        label_etiquetas_grados_el_3[1].next_to(grados_el_3[1], UP, buff=0.1)

        ### Escena elemento 3
        escena_elemento_3 = VGroup(elementos[2], nodos[2:4], soportes[1], label_elementos[2], label_nodos[2:4], k_3)
        matrix_rigidez_3_1 = Matrix(
            [['600', '-600'],
             ['-600', '600']]
        )
        matrix_rigidez_3_2 = matrix_rigidez_3_1.copy()
        matrix_rigidez_3_3 = matrix_rigidez_3_1.copy()
        vector_desplazamientos_el_3 = ecuacion_vector_desplazamiento_resorte('4', '2')
        vector_desplazamientos_modificado_3_3 = vector_desplazamientos_el_3_modificado.copy()
        mr_elemento_3 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), matrix_rigidez.copy(),
                               vector_desplazamientos_el_3.copy()).arrange(RIGHT, buff=0.2)
        mr_elemento_3.to_edge(DOWN).scale(0.5)
        mr_elemento_3_1 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(),
                                 matrix_rigidez_3_2, vector_desplazamientos_el_3.copy()).arrange(RIGHT,
                                                                                                 buff=0.2)
        mr_elemento_3_1.to_edge(DOWN).scale(0.5)
        mr_elemento_3_2 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(),
                                 matrix_rigidez_3_3, vector_desplazamientos_modificado_3_3, ).arrange(RIGHT, buff=0.2)
        mr_elemento_3_2.to_edge(DOWN).scale(0.5)
        mr_elemento_3_2_1 = mr_elemento_3_2.copy()
        mr_elemento_3_2_1[3] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_3, reducida=False).scale(0.5)
        mr_elemento_3_2_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_3_2_2 = mr_elemento_3_2_1.copy()
        sol_el_3_1 = np.array(e_3._k.obtener_matriz(False)) @ np.array(e_3._k.obtener_desplazamientos(False))
        mr_elemento_3_2_2[2] = ecuacion_array_a_matriz(sol_el_3_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_3_2_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_3_2_3 = mr_elemento_3_2_2.copy()
        mr_elemento_3_2_3.submobjects.pop(2)
        mr_elemento_3_2_3[2] = ecuacion_array_a_matriz(sol_el_3_1, formato_num='{x:.8f}', left_bracket=r"\{",
                                                       right_bracket=r"\}").scale(0.5)
        mr_elemento_3_2_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        mr_elemento_3_2_4 = mr_elemento_3_2_1.copy()
        mr_elemento_3_2_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_resorte(e_3, mostrar_valores=True,
                                                                                     formato='%.8g').scale(0.5)
        mr_elemento_3_2_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        f_internas_elemento_3 = mg.elemento_fuerza_interna_resorte(e_3, unidades='')
        f_internas_elemento_3[0][1].shift(LEFT)
        f_internas_elemento_3[1][1].next_to(f_internas_elemento_3[0][1], UP, buff=0.0).shift(0.5*RIGHT)
        # #######################################################################################################
        # ### Escena elemento 2
        # escena_elemento_2 = VGroup(elementos[1], nodos[1:3], soportes[1:3], label_elementos[1], label_nodos[1:3],
        #                            cargas[2:5])
        # factor_matrix_rigidez_2_1 = MathTex(r'\dfrac{EI}{1000}')
        # factor_matrix_rigidez_2_2 = MathTex('EI')
        # factor_matrix_rigidez_2_3 = factor_matrix_rigidez_2_2.copy()
        # factor_matrix_rigidez_2_4 = factor_matrix_rigidez_2_2.copy()
        #
        # matrix_rigidez_2_1 = Matrix(
        #     [['12', '60', '-12', '60'],
        #      ['60', '400', '-60', '200'],
        #      ['-12', '-60', '12', '-60'],
        #      ['60', '200', '-60', '400']]
        # )
        # matrix_rigidez_2_2 = Matrix(
        #     [['0.012', '0.06', '-0.012', '0.06'],
        #      ['0.06', '0.4', '-0.06', '0.2'],
        #      ['-0.012', '-0.06', '0.012', '-0.06'],
        #      ['0.06', '0.2', '-0.060', '0.4']],
        #     h_buff=1.8
        # )
        # matrix_rigidez_2_3 = matrix_rigidez_2_2.copy()
        # matrix_rigidez_2_4 = matrix_rigidez_2_2.copy()
        # vector_desplazamientos_el_2 = ecuacion_vector_desplazamiento_viga(2, 3)
        # vector_desplazamientos_modificado_2_3 = vector_desplazamientos_el_2_modificado.copy()
        # vector_desplazamientos_modificado_2_4 = vector_desplazamientos_el_2_modificado.copy()
        # vector_fuerza_nodal_equivalente_viga_2 = ecuacion_array_a_matriz(e_2._obtener_fuerzas(), left_bracket=r"\{",
        #                                                                  right_bracket=r"\}")
        # mr_elemento_2 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez.copy(),
        #                        matrix_rigidez.copy(),
        #                        vector_desplazamientos_el_2.copy(), ecuacion_signo_menos().copy(),
        #                        ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT, buff=0.2)
        # mr_elemento_2.to_edge(DOWN).scale(0.5)
        # mr_elemento_2_1 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_1,
        #                          matrix_rigidez_2_1, vector_desplazamientos_el_2.copy(), ecuacion_signo_menos().copy(),
        #                          ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT, buff=0.2)
        # mr_elemento_2_1.to_edge(DOWN).scale(0.5)
        # mr_elemento_2_2 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_2,
        #                          matrix_rigidez_2_2, vector_desplazamientos_el_2.copy(), ecuacion_signo_menos().copy(),
        #                          ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT,
        #                                                                                              buff=0.2)
        # mr_elemento_2_2.to_edge(DOWN).scale(0.5)
        # mr_elemento_2_3 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_3,
        #                          matrix_rigidez_2_3, vector_desplazamientos_modificado_2_3,
        #                          ecuacion_signo_menos().copy(),
        #                          ecuacion_vector_fuerza_nodal_equivalente_viga(2, 3).copy()).arrange(RIGHT,
        #                                                                                              buff=0.2)
        # mr_elemento_2_3.to_edge(DOWN).scale(0.5)
        # mr_elemento_2_4 = VGroup(matriz_k_2.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_2_4,
        #                          matrix_rigidez_2_4, vector_desplazamientos_modificado_2_4,
        #                          ecuacion_signo_menos().copy(),
        #                          vector_fuerza_nodal_equivalente_viga_2).arrange(RIGHT,
        #                                                                          buff=0.2)
        # mr_elemento_2_4.to_edge(DOWN).scale(0.5)
        # mr_elemento_2_4_1 = mr_elemento_2_4.copy()
        # mr_elemento_2_4_1[4] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_2, EI_cte=True,
        #                                                                              reducida=False).scale(0.5)
        # mr_elemento_2_4_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # mr_elemento_2_4_2 = mr_elemento_2_4_1.copy()
        # mr_elemento_2_4_2.submobjects.pop(2)
        # mr_elemento_2_4_2.submobjects.pop(2)
        # sol_el_2_1 = np.array(e_2._k.obtener_matriz(False)) @ np.array(e_2._k.obtener_desplazamientos(False))
        # sol_el_2_2 = sol_el_2_1 - e_2._obtener_fuerzas()
        # mr_elemento_2_4_2[2] = ecuacion_array_a_matriz(sol_el_2_1, formato_num='{x:.8f}', left_bracket=r"\{",
        #                                                right_bracket=r"\}").scale(0.5)
        # mr_elemento_2_4_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # mr_elemento_2_4_3 = mr_elemento_2_4_2.copy()
        # mr_elemento_2_4_3.submobjects.pop(2)
        # mr_elemento_2_4_3.submobjects.pop(2)
        # mr_elemento_2_4_3[2] = ecuacion_array_a_matriz(sol_el_2_2, formato_num='{x:.8f}', left_bracket=r"\{",
        #                                                right_bracket=r"\}").scale(0.5)
        # mr_elemento_2_4_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # mr_elemento_2_4_4 = mr_elemento_2_4_1.copy()
        # mr_elemento_2_4_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_viga(e_1, mostrar_valores=True,
        #                                                                           formato='%.8g').scale(0.5)
        # mr_elemento_2_4_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # ecuacion_v_e_2 = MathTex(sp.latex(e_2.ecuacion_de_cortante()), color=BLUE_A)
        # ecuacion_m_e_2 = MathTex(sp.latex(e_2.ecuacion_de_momento()), color=GREEN_A)
        # ec_e_2 = VGroup(ecuacion_v_e_2, ecuacion_m_e_2).arrange(DOWN, buff=0.2).scale(0.5).to_corner(DR, buff=0.5)
        #
        # ## Ecuaciones Elemento 3
        # ecuacion_local_viga_3 = ecuacion_local_viga.copy()
        # matriz_k_3 = ecuacion_vector_fuerza_viga(3, 3, 4)
        # ### Cargas nodales equivalentes
        # # Ninguna
        # ### Cargas en elemento 3
        # # Ninguna
        # ### Grados de libertad en elemento 3
        # grados_el_3 = VGroup(*n_3_gdl.copy(), *n_4_gdl.copy()).set_z_index(1)
        # label_etiquetas_grados_el_3 = VGroup(*n_3_labels_gdl.copy(), *n_4_labels_gdl.copy())
        # label_etiquetas_grados_el_3[0].next_to(grados_el_3[0], DOWN, buff=0.02).scale(0.5)
        # label_etiquetas_grados_el_3[1].next_to(grados_el_3[1], UR, buff=-0.25).scale(0.5)
        # label_etiquetas_grados_el_3[2].next_to(grados_el_3[2], UP, buff=0.02).scale(0.5)
        # label_etiquetas_grados_el_3[3].next_to(grados_el_3[3], DOWN, buff=0.0).scale(0.5)
        #
        # f_internas_elemento_2 = mg.elemento_fuerza_interna_viga(e_2, unidades=['', ''])
        # #######################################################################################################
        # ### Escena elemento 3
        # escena_elemento_3 = VGroup(elementos[2], nodos[2:4], soportes[2:4], label_elementos[2], label_nodos[2:4])
        # factor_matrix_rigidez_3_1 = MathTex(r'\dfrac{EI}{125}')
        # factor_matrix_rigidez_3_2 = MathTex('EI')
        # factor_matrix_rigidez_3_3 = factor_matrix_rigidez_3_2.copy()
        # factor_matrix_rigidez_3_4 = factor_matrix_rigidez_3_2.copy()
        # matrix_rigidez_3_1 = Matrix(
        #     [['12', '30', '-12', '30'],
        #      ['30', '100', '-30', '50'],
        #      ['-12', '-30', '12', '-30'],
        #      ['63', '50', '-30', '100']]
        # )
        #
        # matrix_rigidez_3_2 = ecuacion_array_a_matriz(e_3.get_matriz_rigidez(), h_buff=1.8)
        # matrix_rigidez_3_3 = matrix_rigidez_3_2.copy()
        # matrix_rigidez_3_4 = matrix_rigidez_3_2.copy()
        # vector_desplazamientos_el_3 = ecuacion_vector_desplazamiento_viga(3, 4)
        # vector_desplazamientos_modificado_3_3 = vector_desplazamientos_el_3_modificado.copy()
        # vector_desplazamientos_modificado_3_4 = vector_desplazamientos_el_3_modificado.copy()
        # vector_fuerza_nodal_equivalente_viga_3 = ecuacion_array_a_matriz(e_3._obtener_fuerzas(), left_bracket=r"\{",
        #                                                                  right_bracket=r"\}")
        # mr_elemento_3 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez.copy(),
        #                        matrix_rigidez.copy(),
        #                        vector_desplazamientos_el_3.copy(), ecuacion_signo_menos().copy(),
        #                        ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT, buff=0.2)
        # mr_elemento_3.to_edge(DOWN).scale(0.5)
        # mr_elemento_3_1 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_1,
        #                          matrix_rigidez_3_1, vector_desplazamientos_el_3.copy(), ecuacion_signo_menos().copy(),
        #                          ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT, buff=0.2)
        # mr_elemento_3_1.to_edge(DOWN).scale(0.5)
        # mr_elemento_3_2 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_2,
        #                          matrix_rigidez_3_2, vector_desplazamientos_el_3.copy(), ecuacion_signo_menos().copy(),
        #                          ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT,
        #                                                                                              buff=0.2)
        # mr_elemento_3_2.to_edge(DOWN).scale(0.5)
        # mr_elemento_3_3 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_3,
        #                          matrix_rigidez_3_3, vector_desplazamientos_modificado_3_3,
        #                          ecuacion_signo_menos().copy(),
        #                          ecuacion_vector_fuerza_nodal_equivalente_viga(3, 4).copy()).arrange(RIGHT,
        #                                                                                              buff=0.2)
        # mr_elemento_3_3.to_edge(DOWN).scale(0.5)
        # mr_elemento_3_4 = VGroup(matriz_k_3.copy(), ecuacion_signo_igual().copy(), factor_matrix_rigidez_3_4,
        #                          matrix_rigidez_3_4, vector_desplazamientos_modificado_3_4,
        #                          ecuacion_signo_menos().copy(),
        #                          vector_fuerza_nodal_equivalente_viga_3).arrange(RIGHT,
        #                                                                          buff=0.2)
        # mr_elemento_3_4.to_edge(DOWN).scale(0.5)
        # mr_elemento_3_4_1 = mr_elemento_3_4.copy()
        # mr_elemento_3_4_1[4] = mg.ecuacion_vector_etiquetas_desplazamientos_elemento(e_3, EI_cte=True,
        #                                                                              reducida=False).scale(0.5)
        # mr_elemento_3_4_1.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # mr_elemento_3_4_2 = mr_elemento_3_4_1.copy()
        # mr_elemento_3_4_2.submobjects.pop(2)
        # mr_elemento_3_4_2.submobjects.pop(2)
        # sol_el_3_1 = np.array(e_3._k.obtener_matriz(False)) @ np.array(e_3._k.obtener_desplazamientos(False))
        # sol_el_3_2 = sol_el_3_1 - e_3._obtener_fuerzas()
        # mr_elemento_3_4_2[2] = ecuacion_array_a_matriz(sol_el_3_1, formato_num='{x:.8f}', left_bracket=r"\{",
        #                                                right_bracket=r"\}").scale(0.5)
        # mr_elemento_3_4_2.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # mr_elemento_3_4_3 = mr_elemento_3_4_2.copy()
        # mr_elemento_3_4_3.submobjects.pop(2)
        # mr_elemento_3_4_3.submobjects.pop(2)
        # mr_elemento_3_4_3[2] = ecuacion_array_a_matriz(sol_el_3_2, formato_num='{x:.8f}', left_bracket=r"\{",
        #                                                right_bracket=r"\}").scale(0.5)
        # mr_elemento_3_4_3.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # mr_elemento_3_4_4 = mr_elemento_3_4_1.copy()
        # mr_elemento_3_4_4[0] = mg.ecuacion_vector_etiquetas_fuerzas_internas_viga(e_3, mostrar_valores=True,
        #                                                                           formato='%.8g').scale(0.5)
        # mr_elemento_3_4_4.arrange(RIGHT, buff=0.2).to_edge(DOWN)
        # ecuacion_v_e_3 = MathTex(sp.latex(e_3.ecuacion_de_cortante()), color=BLUE_A)
        # ecuacion_m_e_3 = MathTex(sp.latex(e_3.ecuacion_de_momento()), color=GREEN_A)
        # ec_e_3 = VGroup(ecuacion_v_e_3, ecuacion_m_e_3).arrange(DOWN, buff=0.2).scale(0.5).to_corner(DR, buff=0.5)
        #
        # f_internas_elemento_3 = mg.elemento_fuerza_interna_viga(e_3, unidades=['', ''])
        # ## Elementos intermedios
        ## Diagrama resorte inicial
        escena_inicial = VGroup(elementos, soportes, cargas_puntuales, k_1, k_2, k_3, label_nodos, label_elementos)
        escena_inicial.save_state()
        escena_inicial.to_edge(DOWN + LEFT)
        escena = VGroup(nodos, elementos, soportes, label_elementos, label_nodos, cargas_puntuales)

        # Animaciones
        tit = titulo("Método de Elementos Finitos", "Análisis de un ensamble de resortes")
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.play(FadeIn(tit[2], shift=UP))  # Sube ligeramente al aparecer
        self.wait(2)
        self.play(FadeOut(tit))

        ## Enunciado
        self.play(Write(enunciado), run_time=5)
        ## Diagrama de los resortes
        self.play(FadeIn(escena_inicial), run_time=2)
        self.wait(5)
        self.play(FadeOut(enunciado), run_time=2)
        self.play(Restore(escena_inicial), run_time=2)
        self.wait(5)
        self.play(FadeOut(escena_inicial))
        self.wait(0.5)
        tit = titulo("Discretización del ensamble", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(Restore(escena_inicial))
        self.wait(2)
        ## Discretización del ensamble
        # self.play(Create(mg.ejes), run_time=2)
        # self.play(FadeOut(viga), run_time=2)
        self.play(DrawBorderThenFill(nodos), run_time=2)
        # self.play(Write(label_nodos), Write(label_elementos), run_time=2)
        etiquetas = [MathTex('Nodo'), MathTex('GL[x]')]
        rows = [[1, 'Restringido'],
                [2, 'Restringido'],
                [3, 'Libre'],
                [4, 'Libre']]
        tab_nodos = elemento_tabla(etiquetas, rows).scale(0.5).to_edge(DOWN, buff=0.5)
        etiquetas = [MathTex('Elemento'), MathTex('Nodo_i'), MathTex('Nodo_j'), MathTex('k[N/mm]')]
        rows = [[1, 1, 3, 200],
                [2, 3, 4, 400],
                [3, 4, 2, 600]]
        tab_elementos = elemento_tabla(etiquetas, rows).scale(0.5).to_edge(DOWN, buff=0.5)
        VGroup(tab_nodos, tab_elementos).arrange(RIGHT, buff=1).to_edge(DOWN, buff=0.5)
        self.play(Create(tab_nodos[1]), Create(tab_nodos[2]), run_time=1)
        self.play(FadeIn(tab_nodos[0].get_rows()))
        self.wait(2)
        self.play(Create(tab_elementos[1]), Create(tab_elementos[2]), run_time=1)
        self.play(FadeIn(tab_elementos[0].get_rows()))
        self.wait(5)
        self.play(FadeOut(tab_nodos, tab_elementos), FadeOut(escena), FadeOut(k_1, k_2, k_3), run_time=2)
        # #######################################################################################################
        ## Análisis Elemento 1
        tit = titulo("Matriz de rigidez del elemento 1", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(escena_elemento_1), run_time=2)
        self.wait(1)
        self.play(Write(ecuacion_local_resorte_1), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_local_resorte_1, mr_elemento_1), run_time=2)
        self.play(ReplacementTransform(mr_elemento_1, mr_elemento_1_1), run_time=2)
        self.wait(2)
        self.play(FadeOut(soportes[0:1]), run_time=2)
        self.play(FadeIn(grados_el_1), run_time=2)
        self.play(Write(label_etiquetas_grados_el_1), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(mr_elemento_1_1[3].get_brackets(), mr_elemento_1_2[3].get_brackets()),
                  ReplacementTransform(mr_elemento_1_1[0:3], mr_elemento_1_2[0:3]),
                  FadeOut(mr_elemento_1_1[3].get_entries()),
                  ReplacementTransform(label_etiquetas_grados_el_1[0], mr_elemento_1_2[3].get_entries()[0]),
                  ReplacementTransform(label_etiquetas_grados_el_1[1], mr_elemento_1_2[3].get_entries()[1]),
                  Unwrite(grados_el_1), run_time=2)
        self.wait(1)
        self.play(FadeIn(f_internas_elemento_1))
        self.wait(2)
        self.play(FadeOut(f_internas_elemento_1))
        self.play(FadeOut(elementos[0], nodos[0:2], label_elementos[0], label_nodos[0:2]), FadeOut(mr_elemento_1_2),
                  FadeOut(k_1))
        # #######################################################################################################
        ## Análisis Elemento 2
        tit = titulo("Matriz de rigidez del elemento 2", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(escena_elemento_2), run_time=2)
        self.wait(1)
        self.play(Write(ecuacion_local_resorte_2), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_local_resorte_2, mr_elemento_2), run_time=2)
        self.play(ReplacementTransform(mr_elemento_2, mr_elemento_2_1), run_time=2)
        self.wait(2)
        # self.play(FadeOut(soportes[0:1]), run_time=2)
        self.play(FadeIn(grados_el_2), run_time=2)
        self.play(Write(label_etiquetas_grados_el_2), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(mr_elemento_2_1[3].get_brackets(), mr_elemento_2_2[3].get_brackets()),
                  ReplacementTransform(mr_elemento_2_1[0:3], mr_elemento_2_2[0:3]),
                  FadeOut(mr_elemento_2_1[3].get_entries()),
                  ReplacementTransform(label_etiquetas_grados_el_2[0], mr_elemento_2_2[3].get_entries()[0]),
                  ReplacementTransform(label_etiquetas_grados_el_2[1], mr_elemento_2_2[3].get_entries()[1]),
                  Unwrite(grados_el_2), run_time=2)
        self.wait(1)
        self.play(FadeIn(f_internas_elemento_2))
        self.wait(2)
        self.play(FadeOut(f_internas_elemento_2))
        self.play(FadeOut(elementos[1], nodos[1:3], label_elementos[1], label_nodos[1:3]), FadeOut(mr_elemento_2_2),
                  FadeOut(k_2))
        # #######################################################################################################
        ## Análisis Elemento 3
        tit = titulo("Matriz de rigidez del elemento 3", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        self.play(FadeIn(escena_elemento_3), run_time=2)
        self.wait(1)
        self.play(Write(ecuacion_local_resorte_3), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_local_resorte_3, mr_elemento_3), run_time=2)
        self.play(ReplacementTransform(mr_elemento_3, mr_elemento_3_1), run_time=2)
        self.wait(2)
        self.play(FadeOut(soportes[1]), run_time=2)
        self.play(FadeIn(grados_el_3), run_time=2)
        self.play(Write(label_etiquetas_grados_el_3), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(mr_elemento_3_1[3].get_brackets(), mr_elemento_3_2[3].get_brackets()),
                  ReplacementTransform(mr_elemento_3_1[0:3], mr_elemento_3_2[0:3]),
                  FadeOut(mr_elemento_3_1[3].get_entries()),
                  ReplacementTransform(label_etiquetas_grados_el_3[0], mr_elemento_3_2[3].get_entries()[0]),
                  ReplacementTransform(label_etiquetas_grados_el_3[1], mr_elemento_3_2[3].get_entries()[1]),
                  Unwrite(grados_el_3), run_time=2)
        self.wait(1)
        self.play(FadeIn(f_internas_elemento_3))
        self.wait(2)
        self.play(FadeOut(f_internas_elemento_3))
        self.play(FadeOut(elementos[2], nodos[2:4], label_elementos[2], label_nodos[2:4]), FadeOut(mr_elemento_3_2),
                  FadeOut(k_3))
        tit = titulo("Matriz de rigidez goblal (Ensamblaje)", size_titulo=36)
        self.play(Write(tit[0]))
        self.play(Create(tit[1]))
        self.wait(2)
        self.play(FadeOut(tit))
        m_1 = mr_elemento_1_2.copy()
        m_2 = mr_elemento_2_2.copy()
        m_3 = mr_elemento_3_2.copy()
        self.play(FadeIn(m_1.to_edge(UP)), FadeIn(m_2.move_to(ORIGIN)), FadeIn(m_3.to_edge(DOWN)))
        self.wait(2)
        self.play(
            ReplacementTransform(VGroup(m_1[0].get_brackets()[0], m_2[0].get_brackets()[0], m_3[0].get_brackets()[0]),
                                 matriz_global[0].get_brackets()[0]),
            ReplacementTransform(VGroup(m_1[0].get_brackets()[1], m_2[0].get_brackets()[1], m_3[0].get_brackets()[1]),
                                 matriz_global[0].get_brackets()[1]),
            runtime=4)
        self.play(
            ReplacementTransform(m_1[0].get_entries()[0], matriz_global[0].get_entries()[0]),
            ReplacementTransform(VGroup(m_1[0].get_entries()[1], m_2[0].get_entries()[0]),
                                 matriz_global[0].get_entries()[1]),
            ReplacementTransform(VGroup(m_2[0].get_entries()[1], m_3[0].get_entries()[0]),
                                 matriz_global[0].get_entries()[2]),
            ReplacementTransform(m_3[0].get_entries()[1], matriz_global[0].get_entries()[3]),
            runtime=4)
        self.play(
            ReplacementTransform(VGroup(m_1[1], m_2[1], m_3[1]), matriz_global[1]),
            runtime=4)
        self.play(
            ReplacementTransform(VGroup(m_1[2].get_brackets()[0], m_2[2].get_brackets()[0], m_3[2].get_brackets()[0]),
                                 matriz_global[2].get_brackets()[0]),
            ReplacementTransform(VGroup(m_1[2].get_brackets()[1], m_2[2].get_brackets()[1], m_3[2].get_brackets()[1]),
                                 matriz_global[2].get_brackets()[1]),
            m_1[3].animate.next_to(matriz_global[2], RIGHT, buff=0.5).align_to(m_1[3], UP),
            m_2[3].animate.next_to(matriz_global[2], RIGHT, buff=0.5).align_to(m_2[3], UP),
            m_3[3].animate.next_to(matriz_global[2], RIGHT, buff=0.5).align_to(m_3[3], UP),
            runtime=4)
        self.play(
            ReplacementTransform(m_1[2].get_entries()[0:2], matriz_global[2].get_entries()[0:2]),
            ReplacementTransform(m_1[2].get_entries()[2], matriz_global[2].get_entries()[4]),
            ReplacementTransform(m_2[2].get_entries()[1], matriz_global[2].get_entries()[6]),
            ReplacementTransform(m_2[2].get_entries()[2], matriz_global[2].get_entries()[9]),
            ReplacementTransform(m_3[2].get_entries()[1], matriz_global[2].get_entries()[11]),
            ReplacementTransform(m_3[2].get_entries()[2:], matriz_global[2].get_entries()[14:]),
            ReplacementTransform(
                VGroup(m_1[2].get_entries()[3], m_2[2].get_entries()[0]),
                matriz_global[2].get_entries()[5]),
            ReplacementTransform(
                VGroup(m_2[2].get_entries()[3], m_3[2].get_entries()[0]),
                matriz_global[2].get_entries()[10]),
            runtime=4)
        self.play(
            FadeIn(matriz_global[2].get_entries()[2:4]),
            FadeIn(matriz_global[2].get_entries()[7:9]),
            FadeIn(matriz_global[2].get_entries()[12:14]),
            runtime=4)
        self.play(
            ReplacementTransform(VGroup(m_1[3].get_brackets()[0], m_2[3].get_brackets()[0], m_3[3].get_brackets()[0]),
                                 matriz_global[3].get_brackets()[0]),
            ReplacementTransform(VGroup(m_1[3].get_brackets()[1], m_2[3].get_brackets()[1], m_3[3].get_brackets()[1]),
                                 matriz_global[3].get_brackets()[1]),
            ReplacementTransform(m_1[3].get_entries()[0], matriz_global[3].get_entries()[0]),
            ReplacementTransform(VGroup(m_1[3].get_entries()[1], m_2[3].get_entries()[0]),
                                 matriz_global[3].get_entries()[1]),
            ReplacementTransform(VGroup(m_2[3].get_entries()[1], m_3[3].get_entries()[0]),
                                 matriz_global[3].get_entries()[2]),
            ReplacementTransform(m_3[3].get_entries()[1], matriz_global[3].get_entries()[3]),
            runtime=4)
        # self.play(
        #     ReplacementTransform(VGroup(m_1[6].get_brackets()[0], m_2[6].get_brackets()[0], m_3[6].get_brackets()[0]),
        #                          matriz_global[6].get_brackets()[0]),
        #     ReplacementTransform(VGroup(m_1[6].get_brackets()[1], m_2[6].get_brackets()[1], m_3[6].get_brackets()[1]),
        #                          matriz_global[6].get_brackets()[1]),
        #     ReplacementTransform(m_1[6].get_entries()[:2], matriz_global[6].get_entries()[:2]),
        #     ReplacementTransform(VGroup(m_1[6].get_entries()[2:], m_2[6].get_entries()[:2]),
        #                          matriz_global[6].get_entries()[2:4]),
        #     ReplacementTransform(VGroup(m_2[6].get_entries()[2:], m_3[6].get_entries()[:2]),
        #                          matriz_global[6].get_entries()[4:6]),
        #     ReplacementTransform(m_3[6].get_entries()[2:], matriz_global[6].get_entries()[6:]),
        #     ReplacementTransform(VGroup(m_1[5], m_2[5], m_3[5]), matriz_global[5]),
        #     runtime=4)
        # self.wait(5)
        # self.play(FadeOut(matriz_global))
        # tit = titulo("Matriz de rigidez goblal reducida", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # self.play(FadeIn(matriz_global))
        # items_reducida = [3, 5]
        # elementos_reducida = list()
        # elementos_no_reducida = list()
        # for f in items_reducida:
        #     for c, elem in enumerate(matriz_global[3].get_rows()[f]):
        #         if c in items_reducida:
        #             elementos_reducida.append(elem)
        #         else:
        #             elementos_no_reducida.append(elem)
        # self.play(ReplacementTransform(matriz_global[0].get_brackets(), matriz_global_reducida[0].get_brackets()),
        #           ReplacementTransform(matriz_global[3].get_brackets(), matriz_global_reducida[3].get_brackets()),
        #           ReplacementTransform(matriz_global[4].get_brackets(), matriz_global_reducida[4].get_brackets()),
        #           ReplacementTransform(matriz_global[6].get_brackets(), matriz_global_reducida[6].get_brackets()),
        #           FadeOut(matriz_global[0].get_rows()[:3], matriz_global[3].get_rows()[:3],
        #                   matriz_global[4].get_rows()[:3], matriz_global[6].get_rows()[:3]),
        #           FadeOut(matriz_global[0].get_rows()[4], matriz_global[3].get_rows()[4],
        #                   matriz_global[4].get_rows()[4],
        #                   matriz_global[6].get_rows()[4]),
        #           FadeOut(matriz_global[0].get_rows()[6:], matriz_global[3].get_rows()[6:],
        #                   matriz_global[4].get_rows()[6:],
        #                   matriz_global[6].get_rows()[6:]),
        #           *[FadeOut(elem) for elem in elementos_no_reducida],
        #           ReplacementTransform(matriz_global[1], matriz_global_reducida[1]),
        #           ReplacementTransform(matriz_global[2], matriz_global_reducida[2]),
        #           ReplacementTransform(matriz_global[5], matriz_global_reducida[5]),
        #           ReplacementTransform(matriz_global[0].get_entries()[3], matriz_global_reducida[0].get_entries()[0]),
        #           ReplacementTransform(matriz_global[0].get_entries()[5], matriz_global_reducida[0].get_entries()[1]),
        #           ReplacementTransform(elementos_reducida[0], matriz_global_reducida[3].get_entries()[0]),
        #           ReplacementTransform(elementos_reducida[1], matriz_global_reducida[3].get_entries()[1]),
        #           ReplacementTransform(elementos_reducida[2], matriz_global_reducida[3].get_entries()[2]),
        #           ReplacementTransform(elementos_reducida[3], matriz_global_reducida[3].get_entries()[3]),
        #           ReplacementTransform(matriz_global[4].get_entries()[3], matriz_global_reducida[4].get_entries()[0]),
        #           ReplacementTransform(matriz_global[4].get_entries()[5], matriz_global_reducida[4].get_entries()[1]),
        #           ReplacementTransform(matriz_global[6].get_entries()[3], matriz_global_reducida[6].get_entries()[0]),
        #           ReplacementTransform(matriz_global[6].get_entries()[5], matriz_global_reducida[6].get_entries()[1]),
        #           run_time=4)
        # self.wait(2)
        # self.play(FadeOut(matriz_global_reducida))
        # tit = titulo("Resolución de los desplazamientos desconocidos", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # self.play(FadeIn(matriz_global_reducida))
        #
        # self.play(ReplacementTransform(matriz_global_reducida[6], matriz_global_reducida_final[0]),
        #           ReplacementTransform(matriz_global_reducida[1], matriz_global_reducida_final[1]),
        #           ReplacementTransform(matriz_global_reducida[2], matriz_global_reducida_final[2]),
        #           ReplacementTransform(matriz_global_reducida[3], matriz_global_reducida_final[3]),
        #           ReplacementTransform(matriz_global_reducida[4], matriz_global_reducida_final[4]),
        #           FadeOut(matriz_global_reducida[0], matriz_global_reducida[5]), run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(matriz_global_reducida_final[3], matriz_global_reducida_final_2[1][0]),
        #           ReplacementTransform(matriz_global_reducida_final[0], matriz_global_reducida_final_2[2]),
        #           ReplacementTransform(matriz_global_reducida_final[2], matriz_global_reducida_final_2[0]),
        #           ReplacementTransform(matriz_global_reducida_final[1], matriz_global_reducida_final_2[3]),
        #           ReplacementTransform(matriz_global_reducida_final[4], matriz_global_reducida_final_2[4]),
        #           FadeIn(matriz_global_reducida_final_2[1][1]), run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(matriz_global_reducida_final_2[1][0].get_brackets(),
        #                                matriz_global_reducida_final_3[1].get_brackets()),
        #           ReplacementTransform(matriz_global_reducida_final_2[1][0].get_entries(),
        #                                matriz_global_reducida_final_3[1].get_entries()),
        #           ReplacementTransform(matriz_global_reducida_final_2[0], matriz_global_reducida_final_3[0]),
        #           ReplacementTransform(matriz_global_reducida_final_2[2], matriz_global_reducida_final_3[2]),
        #           ReplacementTransform(matriz_global_reducida_final_2[3], matriz_global_reducida_final_3[3]),
        #           ReplacementTransform(matriz_global_reducida_final_2[4], matriz_global_reducida_final_3[4]),
        #
        #           FadeOut(matriz_global_reducida_final_2[1][1]), run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(
        #     VGroup(matriz_global_reducida_final_3[1].get_entries(), matriz_global_reducida_final_3[2].get_entries()),
        #     matriz_global_reducida_final_4[1].get_entries()),
        #     ReplacementTransform(matriz_global_reducida_final_3[1].get_brackets()[0],
        #                          matriz_global_reducida_final_4[1].get_brackets()[0]),
        #     ReplacementTransform(matriz_global_reducida_final_3[2].get_brackets()[1],
        #                          matriz_global_reducida_final_4[1].get_brackets()[1]),
        #     FadeOut(matriz_global_reducida_final_3[1].get_brackets()[1]),
        #     FadeOut(matriz_global_reducida_final_3[2].get_brackets()[0]),
        #
        #     ReplacementTransform(matriz_global_reducida_final_3[0], matriz_global_reducida_final_4[0]),
        #     ReplacementTransform(matriz_global_reducida_final_3[3], matriz_global_reducida_final_4[2]),
        #     ReplacementTransform(matriz_global_reducida_final_3[4], matriz_global_reducida_final_4[3]),
        #
        #     # FadeOut(matriz_global_reducida_final_3[2]),
        #     run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(matriz_global_reducida_final_4[1].get_entries()[0], sol_1[2]),
        #           ReplacementTransform(matriz_global_reducida_final_4[1].get_entries()[1], sol_2[2]),
        #           ReplacementTransform(matriz_global_reducida_final_4[2], VGroup(sol_1[1], sol_2[1])),
        #           ReplacementTransform(matriz_global_reducida_final_4[3].get_entries()[0], sol_1[0]),
        #           ReplacementTransform(matriz_global_reducida_final_4[3].get_entries()[1], sol_2[0]),
        #           FadeOut(matriz_global_reducida_final_4[1].get_brackets()),
        #           FadeOut(matriz_global_reducida_final_4[3].get_brackets()),
        #           FadeOut(matriz_global_reducida_final_4[0]),
        #           run_time=4)
        # self.wait(2)
        # self.play(FadeOut(sol_1), FadeOut(sol_2))
        # tit = titulo("Resolución de las reacciones desconocidas", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # self.play(FadeIn(matriz_global_final_2))
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(matriz_global_final_2[0:2]), VGroup(matriz_global_final_3[0:2])),
        #           ReplacementTransform(
        #               VGroup(matriz_global_final_2[3].get_entries(), matriz_global_final_2[4].get_entries()),
        #               VGroup(matriz_global_final_3[2].get_entries())),
        #           # ReplacementTransform(VGroup(matriz_global_final_2[2:5]), VGroup(matriz_global_final_3[2])),
        #           ReplacementTransform(matriz_global_final_2[3].get_brackets()[0],
        #                                matriz_global_final_3[2].get_brackets()[0]),
        #           ReplacementTransform(matriz_global_final_2[4].get_brackets()[1],
        #                                matriz_global_final_3[2].get_brackets()[1]),
        #           FadeOut(matriz_global_final_2[3].get_brackets()[1]),
        #           FadeOut(matriz_global_final_2[4].get_brackets()[0]),
        #           FadeOut(matriz_global_final_2[2]),
        #           ReplacementTransform(VGroup(matriz_global_final_2[5:7]), VGroup(matriz_global_final_3[3:5])),
        #           # FadeOut(matriz_global_final_2),
        #           run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(matriz_global_final_3[0:2]), VGroup(matriz_global_final_4[0:2])),
        #           ReplacementTransform(matriz_global_final_3[2].get_brackets()[0],
        #                                matriz_global_final_4[2].get_brackets()[0]),
        #           ReplacementTransform(matriz_global_final_3[4].get_brackets()[1],
        #                                matriz_global_final_4[2].get_brackets()[1]),
        #
        #           ReplacementTransform(
        #               VGroup(matriz_global_final_3[2].get_entries(), matriz_global_final_3[4].get_entries()),
        #               VGroup(matriz_global_final_4[2].get_entries())),
        #           FadeOut(matriz_global_final_3[3]),
        #           FadeOut(matriz_global_final_3[2].get_brackets()[1]),
        #           FadeOut(matriz_global_final_3[4].get_brackets()[0]),
        #           run_time=4)
        # self.wait(2)
        #
        # self.play(FadeOut(matriz_global_final_4))
        # tit = titulo("Matriz global solucionada", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # self.play(FadeIn(matriz_global_final))
        # self.wait(5)
        # self.play(FadeOut(matriz_global_final))
        # tit = titulo("Fuerzas internas del elemento 1", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        #
        # self.play(FadeIn(elementos[0], nodos[0:2], label_elementos[0], label_nodos[0:2]), FadeIn(mr_elemento_1_4),
        #           FadeIn(f_internas_elemento_1), FadeIn(cargas_e_1))
        # self.play(
        #     ReplacementTransform(mr_elemento_1_4[0], mr_elemento_1_4_1[0]),
        #     ReplacementTransform(mr_elemento_1_4[1], mr_elemento_1_4_1[1]),
        #     ReplacementTransform(mr_elemento_1_4[2], mr_elemento_1_4_1[2]),
        #     ReplacementTransform(mr_elemento_1_4[3], mr_elemento_1_4_1[3]),
        #     ReplacementTransform(mr_elemento_1_4[4], mr_elemento_1_4_1[4]),
        #     ReplacementTransform(mr_elemento_1_4[5], mr_elemento_1_4_1[5]),
        #     ReplacementTransform(mr_elemento_1_4[6], mr_elemento_1_4_1[6]),
        #     run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(mr_elemento_1_4_1[3].get_entries(), mr_elemento_1_4_1[4].get_entries()),
        #                                mr_elemento_1_4_2[2].get_entries()),
        #           ReplacementTransform(mr_elemento_1_4_1[3].get_brackets()[0],
        #                                mr_elemento_1_4_2[2].get_brackets()[0]),
        #           ReplacementTransform(mr_elemento_1_4_1[4].get_brackets()[1],
        #                                mr_elemento_1_4_2[2].get_brackets()[1]),
        #           ReplacementTransform(mr_elemento_1_4_1[0], mr_elemento_1_4_2[0]),
        #           ReplacementTransform(mr_elemento_1_4_1[1], mr_elemento_1_4_2[1]),
        #           ReplacementTransform(mr_elemento_1_4_1[5], mr_elemento_1_4_2[3]),
        #           ReplacementTransform(mr_elemento_1_4_1[6], mr_elemento_1_4_2[4]),
        #           FadeOut(mr_elemento_1_4_1[2]),
        #           FadeOut(mr_elemento_1_4_1[3].get_brackets()[1]),
        #           FadeOut(mr_elemento_1_4_1[4].get_brackets()[0]),
        #           run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(mr_elemento_1_4_2[2].get_entries(), mr_elemento_1_4_2[4].get_entries()),
        #                                mr_elemento_1_4_3[2].get_entries()),
        #           ReplacementTransform(mr_elemento_1_4_2[2].get_brackets()[0],
        #                                mr_elemento_1_4_3[2].get_brackets()[0]),
        #           ReplacementTransform(mr_elemento_1_4_2[4].get_brackets()[1],
        #                                mr_elemento_1_4_3[2].get_brackets()[1]),
        #           ReplacementTransform(mr_elemento_1_4_2[0], mr_elemento_1_4_3[0]),
        #           ReplacementTransform(mr_elemento_1_4_2[1], mr_elemento_1_4_3[1]),
        #           FadeOut(mr_elemento_1_4_2[3]),
        #           FadeOut(mr_elemento_1_4_2[2].get_brackets()[1]),
        #           FadeOut(mr_elemento_1_4_2[4].get_brackets()[0]),
        #           run_time=4)
        # self.wait(2)
        # self.play(mr_elemento_1_4_3.animate.to_corner(DOWN + LEFT), run_time=4)
        # self.wait(2)
        # self.play(Write(ecuacion_v_e_1))
        # self.wait(2)
        # self.play(Write(ecuacion_m_e_1))
        # self.wait(2)
        # self.play(FadeOut(mr_elemento_1_4_3), FadeOut(ec_e_1),
        #           FadeOut(elementos[0], nodos[0:2], label_elementos[0], label_nodos[0:2]),
        #           FadeOut(f_internas_elemento_1), FadeOut(cargas_e_1))
        # self.wait(2)
        # mr_elemento_1_4_4.move_to(ORIGIN)
        # self.play(FadeIn(mr_elemento_1_4_4))
        # self.wait(2)
        # self.play(FadeOut(mr_elemento_1_4_4))
        # ####################################
        # tit = titulo("Fuerzas internas del elemento 2", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # self.play(FadeIn(elementos[1], nodos[1:3], label_elementos[1], label_nodos[1:3]), FadeIn(mr_elemento_2_4),
        #           FadeIn(cargas_e_2), FadeIn(f_internas_elemento_2))
        # self.play(
        #     ReplacementTransform(mr_elemento_2_4[0], mr_elemento_2_4_1[0]),
        #     ReplacementTransform(mr_elemento_2_4[1], mr_elemento_2_4_1[1]),
        #     ReplacementTransform(mr_elemento_2_4[2], mr_elemento_2_4_1[2]),
        #     ReplacementTransform(mr_elemento_2_4[3], mr_elemento_2_4_1[3]),
        #     ReplacementTransform(mr_elemento_2_4[4], mr_elemento_2_4_1[4]),
        #     ReplacementTransform(mr_elemento_2_4[5], mr_elemento_2_4_1[5]),
        #     ReplacementTransform(mr_elemento_2_4[6], mr_elemento_2_4_1[6]),
        #     run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(mr_elemento_2_4_1[3].get_entries(), mr_elemento_2_4_1[4].get_entries()),
        #                                mr_elemento_2_4_2[2].get_entries()),
        #           ReplacementTransform(mr_elemento_2_4_1[3].get_brackets()[0],
        #                                mr_elemento_2_4_2[2].get_brackets()[0]),
        #           ReplacementTransform(mr_elemento_2_4_1[4].get_brackets()[1],
        #                                mr_elemento_2_4_2[2].get_brackets()[1]),
        #           ReplacementTransform(mr_elemento_2_4_1[0], mr_elemento_2_4_2[0]),
        #           ReplacementTransform(mr_elemento_2_4_1[1], mr_elemento_2_4_2[1]),
        #           ReplacementTransform(mr_elemento_2_4_1[5], mr_elemento_2_4_2[3]),
        #           ReplacementTransform(mr_elemento_2_4_1[6], mr_elemento_2_4_2[4]),
        #           FadeOut(mr_elemento_2_4_1[2]),
        #           FadeOut(mr_elemento_2_4_1[3].get_brackets()[1]),
        #           FadeOut(mr_elemento_2_4_1[4].get_brackets()[0]),
        #           run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(mr_elemento_2_4_2[2].get_entries(), mr_elemento_2_4_2[4].get_entries()),
        #                                mr_elemento_2_4_3[2].get_entries()),
        #           ReplacementTransform(mr_elemento_2_4_2[2].get_brackets()[0],
        #                                mr_elemento_2_4_3[2].get_brackets()[0]),
        #           ReplacementTransform(mr_elemento_2_4_2[4].get_brackets()[1],
        #                                mr_elemento_2_4_3[2].get_brackets()[1]),
        #           ReplacementTransform(mr_elemento_2_4_2[0], mr_elemento_2_4_3[0]),
        #           ReplacementTransform(mr_elemento_2_4_2[1], mr_elemento_2_4_3[1]),
        #           FadeOut(mr_elemento_2_4_2[3]),
        #           FadeOut(mr_elemento_2_4_2[2].get_brackets()[1]),
        #           FadeOut(mr_elemento_2_4_2[4].get_brackets()[0]),
        #           run_time=4)
        # self.wait(2)
        # self.play(mr_elemento_2_4_3.animate.to_corner(DOWN + LEFT), run_time=4)
        # self.wait(2)
        # self.play(Write(ecuacion_v_e_2))
        # self.wait(2)
        # self.play(Write(ecuacion_m_e_2))
        # self.wait(2)
        # self.play(FadeOut(mr_elemento_2_4_3), FadeOut(ec_e_2),
        #           FadeOut(elementos[1], nodos[1:3], label_elementos[1], label_nodos[1:3]),
        #           FadeOut(f_internas_elemento_2), FadeOut(cargas_e_2))
        # self.wait(2)
        # mr_elemento_2_4_4.move_to(ORIGIN)
        # self.play(FadeIn(mr_elemento_2_4_4))
        # self.wait(2)
        # self.play(FadeOut(mr_elemento_2_4_4))
        # ####################################
        # tit = titulo("Fuerzas internas del elemento 3", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # self.play(FadeIn(elementos[2], nodos[2:4], label_elementos[2], label_nodos[2:4]), FadeIn(mr_elemento_3_4),
        #           FadeIn(f_internas_elemento_3))
        # self.play(
        #     ReplacementTransform(mr_elemento_3_4[0], mr_elemento_3_4_1[0]),
        #     ReplacementTransform(mr_elemento_3_4[1], mr_elemento_3_4_1[1]),
        #     ReplacementTransform(mr_elemento_3_4[2], mr_elemento_3_4_1[2]),
        #     ReplacementTransform(mr_elemento_3_4[3], mr_elemento_3_4_1[3]),
        #     ReplacementTransform(mr_elemento_3_4[4], mr_elemento_3_4_1[4]),
        #     ReplacementTransform(mr_elemento_3_4[5], mr_elemento_3_4_1[5]),
        #     ReplacementTransform(mr_elemento_3_4[6], mr_elemento_3_4_1[6]),
        #     run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(mr_elemento_3_4_1[3].get_entries(), mr_elemento_3_4_1[4].get_entries()),
        #                                mr_elemento_3_4_2[2].get_entries()),
        #           ReplacementTransform(mr_elemento_3_4_1[3].get_brackets()[0],
        #                                mr_elemento_3_4_2[2].get_brackets()[0]),
        #           ReplacementTransform(mr_elemento_3_4_1[4].get_brackets()[1],
        #                                mr_elemento_3_4_2[2].get_brackets()[1]),
        #           ReplacementTransform(mr_elemento_3_4_1[0], mr_elemento_3_4_2[0]),
        #           ReplacementTransform(mr_elemento_3_4_1[1], mr_elemento_3_4_2[1]),
        #           ReplacementTransform(mr_elemento_3_4_1[5], mr_elemento_3_4_2[3]),
        #           ReplacementTransform(mr_elemento_3_4_1[6], mr_elemento_3_4_2[4]),
        #           FadeOut(mr_elemento_3_4_1[2]),
        #           FadeOut(mr_elemento_3_4_1[3].get_brackets()[1]),
        #           FadeOut(mr_elemento_3_4_1[4].get_brackets()[0]),
        #           run_time=4)
        # self.wait(2)
        # self.play(ReplacementTransform(VGroup(mr_elemento_3_4_2[2].get_entries(), mr_elemento_3_4_2[4].get_entries()),
        #                                mr_elemento_3_4_3[2].get_entries()),
        #           ReplacementTransform(mr_elemento_3_4_2[2].get_brackets()[0],
        #                                mr_elemento_3_4_3[2].get_brackets()[0]),
        #           ReplacementTransform(mr_elemento_3_4_2[4].get_brackets()[1],
        #                                mr_elemento_3_4_3[2].get_brackets()[1]),
        #           ReplacementTransform(mr_elemento_3_4_2[0], mr_elemento_3_4_3[0]),
        #           ReplacementTransform(mr_elemento_3_4_2[1], mr_elemento_3_4_3[1]),
        #           FadeOut(mr_elemento_3_4_2[3]),
        #           FadeOut(mr_elemento_3_4_2[2].get_brackets()[1]),
        #           FadeOut(mr_elemento_3_4_2[4].get_brackets()[0]),
        #           run_time=4)
        # self.wait(2)
        # self.play(mr_elemento_3_4_3.animate.to_corner(DOWN + LEFT), run_time=4)
        # self.wait(2)
        # self.play(Write(ecuacion_v_e_3))
        # self.wait(2)
        # self.play(Write(ecuacion_m_e_3))
        # self.wait(2)
        # self.play(FadeOut(mr_elemento_3_4_3), FadeOut(ec_e_3),
        #           FadeOut(elementos[2], nodos[2:4], label_elementos[2], label_nodos[2:4]),
        #           FadeOut(f_internas_elemento_3))
        # self.wait(2)
        # mr_elemento_3_4_4.move_to(ORIGIN)
        # self.play(FadeIn(mr_elemento_3_4_4))
        # self.wait(2)
        # self.play(FadeOut(mr_elemento_3_4_4))
        # #######################################################################################################
        # tit = titulo("Diagrama de cortantes", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # x = sp.Symbol('x')
        # v_1 = e_1.ecuacion_de_cortante().rhs.args[0].args[0]
        # v_2 = e_1.ecuacion_de_cortante().rhs.args[1].args[0]
        # v_3 = e_2.ecuacion_de_cortante().rhs.args[0].args[0]
        # v_4 = e_3.ecuacion_de_cortante().rhs.args[0].args[0]
        # nuevos_argumentos = []
        # for sub_piecewise, condicion_externa in mg.ecuacion_de_momento().rhs.args:
        #     nuevos_argumentos.extend(sub_piecewise.args)
        # m = sp.Piecewise(*nuevos_argumentos)
        # m_1 = e_1.ecuacion_de_momento().rhs.args[0].args[0]
        # m_2 = e_1.ecuacion_de_momento().rhs.args[1].args[0]
        # m_3 = e_2.ecuacion_de_momento().rhs.args[0].args[0]
        # m_4 = e_3.ecuacion_de_momento().rhs.args[0].args[0]
        #
        # f_v_1 = sp.lambdify(x, v_1, 'numpy')
        # f_v_2 = sp.lambdify(x, v_2, 'numpy')
        # f_v_3 = sp.lambdify(x, v_3, 'numpy')
        # f_v_4 = sp.lambdify(x, v_4, 'numpy')
        # f_m = sp.lambdify(x, m, 'numpy')
        # f_m_1 = sp.lambdify(x, m_1, 'numpy')
        # f_m_2 = sp.lambdify(x, m_2, 'numpy')
        # f_m_3 = sp.lambdify(x, m_3, 'numpy')
        # f_m_4 = sp.lambdify(x, m_4, 'numpy')
        #
        # # 3. Crear los Ejes
        # ejes_v = Axes(
        #     x_range=[0, 26, 5],
        #     y_range=[-120, 125, 25],
        #     axis_config={"include_numbers": True, "tip_shape": StealthTip, "font_size": 18, }
        # )
        # titulos_ejes_v = ejes_v.get_axis_labels(
        #     x_label=MathTex("x (m)", font_size=20),
        #     y_label=MathTex("Cortante (kN)", font_size=20)
        # ).set_color(BLUE_A)
        # # ejes_v.add_coordinates(
        # #     x_label="x (m)",
        # #     y_label="Cortante (kN)"
        # # )
        # titulo_v = Text("Diagrama de cortante", font_size=28)
        # titulo_v.next_to(ejes_v, UP, buff=0.1)
        # ejes_m = Axes(
        #     x_range=[0, 26, 5],
        #     y_range=[-180, 140, 25],
        #     axis_config={"include_numbers": True, "tip_shape": StealthTip, "font_size": 18, }
        # )
        # titulos_ejes_m = ejes_v.get_axis_labels(
        #     x_label=MathTex("x (m)", font_size=20),
        #     y_label=MathTex(r"Momento (kN \cdot m)", font_size=20)
        # ).set_color(BLUE_A)
        # # ejes_m.add_coordinates(
        # #     x_label="x (m)",
        # #     y_label=r"Momento (kN \cdot m)"
        # # )
        # titulo_m = Text("Diagrama de momento", font_size=28)
        # titulo_m.next_to(ejes_m, UP, buff=0.1)
        # curva_v_1 = ejes_v.plot(f_v_1, x_range=[0, 6], color=BLUE_E)
        # curva_v_2 = ejes_v.plot(f_v_2, x_range=[6, 10], color=BLUE_E)
        # curva_v_3 = ejes_v.plot(f_v_3, x_range=[10, 20], color=BLUE_E)
        # curva_v_4 = ejes_v.plot(f_v_4, x_range=[20, 25], color=BLUE_E)
        # label_v_1_1 = MathTex(f'{f_v_1(0):.3g}', color=ORANGE).next_to(ejes_v.c2p(0, f_v_1(0), 0), UP, buff=0.0).shift(
        #     RIGHT * 0.2).scale(0.35)
        # label_v_1_2 = MathTex(f'{f_v_1(6):.3g}', color=ORANGE).next_to(ejes_v.c2p(6, f_v_1(6), 0), UP, buff=0.0).scale(
        #     0.35)
        # label_v_2_1 = MathTex(f'{f_v_2(6):.3g}', color=ORANGE).next_to(ejes_v.c2p(6, f_v_2(6), 0), DOWN,
        #                                                                buff=0.0).scale(0.35)
        # label_v_2_2 = MathTex(f'{f_v_2(10):.3g}', color=ORANGE).next_to(ejes_v.c2p(10, f_v_2(10), 0), DOWN,
        #                                                                 buff=0.0).scale(0.35)
        # label_v_3_1 = MathTex(f'{f_v_3(10):.3g}', color=ORANGE).next_to(ejes_v.c2p(10, f_v_3(10), 0), UP,
        #                                                                 buff=0.0).scale(0.35)
        # label_v_3_2 = MathTex(f'{f_v_3(20):.3g}', color=ORANGE).next_to(ejes_v.c2p(20, f_v_3(20), 0), DOWN,
        #                                                                 buff=0.0).scale(0.35)
        # label_v_4_1 = MathTex(f'{f_v_4(20):.3g}', color=ORANGE).next_to(ejes_v.c2p(20, f_v_4(20), 0), UP,
        #                                                                 buff=0.0).scale(0.35)
        # label_v_4_2 = MathTex(f'{f_v_4(25):.3g}', color=ORANGE).next_to(ejes_v.c2p(25, f_v_4(25), 0), UP,
        #                                                                 buff=0.0).scale(0.35)
        # curva_m = ejes_m.plot(f_m, x_range=[0, 25, 0.05], color=BLUE_E)
        # # curva_m_1 = ejes_m.plot(f_m_1, x_range=[0, 6], color=BLUE_E)
        # # curva_m_2 = ejes_m.plot(f_m_2, x_range=[6, 10], color=BLUE_E)
        # # curva_m_3 = ejes_m.plot(f_m_3, x_range=[10, 20, 0.1], color=BLUE_E)
        # # curva_m_4 = ejes_m.plot(f_m_4, x_range=[20, 25], color=BLUE_E)
        # label_m_1_1 = MathTex(f'{f_m_1(0):.3g}', color=ORANGE).next_to(ejes_m.c2p(0, f_m_1(0), 0), DOWN,
        #                                                                buff=0.0).shift(
        #     RIGHT * 0.2).scale(0.35)
        # label_m_1_2 = MathTex(f'{f_m_1(6):.3g}', color=ORANGE).next_to(ejes_m.c2p(6, f_m_1(6), 0), UP, buff=0.0).scale(
        #     0.35)
        # # label_m_2_1 = MathTex(f'{f_m_2(6):.3g}', color=ORANGE).next_to(ejes_m.c2p(6, f_m_2(6), 0), DOWN,
        # #                                                                buff=0.0).scale(
        # #     0.35)
        # label_m_2_2 = MathTex(f'{f_m_2(10):.3g}', color=ORANGE).next_to(ejes_m.c2p(10, f_m_2(10), 0), DOWN,
        #                                                                 buff=0.0).scale(0.35)
        # label_m_3_1 = MathTex(f'{f_m_3(15.0956521739130):.3g}', color=ORANGE).next_to(
        #     ejes_m.c2p(15.0956521739130, f_m_3(15.0956521739130), 0), UP,
        #     buff=0.0).scale(0.35)
        # label_m_3_2 = MathTex(f'{f_m_3(20):.3g}', color=ORANGE).next_to(ejes_m.c2p(20, f_m_3(20), 0), DOWN,
        #                                                                 buff=0.0).scale(0.35)
        # # label_m_4_1 = MathTex(f'{f_m_4(20):.3g}', color=ORANGE).next_to(ejes_m.c2p(20, f_m_4(20), 0), UP,
        # #                                                                 buff=0.0).scale(0.35)
        # label_m_4_2 = MathTex(f'{f_m_4(25):.3g}', color=ORANGE).next_to(ejes_m.c2p(25, f_m_4(25), 0), UP,
        #                                                                 buff=0.0).scale(0.35)
        # self.play(Create(ejes_v), Write(titulos_ejes_v), Write(titulo_v), run_time=4)
        # t_tracker_v = ValueTracker(0)
        #
        # def update_area_v_1():
        #     t = t_tracker_v.get_value()
        #     if t <= 0:
        #         return VGroup()
        #     return ejes_v.get_area(curva_v_1, x_range=(0, min(t, 6)), color=BLUE, opacity=0.3)
        #
        # area_1_dinamica_v = always_redraw(update_area_v_1)
        #
        # def update_area_v_2():
        #     t = t_tracker_v.get_value()
        #     if t <= 6:
        #         return VGroup()
        #     return ejes_v.get_area(curva_v_2, x_range=(6, min(t, 10)), color=BLUE, opacity=0.3)
        #
        # area_2_dinamica_v = always_redraw(update_area_v_2)
        #
        # def update_area_v_3():
        #     t = t_tracker_v.get_value()
        #     if t <= 10:
        #         return VGroup()
        #     return ejes_v.get_area(curva_v_3, x_range=(10, min(t, 20)), color=BLUE, opacity=0.3)
        #
        # area_3_dinamica_v = always_redraw(update_area_v_3)
        #
        # def update_area_v_4():
        #     t = t_tracker_v.get_value()
        #     if t <= 20:
        #         return VGroup()
        #     return ejes_v.get_area(curva_v_4, x_range=(20, min(t, 25)), color=BLUE, opacity=0.3)
        #
        # area_4_dinamica_v = always_redraw(update_area_v_4)
        # self.add(area_1_dinamica_v, area_2_dinamica_v, area_3_dinamica_v, area_4_dinamica_v)
        # self.play(Write(label_v_1_1))
        # self.play(t_tracker_v.animate.set_value(6), run_time=4, rate_func=linear)
        # self.play(Write(label_v_1_2))
        # self.wait(0.5)
        # self.play(Write(label_v_2_1))
        # self.play(t_tracker_v.animate.set_value(10), run_time=4, rate_func=linear)
        # self.play(Write(label_v_2_2))
        # self.wait(0.5)
        # self.play(Write(label_v_3_1))
        # self.play(t_tracker_v.animate.set_value(20), run_time=4, rate_func=linear)
        # self.play(Write(label_v_3_2))
        # self.wait(0.5)
        # self.play(Write(label_v_4_1))
        # self.play(t_tracker_v.animate.set_value(25), run_time=4, rate_func=linear)
        # self.play(Write(label_v_4_2))
        # self.wait(2)
        # self.play(
        #     FadeOut(titulos_ejes_v, titulo_v, ejes_v, label_v_1_1, label_v_1_2, label_v_2_1, label_v_2_2, label_v_3_1,
        #             label_v_3_2, label_v_4_1,
        #             label_v_4_2, curva_v_1, curva_v_2, curva_v_3, curva_v_4, area_1_dinamica_v, area_2_dinamica_v,
        #             area_3_dinamica_v, area_4_dinamica_v))
        # tit = titulo("Diagrama de momento", size_titulo=36)
        # self.play(Write(tit[0]))
        # self.play(Create(tit[1]))
        # self.wait(2)
        # self.play(FadeOut(tit))
        # self.play(Create(ejes_m), Write(titulos_ejes_m), Write(titulo_m), run_time=4)
        # t_tracker_m = ValueTracker(0)
        #
        # def update_area_m():
        #     t = t_tracker_m.get_value()
        #     if t <= 0:
        #         return VGroup()
        #     return ejes_m.get_area(curva_m, x_range=(0, min(t, 25)), color=BLUE, opacity=0.3)
        #
        # area_dinamica_m = always_redraw(update_area_m)
        #
        # # def update_area_m_1():
        # #     t = t_tracker_m.get_value()
        # #     if t <= 0:
        # #         return VGroup()
        # #     return ejes_m.get_area(curva_m_1, x_range=(0, min(t, 10)), color=BLUE, opacity=0.3)
        # #
        # # area_1_dinamica_m = always_redraw(update_area_m_1)
        # #
        # # def update_area_m_2():
        # #     t = t_tracker_m.get_value()
        # #     if t <= 10:
        # #         return VGroup()
        # #     return ejes_m.get_area(curva_m_3, x_range=(10, min(t, 20)), color=BLUE, opacity=0.3)
        # #
        # # area_2_dinamica_m = always_redraw(update_area_m_2)
        # #
        # # def update_area_m_3():
        # #     t = t_tracker_m.get_value()
        # #     if t <= 20:
        # #         return VGroup()
        # #     return ejes_m.get_area(curva_m_4, x_range=(20, min(t, 25)), color=BLUE, opacity=0.3)
        # #
        # # area_3_dinamica_m = always_redraw(update_area_m_3)
        #
        # # def update_area_m_4():
        # #     t = t_tracker_m.get_value()
        # #     if t <= 20:
        # #         return VGroup()
        # #     return ejes_m.get_area(curva_m_4, x_range=(20, min(t, 25)), color=BLUE, opacity=0.3)
        # #
        # # area_4_dinamica_m = always_redraw(update_area_m_4)
        # self.add(area_dinamica_m)
        # self.play(Write(label_m_1_1))
        # self.play(t_tracker_m.animate.set_value(6), run_time=4, rate_func=linear)
        # self.play(Write(label_m_1_2))
        # self.wait(0.5)
        # # self.play(Write(label_m_2_1))
        # self.play(t_tracker_m.animate.set_value(10), run_time=4, rate_func=linear)
        # self.play(Write(label_m_2_2))
        # self.wait(0.5)
        # self.play(t_tracker_m.animate.set_value(15.0956521739130), run_time=4, rate_func=linear)
        # self.play(Write(label_m_3_1))
        # self.wait(0.5)
        # self.play(t_tracker_m.animate.set_value(20), run_time=4, rate_func=linear)
        # self.play(Write(label_m_3_2))
        # self.wait(0.5)
        # # self.play(Write(label_m_4_1))
        # self.play(t_tracker_m.animate.set_value(25), run_time=4, rate_func=linear)
        # self.play(Write(label_m_4_2))
        # self.wait(2)
        # self.play(
        #     FadeOut(titulos_ejes_m, titulo_m, ejes_m, label_m_1_1, label_m_1_2, label_m_2_2, label_m_3_1, label_m_3_2,
        #             label_m_4_2, curva_m, area_dinamica_m))


class pruebas(Scene):
    def construct(self) -> None:
        # etiquetas = [MathTex('Nodo'), MathTex('x[m]'), MathTex('GL[y]'), MathTex(r'GL[\phi]')]
        # rows = [[1, 0.0, 'Restringido', 'Restringido'],
        #         [2, 10.0, 'Restringido', 'Libre'],
        #         [3, 20.0, 'Restringido', 'Libre'],
        #         [4, 25.0, 'Restringido', 'Restringido']]
        # tab_nodos = elemento_tabla(etiquetas, rows).scale(0.5).to_edge(DOWN, buff=0.5)
        # etiquetas = [MathTex('Elemento'), MathTex(r'Nodo_i'), MathTex(r'Nodo_j'), MathTex('EI')]
        # rows = [[1, 1, 2, 'cte'],
        #         [2, 2, 3, 'cte'],
        #         [3, 3, 4, 'cte']]
        # tab_elementos = elemento_tabla(etiquetas, rows).scale(0.5).to_edge(DOWN, buff=0.5)
        # VGroup(tab_nodos, tab_elementos).arrange(RIGHT, buff=1).to_edge(DOWN, buff=0.5)
        # self.play(Create(tab_nodos[1]), Create(tab_nodos[2]), run_time=1)
        # self.play(FadeIn(tab_nodos[0].get_rows()))
        # self.wait(2)
        # self.play(Create(tab_elementos[1]), Create(tab_elementos[2]), run_time=1)
        # self.play(FadeIn(tab_elementos[0].get_rows()))
        # self.wait(2)
        # self.play(FadeOut(tab_nodos, tab_elementos), run_time=2)
        punto_a_1 = 2 * LEFT
        punto_b_1 = 2 * RIGHT
        punto_a_2 = 2 * LEFT
        punto_b_2 = 2 * RIGHT
        punto_a_final = 3 * LEFT
        punto_b_final = 3 * RIGHT

        # Instanciamos nuestro objeto personalizado
        mi_resorte = Resorte(punto_a_1, punto_b_1, n=40)
        # porc_h= 0.1 por defecto, se cambia para que no aumente el d del resorte visualmente
        mi_resorte_2 = Resorte(punto_a_final, punto_b_final, n=40, porc_h=2 / 30)
        n_a_1 = Dot(punto_a_1, radius=0.05, color=GRAY)
        n_b_1 = Dot(punto_b_1, radius=0.05, color=GRAY)
        n_a_2 = Dot(punto_a_2, radius=0.05, color=RED_D).set_z_index(1)
        n_b_2 = Dot(punto_b_2, radius=0.05, color=RED_D).set_z_index(1)

        label_1 = LabeledDot(MathTex('1', color=WHITE), color=BLUE, stroke_color=BLUE, stroke_width=1,
                             fill_opacity=0.8).next_to(punto_a_1, UP, buff=-0.1).scale(0.35)
        label_2 = LabeledDot(MathTex('2', color=WHITE), color=BLUE, stroke_color=BLUE, stroke_width=1,
                             fill_opacity=0.8).next_to(punto_b_1, UP, buff=-0.1).scale(0.35)
        T_1 = Arrow(
            start=punto_a_1,
            end=punto_a_1 + LEFT,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=RED,
            stroke_width=4,  # Grosor de la línea
            tip_shape=StealthTip,  # Aquí cambias la forma
            max_tip_length_to_length_ratio=0.15  # Controla el tamaño de la punta
        )
        T_2 = Arrow(
            start=punto_b_1,
            end=punto_b_1 + RIGHT,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=RED,
            stroke_width=4,  # Grosor de la línea
            tip_shape=StealthTip,  # Aquí cambias la forma
            max_tip_length_to_length_ratio=0.15  # Controla el tamaño de la punta
        )
        label_T_1 = MathTex('T', color=RED).next_to(punto_a_1 + LEFT, LEFT, buff=0).scale(0.5)
        label_T_2 = MathTex('T', color=RED).next_to(punto_b_1 + RIGHT, RIGHT, buff=0).scale(0.5)
        cota_L = crear_cota(punto_a_1 + DOWN, punto_b_1 + DOWN, 'L', color=GRAY_A)
        cota_1 = crear_cota(punto_a_1 + DOWN, punto_a_final + DOWN, 'u_1', color=GRAY_A)
        cota_2 = crear_cota(punto_b_1 + DOWN, punto_b_final + DOWN, 'u_2', color=GRAY_A)
        eje_x = elemento_direccion_eje(UP, 0.5, ang=0.0, color=WHITE)
        eje_u_1 = elemento_direccion_eje(punto_a_1 + UP, 0.5, ang=0.0, color=WHITE)
        eje_u_2 = elemento_direccion_eje(punto_b_1 + UP, 0.5, ang=0.0, color=WHITE)
        label_dir_x = MathTex('x', color=WHITE).next_to(eje_x, RIGHT, buff=0).scale(0.5)
        label_dir_u_1 = MathTex('f_{1x},u_1', color=WHITE).next_to(eje_u_1, RIGHT, buff=0).scale(0.5)
        label_dir_u_2 = MathTex('f_{2x},u_2', color=WHITE).next_to(eje_u_2, RIGHT, buff=0).scale(0.5)
        dir_u_1 = VGroup(eje_u_1, label_dir_u_1)
        dir_u_2 = VGroup(eje_u_2, label_dir_u_2)
        dir_x = VGroup(eje_x, label_dir_x)
        ecuacion_delta = VGroup(MathTex(r'\delta'), ecuacion_signo_igual(), MathTex('u_2'), ecuacion_signo_menos(),
                                MathTex('u_1')).arrange(RIGHT)
        ecuacion_T = VGroup(MathTex('T'), ecuacion_signo_igual(), MathTex('k'), MathTex(r'\delta')).arrange(RIGHT)
        ecuacion_T_2 = VGroup(MathTex('T'), ecuacion_signo_igual(), MathTex('k'), MathTex('('), MathTex('u_2'),
                              ecuacion_signo_menos(),
                              MathTex('u_1'), MathTex(')')).arrange(RIGHT).scale(0.5)
        ecuacion_f_1_1 = VGroup(MathTex('f_{1x}'), ecuacion_signo_igual(), ecuacion_signo_menos(),
                                MathTex('T')).arrange(RIGHT)
        ecuacion_f_1_2 = VGroup(MathTex('f_{1x}'), ecuacion_signo_igual(), ecuacion_signo_menos(), MathTex('k'),
                                MathTex('('), MathTex('u_2'), ecuacion_signo_menos(),
                                MathTex('u_1'), MathTex(')')).arrange(RIGHT).scale(0.5)
        ecuacion_f_1_3 = VGroup(MathTex('f_{1x}'), ecuacion_signo_igual(), MathTex('k'), MathTex('('), MathTex('u_1'),
                                ecuacion_signo_menos(),
                                MathTex('u_2'), MathTex(')')).arrange(RIGHT).scale(0.5)
        ecuacion_f_1_4 = VGroup(MathTex('f_{1x}'), ecuacion_signo_igual(), MathTex('('), MathTex('k'), MathTex('u_1'),
                                ecuacion_signo_menos(), MathTex('k'), MathTex('u_2'), MathTex(')')).arrange(
            RIGHT).scale(0.5)
        ecuacion_f_2_1 = VGroup(MathTex('f_{2x}'), ecuacion_signo_igual(), MathTex('T')).arrange(RIGHT)
        ecuacion_f_2_2 = VGroup(MathTex('f_{2x}'), ecuacion_signo_igual(), MathTex('k'), MathTex('('), MathTex('u_2'),
                                ecuacion_signo_menos(),
                                MathTex('u_1'), MathTex(')')).arrange(RIGHT).scale(0.5)
        ecuacion_f_2_3 = VGroup(MathTex('f_{2x}'), ecuacion_signo_igual(), ecuacion_signo_menos(), MathTex('k'),
                                MathTex('('), MathTex('u_1'), ecuacion_signo_menos(),
                                MathTex('u_2'), MathTex(')')).arrange(RIGHT).scale(0.5)
        ecuacion_f_2_4 = VGroup(MathTex('f_{2x}'), ecuacion_signo_igual(), MathTex('('), ecuacion_signo_menos(),
                                MathTex('k'), MathTex('u_1'), ecuacion_signo_mas(), MathTex('k'),
                                MathTex('u_2'), MathTex(')')).arrange(RIGHT).scale(0.5)
        ecuacion_local_resorte_1 = VGroup(Matrix([['f_{1x}'], ['f_{2x}']], left_bracket=r"\{", right_bracket=r"\}"),
                                          ecuacion_signo_igual(),
                                          Matrix([['k', '-k'], ['-k', 'k']]),
                                          Matrix([['u_1'], ['u_2']], left_bracket=r"\{", right_bracket=r"\}")
                                          ).arrange(RIGHT).scale(0.5).move_to(DOWN * 3.2)
        ecuacion_local_resorte_2 = VGroup(Matrix([['f']], left_bracket=r"\{", right_bracket=r"\}"),
                                          ecuacion_signo_igual(),
                                          Matrix([['k']]), Matrix([['d']], left_bracket=r"\{", right_bracket=r"\}")
                                          ).arrange(RIGHT).scale(0.5).move_to(DOWN * 3)
        grupo_ecuaciones_1 = VGroup(ecuacion_delta, ecuacion_T, ecuacion_f_1_1, ecuacion_f_2_1).arrange(DOWN,
                                                                                                        buff=0.2).scale(
            0.5).move_to(DOWN * 2)
        ecuacion_T_2.move_to(grupo_ecuaciones_1[1])
        ecuacion_f_1_2.move_to(grupo_ecuaciones_1[2])
        ecuacion_f_1_3.move_to(grupo_ecuaciones_1[2])
        ecuacion_f_1_4.move_to(grupo_ecuaciones_1[2])
        ecuacion_f_2_2.move_to(grupo_ecuaciones_1[3])
        ecuacion_f_2_3.move_to(grupo_ecuaciones_1[3])
        ecuacion_f_2_4.move_to(grupo_ecuaciones_1[3])
        # Animamos su aparición
        self.play(FadeIn(mi_resorte, n_a_1, n_b_1, n_a_2, n_b_2, label_1, label_2, cota_L), run_time=3)
        self.wait(2)
        self.play(FadeIn(T_1, T_2, label_T_1, label_T_2, dir_x, dir_u_1, dir_u_2), run_time=3)
        self.wait(2)
        self.play(ReplacementTransform(mi_resorte, mi_resorte_2),
                  n_a_2.animate.move_to(punto_a_final),
                  n_b_2.animate.move_to(punto_b_final),
                  label_1.animate.move_to(label_1.get_center() + LEFT),
                  label_2.animate.move_to(label_2.get_center() + RIGHT),
                  T_1.animate.move_to(punto_a_final + 0.5 * LEFT),
                  T_2.animate.move_to(punto_b_final + 0.5 * RIGHT),
                  label_T_1.animate.move_to(label_T_1.get_center() + LEFT),
                  label_T_2.animate.move_to(label_T_2.get_center() + RIGHT),
                  run_time=4)
        self.play(FadeIn(cota_1, cota_2), run_time=2)
        self.wait(2)
        self.play(FadeOut(n_a_1, n_b_1), run_time=1)
        self.wait(1)
        self.play(FadeIn(grupo_ecuaciones_1[0]), run_time=2)
        self.wait(2)
        self.play(FadeIn(grupo_ecuaciones_1[1]), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(grupo_ecuaciones_1[1][0], ecuacion_T_2[0]),
                  ReplacementTransform(grupo_ecuaciones_1[1][1], ecuacion_T_2[1]),
                  ReplacementTransform(grupo_ecuaciones_1[1][2], ecuacion_T_2[2]),
                  ReplacementTransform(grupo_ecuaciones_1[0][2], ecuacion_T_2[4]),
                  ReplacementTransform(grupo_ecuaciones_1[0][3], ecuacion_T_2[5]),
                  ReplacementTransform(grupo_ecuaciones_1[0][4], ecuacion_T_2[6]),
                  FadeIn(ecuacion_T_2[3], ecuacion_T_2[7]),
                  FadeOut(grupo_ecuaciones_1[0][0:2], grupo_ecuaciones_1[1][3]),
                  run_time=4)
        self.wait(2)
        self.play(FadeIn(grupo_ecuaciones_1[2:]))
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_T_2[2:].copy(), ecuacion_f_1_2[3:]),
                  ReplacementTransform(ecuacion_T_2[2:], ecuacion_f_2_2[2:]),
                  ReplacementTransform(grupo_ecuaciones_1[2][:3], ecuacion_f_1_2[:3]),
                  ReplacementTransform(grupo_ecuaciones_1[3][:2], ecuacion_f_2_2[:2]),
                  FadeOut(ecuacion_T_2[:2], grupo_ecuaciones_1[2][3], grupo_ecuaciones_1[3][2]),
                  run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_f_1_2[:2], ecuacion_f_1_3[:2]),
                  ReplacementTransform(ecuacion_f_1_2[3], ecuacion_f_1_3[2]),
                  ReplacementTransform(ecuacion_f_1_2[4], ecuacion_f_1_3[3]),
                  ReplacementTransform(ecuacion_f_1_2[5], ecuacion_f_1_3[6]),
                  ReplacementTransform(ecuacion_f_1_2[6], ecuacion_f_1_3[5]),
                  ReplacementTransform(ecuacion_f_1_2[7], ecuacion_f_1_3[4]),
                  ReplacementTransform(ecuacion_f_1_2[8], ecuacion_f_1_3[7]),

                  ReplacementTransform(ecuacion_f_2_2[:2], ecuacion_f_2_3[:2]),
                  ReplacementTransform(ecuacion_f_2_2[2], ecuacion_f_2_3[3]),
                  ReplacementTransform(ecuacion_f_2_2[3], ecuacion_f_2_3[4]),
                  ReplacementTransform(ecuacion_f_2_2[4], ecuacion_f_2_3[7]),
                  ReplacementTransform(ecuacion_f_2_2[5], ecuacion_f_2_3[6]),
                  ReplacementTransform(ecuacion_f_2_2[6], ecuacion_f_2_3[5]),
                  ReplacementTransform(ecuacion_f_2_2[7], ecuacion_f_2_3[8]),
                  FadeOut(ecuacion_f_1_2[2]),
                  FadeIn(ecuacion_f_2_3[2]),
                  run_time=4)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_f_1_3[:2], ecuacion_f_1_4[:2]),
                  ReplacementTransform(ecuacion_f_1_3[2].copy(), ecuacion_f_1_4[3]),
                  ReplacementTransform(ecuacion_f_1_3[2], ecuacion_f_1_4[6]),
                  ReplacementTransform(ecuacion_f_1_3[3], ecuacion_f_1_4[2]),
                  ReplacementTransform(ecuacion_f_1_3[4], ecuacion_f_1_4[4]),
                  ReplacementTransform(ecuacion_f_1_3[5], ecuacion_f_1_4[5]),
                  ReplacementTransform(ecuacion_f_1_3[6], ecuacion_f_1_4[7]),
                  ReplacementTransform(ecuacion_f_1_3[7], ecuacion_f_1_4[8]),

                  ReplacementTransform(ecuacion_f_2_3[:2], ecuacion_f_2_4[:2]),
                  ReplacementTransform(ecuacion_f_2_3[2:4].copy(), ecuacion_f_2_4[3:5]),
                  ReplacementTransform(VGroup(ecuacion_f_2_3[2], ecuacion_f_2_3[6]), ecuacion_f_2_4[6]),
                  ReplacementTransform(ecuacion_f_2_3[3], ecuacion_f_2_4[7]),
                  ReplacementTransform(ecuacion_f_2_3[4], ecuacion_f_2_4[2]),
                  ReplacementTransform(ecuacion_f_2_3[5], ecuacion_f_2_4[5]),
                  ReplacementTransform(ecuacion_f_2_3[7], ecuacion_f_2_4[8]),
                  ReplacementTransform(ecuacion_f_2_3[8], ecuacion_f_2_4[9]),
                  run_time=4)
        self.wait(2)
        self.play(FadeIn(ecuacion_local_resorte_1[0].get_brackets(), ecuacion_local_resorte_1[1],
                         ecuacion_local_resorte_1[2].get_brackets(), ecuacion_local_resorte_1[3].get_brackets()),
                  run_time=2)
        self.play(ReplacementTransform(ecuacion_f_1_4[0], ecuacion_local_resorte_1[0].get_entries()[0]),
                  ReplacementTransform(ecuacion_f_2_4[0], ecuacion_local_resorte_1[0].get_entries()[1]),
                  run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(ecuacion_f_1_4[3], ecuacion_local_resorte_1[2].get_entries()[0]),
                  ReplacementTransform(ecuacion_f_1_4[5], ecuacion_local_resorte_1[2].get_entries()[1][0][0]),
                  ReplacementTransform(ecuacion_f_1_4[6], ecuacion_local_resorte_1[2].get_entries()[1][0][1]),
                  ReplacementTransform(ecuacion_f_2_4[3], ecuacion_local_resorte_1[2].get_entries()[2][0][0]),
                  ReplacementTransform(ecuacion_f_2_4[4], ecuacion_local_resorte_1[2].get_entries()[2][0][1]),
                  ReplacementTransform(ecuacion_f_2_4[7], ecuacion_local_resorte_1[2].get_entries()[3]),
                  FadeOut(ecuacion_f_2_4[6]),
                  run_time=2)
        self.play(ReplacementTransform(VGroup(ecuacion_f_1_4[4], ecuacion_f_2_4[5]),
                                       ecuacion_local_resorte_1[3].get_entries()[0]),
                  ReplacementTransform(VGroup(ecuacion_f_1_4[7], ecuacion_f_2_4[8]),
                                       ecuacion_local_resorte_1[3].get_entries()[1]),
                  FadeOut(ecuacion_f_1_4[1:3], ecuacion_f_1_4[8]),
                  FadeOut(ecuacion_f_2_4[1:3], ecuacion_f_2_4[9]),
                  run_time=2)
        self.wait(2)
        self.play(ecuacion_local_resorte_1.animate.move_to(DOWN * 2),
                  run_time=2)
        self.wait(2)
        self.play(Write(ecuacion_local_resorte_2),
                  run_time=2)
        self.wait(2)


class pruebas2(Scene):
    def construct(self) -> None:
        punto_a_1 = 2 * LEFT
        punto_b_1 = 2 * RIGHT

        # Instanciamos nuestro objeto personalizado
        mi_resorte = Resorte(punto_a_1, punto_b_1, n=40)
        self.add(mi_resorte)
