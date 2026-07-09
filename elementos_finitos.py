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
            y_range=[0, 12, 1],
            background_line_style={
                "stroke_opacity": 0.1  # Puedes atenuar las líneas de la cuadrícula si no las quieres ver
            }
        )
        ejes_planos.to_edge(DOWN + LEFT)
        ejes = ejes_coordenados
        ev_1 = elemento_viga(e_1.get_nodo_inicial().punto[0], e_1.get_nodo_final().punto[0], 0.25, ejes)
        ev_2 = elemento_viga(e_2.get_nodo_inicial().punto[0], e_2.get_nodo_final().punto[0], 0.25, ejes)
        ev_3 = elemento_viga(e_3.get_nodo_inicial().punto[0], e_3.get_nodo_final().punto[0], 0.25, ejes)
        cargas = VGroup()
        for carga_puntual in mg._lista_cargas_puntuales:
            cp = elemento_carga((carga_puntual[1][0][0]+carga_puntual[2], 0.0, 0.0),ejes,2,ang=90, saliente=False)
            valor = MathTex(str(abs(carga_puntual[0]))+r"\,kN").next_to(cp, UP, buff=0.1)
            cargas.add(cp)
            cargas.add(valor)
        for carga_distribuida in mg._lista_cargas_distribuidas:
            cp = elemento_carga_distribuida((carga_distribuida[1][0][0], 0.0, 0.0),(carga_distribuida[1][1][0], 0.0, 0.0), ejes, 0,
                                saliente=False)
            valor_1 = MathTex(str(abs(carga_distribuida[0][0])) + r"\,kN").next_to(cp, UL, buff=0.1)
            valor_2 = MathTex(str(abs(carga_distribuida[0][1])) + r"\,kN").next_to(cp, UR, buff=0.1)
            cargas.add(cp)
            cargas.add(valor_1)
            cargas.add(valor_2)
        self.play(FadeIn(ejes), run_time=2)
        self.play(FadeIn(ev_1, ev_2, ev_3), run_time=2)
        self.play(FadeIn(cargas), run_time=2)
        self.wait(2)

