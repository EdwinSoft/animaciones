from manim import *
import numpy as np


class NewtonRaphson(MovingCameraScene):
    def construct(self):
        # 1. Configurar los ejes cartesianos con longitudes fijas
        axes = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2.0, 2.0, 0.5],
            # x_length=7,  # Define el ancho físico en la pantalla (en unidades de Manim)
            # y_length=5,  # Define el alto físico en la pantalla
            axis_config={"include_tip": True}
        )
        # Centrar los ejes un poco si es necesario (opcional)
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # 2. Definir la función y su derivada usando Numpy
        def f(x):
            return np.exp(-x) - x

        def df(x):
            return -np.exp(-x) - 1

        # Dibujar la gráfica principal
        graph = axes.plot(f, color=BLUE, x_range=[-1, 3])
        graph_label = axes.get_graph_label(graph, label="e^{-x} - x", x_val=1, direction=UR)

        # Animación inicial: Aparecen los ejes y la curva
        self.play(Create(axes), Write(labels))
        self.play(Create(graph), Write(graph_label))
        self.wait(1)

        # 3. Proceso de Newton-Raphson
        x_n = 0  # Nuestro punto de partida inicial
        # Opcional: Guardamos el estado inicial de la cámara por si quieres alejarla al final
        self.camera.frame.save_state()

        # Realizamos 3 iteraciones para ver cómo converge
        for i in range(3):
            # Dibujar el punto actual en el eje X
            dot_x = Dot(axes.c2p(x_n, 0), color=YELLOW)
            label_x = MathTex(f"x_{i}").scale(0.7).next_to(dot_x, DL, buff=0.1)
            self.play(FadeIn(dot_x), Write(label_x))

            # Proyectar una línea vertical hasta tocar la curva f(x)
            y_n = f(x_n)
            dot_f = Dot(axes.c2p(x_n, y_n), color=RED)
            v_line = axes.get_vertical_line(axes.c2p(x_n, y_n), color=YELLOW, line_func=DashedLine)

            self.play(Create(v_line))
            self.play(FadeIn(dot_f))

            # Calcular la recta tangente matemática
            slope = df(x_n)

            # Ecuación de la recta: y = m(x - x0) + y0
            def tangent_func(x):
                return slope * (x - x_n) + y_n

            # Dibujar la recta tangente
            tangent_line = axes.plot(tangent_func, color=GREEN, x_range=[x_n - 1, x_n + 1.5])
            self.play(Create(tangent_line))

            # Calcular el nuevo punto x_{n+1} donde la tangente cruza el eje X
            x_next = x_n - y_n / slope
            dot_next = Dot(axes.c2p(x_next, 0), color=YELLOW)

            # ¡LA MAGIA DEL ZOOM!
            # Agrupamos el FadeIn del punto con el movimiento de la cámara
            self.play(
                FadeIn(dot_next),
                self.camera.frame.animate.scale(0.35).move_to(axes.c2p(x_next, 0)),
                run_time=1.5  # Hacemos que la animación dure 1.5 segundos para que sea suave
            )
            self.wait(1)

            # Limpiar la pantalla para la siguiente iteración
            if i < 2:
                self.play(
                    FadeOut(dot_x), FadeOut(label_x), FadeOut(v_line),
                    FadeOut(dot_f), FadeOut(tangent_line)
                )

            x_n = x_next

            # Animación extra (opcional): Alejar la cámara al tamaño original al terminar
        self.wait(1)
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)


class RotacionEspacio(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=True,
            show_basis_vectors=True,
            include_background_plane=True,  # Mantiene la cuadrícula original estática de fondo
            **kwargs
        )

    def construct(self):
        # Matriz de rotación 2D para 45 grados
        theta = np.radians(45)
        matriz_rotacion = [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ]

        # Animar la transformación de todo el plano
        self.apply_matrix(matriz_rotacion)
        self.wait()