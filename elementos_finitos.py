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
        # ejes_planos.to_edge(DOWN + LEFT)
        ejes = ejes_planos
        cargas = VGroup()
        for carga_puntual in mg._lista_cargas_puntuales:
            cp = elemento_carga((carga_puntual[1][0][0] + carga_puntual[2], 0.0, 0.0), ejes, 3, ang=90, saliente=False,
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
        mg.solucion()
        mg.diagrama_cargas()

        nodos = VGroup()
        label_nodos = VGroup().set_z_index(1.5)
        soportes = VGroup().set_z_index(1)
        for n in mg._lista_nodos:
            nodos.add(Dot(ejes.c2p(n.punto), color=BLUE_A))
            label_nodos.add(
                LabeledDot(MathTex(n.nombre, color=WHITE), color=GREEN).next_to(ejes.c2p(n.punto), DR, buff=-0.1).scale(
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
            rec = np.array([punto_medio + np.array([-0.15, 0.15, 0.0]), punto_medio + np.array([0.15, 0.15, 0.0]),
                            punto_medio + np.array([0.15, -0.15, 0.0]),
                            punto_medio + np.array([-0.15, -0.15, 0.0])])
            label_elementos.add(
                LabeledPolygram(rec, label=MathTex(el.nombre, color=WHITE).add_background_rectangle(
                    color=RED,  # Color del fondo del texto
                    opacity=0.8,  # Opacidad (1 = sólido, 0 = transparente)
                    buff=0.1  # La "márgen" o padding alrededor de las letras
                ), stroke_width=0, precision=0.0).scale(0.5).shift(np.array([0.0, -0.4, 0.0])))

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
        self.play(Write(enunciado), run_time=5)
        escena_inicial = VGroup(viga, soportes, cargas, cotas)
        escena_inicial.save_state()
        escena_inicial.to_edge(DOWN + LEFT)
        escena_elemento_1 = VGroup(elementos[0], nodos[0:2], soportes[0], label_elementos[0], label_nodos[0:2],
                                   cargas[0:2], cotas[0:2])
        escena = VGroup(nodos, elementos, soportes, label_elementos, label_nodos, cargas, cotas)

        self.play(FadeIn(escena_inicial), run_time=2)
        self.wait(5)
        self.play(FadeOut(enunciado), run_time=2)
        self.play(Restore(escena_inicial), run_time=2)
        self.wait(5)
        self.play(Create(ejes), run_time=2)
        self.play(FadeOut(viga), run_time=2)
        self.play(DrawBorderThenFill(nodos), DrawBorderThenFill(elementos), run_time=2)
        self.play(Write(label_nodos), Write(label_elementos), run_time=2)
        self.wait(5)

        # self.play(GrowFromEdge(elementos, edge=LEFT), run_time=2)
        # self.play(Create(cotas), run_time=2)
        # self.play(FadeIn(soportes), run_time=2)

        # self.play(FadeIn(label_elementos), run_time=2)
        # self.play(FadeIn(cargas), run_time=2)
        # self.wait(2)
        self.play(FadeOut(escena), run_time=2)
        self.play(FadeIn(escena_elemento_1), run_time=2)
        self.wait(2)