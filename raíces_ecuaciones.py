from manim import *
import numpy as np
from mnspy import Biseccion, FalsaPosicion


class BiseccionAnimacion(MovingCameraScene):
    def construct(self):
        # Definir la función para Bisección: f(x) = sin(cos(e^x))
        def f(x):
            return np.sin(np.cos(np.exp(x)))

        bis = Biseccion(f, -1, 1.5, 0.1, tipo_error='%')
        # Configurar los ejes cartesianos
        axes = Axes(
            x_range=[-1.0, 2, 1],
            y_range=[-1.0, 1.0, 1],
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True}
        )
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.plot(f, color=BLUE, x_range=[-1, 1.5])
        graph_label = axes.get_graph_label(graph, label=r"\sin(\cos(e^x))", x_val=0.5, buff=2, direction=UR).scale(0.6)

        self.play(Create(axes), Write(labels), run_time=3)
        self.play(Create(graph), Write(graph_label))
        self.wait(1)
        self.camera.frame.save_state()
        # Guardamos la altura original de la cámara (por defecto suele ser 8.0)
        altura_original = self.camera.frame.height

        # 3. Agregar los UPDATERS dinámicos
        # Reducen el stroke_width conforme la cámara disminuye su tamaño
        axes.add_updater(
            lambda mob: mob.set_stroke(width=4 * (self.camera.frame.height / altura_original))
            # .x_axis.set(tick_size=0.1 * (self.camera.frame.height / altura_original))
            # .y_axis.set(tick_size=0.1 * (self.camera.frame.height / altura_original))
        )

        graph.add_updater(
            lambda mob: mob.set_stroke(width=4 * (self.camera.frame.height / altura_original))
        )
        # Parámetros iniciales de Bisección
        # a, b = bis._rango
        # a, b = 0.5, 3.5
        escala = 1.0
        for i in range(10):
            # Dibujar el intervalo [a, b]
            a, b = bis._tabla['x_min'][i], bis._tabla['x_max'][i]
            line_a = axes.get_vertical_line(axes.c2p(a, f(a)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            # line_a = line_a.to_dashed(dash_length=0.15, spacing=0.1)
            line_b = axes.get_vertical_line(axes.c2p(b, f(b)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            dot_a = Dot(axes.c2p(a, 0), color=YELLOW).scale(escala)
            dot_b = Dot(axes.c2p(b, 0), color=YELLOW).scale(escala)
            label_a = MathTex(f"a_{i}").scale(0.6 * escala).next_to(dot_a, DOWN * escala, buff=0.05)
            label_b = MathTex(f"b_{i}").scale(0.6 * escala).next_to(dot_b, UP * escala, buff=0.05)

            self.play(Create(line_a), Create(line_b), FadeIn(dot_a, dot_b), FadeIn(label_a), FadeIn(label_b))

            # Calcular punto medio
            # m = (a + b) / 2
            m = bis._tabla['x'][i]
            dot_m = Dot(axes.c2p(m, 0), color=RED).scale(escala)
            label_m = MathTex(f"m_{i}").scale(0.6 * escala).next_to(dot_m, UP * escala, buff=0.05)
            self.play(
                FadeIn(dot_m), FadeIn(label_m), run_time=1.5
            )
            self.wait(1)
            # 1. Convertimos los puntos 'a' y 'b' a coordenadas de pantalla
            coord_a = axes.c2p(a, 0)
            coord_b = axes.c2p(b, 0)

            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_b[0] - coord_a[0])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.5

            # Opcional (¡Muy recomendado!):
            # Evitar que la cámara haga un zoom infinito si 'a' y 'b' están casi pegados.
            # Esto establece que el ancho nunca sea menor a 1 unidad.
            # nuevo_ancho = max(nuevo_ancho, 1.0)

            # 4. Aplicamos el ancho exacto con set_width
            self.play(
                self.camera.frame.animate.set_width(nuevo_ancho).move_to(axes.c2p(m, 0)),
                run_time=1.5
            )
            # self.play(
            #     FadeIn(dot_m), FadeIn(label_m),
            #     #Write(label_m),
            #     self.camera.frame.animate.scale(0.65).move_to(axes.c2p(m, 0)),
            #     run_time=1.5
            # )
            self.wait(1)

            # Lógica de bisección para la siguiente iteración
            # if f(a) * f(m) < 0:
            #     b = m
            # else:
            #     a = m
            if f(a) * f(m) < 0:
                self.play(dot_b.animate.move_to(axes.c2p(m, 0)), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(dot_m), FadeOut(label_a), FadeOut(dot_a), FadeOut(dot_b),
                    FadeOut(label_b), FadeOut(label_m)
                )

            else:
                self.play(dot_a.animate.move_to(axes.c2p(m, 0)), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(dot_m), FadeOut(label_a), FadeOut(dot_a), FadeOut(dot_b),
                    FadeOut(label_b), FadeOut(label_m)
                )

            # Limpiar para la siguiente iteración
            # self.play(
            #     FadeOut(line_a), FadeOut(line_b), FadeOut(dot_a),
            #     FadeOut(dot_b), FadeOut(dot_m), FadeOut(label_a),
            #     FadeOut(label_b), FadeOut(label_m), run_time=2.5
            # )

            # escala*=0.65
            escala = nuevo_ancho / config.frame_width

        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)


class FalsaPosicionAnimacion(MovingCameraScene):
    def construct(self):
        # Definir la función para Bisección: f(x) = sin(cos(e^x))
        def f(x):
            return np.sin(np.cos(np.exp(x)))

        fp = FalsaPosicion(f, -1, 1.5, 0.1, tipo_error='%')
        # Configurar los ejes cartesianos
        axes = Axes(
            x_range=[-1.0, 2, 1],
            y_range=[-1.0, 1.0, 1],
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True}
        )
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.plot(f, color=BLUE, x_range=[-1, 1.5])
        graph_label = axes.get_graph_label(graph, label=r"\sin(\cos(e^x))", x_val=0.5, buff=2, direction=UR).scale(0.6)

        self.play(Create(axes), Write(labels), run_time=3)
        self.play(Create(graph), Write(graph_label))
        self.wait(1)
        self.camera.frame.save_state()
        # Guardamos la altura original de la cámara (por defecto suele ser 8.0)
        altura_original = self.camera.frame.height

        # 3. Agregar los UPDATERS dinámicos
        # Reducen el stroke_width conforme la cámara disminuye su tamaño
        axes.add_updater(
            lambda mob: mob.set_stroke(width=4 * (self.camera.frame.height / altura_original))
            # .x_axis.set(tick_size=0.1 * (self.camera.frame.height / altura_original))
            # .y_axis.set(tick_size=0.1 * (self.camera.frame.height / altura_original))
        )

        graph.add_updater(
            lambda mob: mob.set_stroke(width=4 * (self.camera.frame.height / altura_original))
        )
        # Parámetros iniciales de Bisección
        # a, b = bis._rango
        # a, b = 0.5, 3.5
        escala = 1.0
        for i in range(len(fp._tabla['x'])):
            # Dibujar el intervalo [a, b]
            a, b = fp._tabla['x_min'][i], fp._tabla['x_max'][i]
            line_a = axes.get_vertical_line(axes.c2p(a, f(a)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            # line_a = line_a.to_dashed(dash_length=0.15, spacing=0.1)
            line_b = axes.get_vertical_line(axes.c2p(b, f(b)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            linea_punteada = DashedLine(
                start=axes.c2p(a, f(a)),
                end=axes.c2p(b, f(b)),
                dash_length=0.05 * escala,  # Longitud de cada rayita
                # dashed_ratio=0.5,  # Proporción entre la rayita y el espacio vacío
                color=YELLOW  # Color de la línea
                , stroke_width=2 * escala
            )
            dot_a = Dot(axes.c2p(a, 0), color=YELLOW).scale(escala)
            dot_b = Dot(axes.c2p(b, 0), color=YELLOW).scale(escala)
            label_a = MathTex(f"a_{i}").scale(0.6 * escala).next_to(dot_a, DOWN * escala, buff=0.05)
            label_b = MathTex(f"b_{i}").scale(0.6 * escala).next_to(dot_b, UP * escala, buff=0.05)

            self.play(Create(line_a), Create(line_b), Create(linea_punteada), FadeIn(dot_a, dot_b), FadeIn(label_a),
                      FadeIn(label_b))

            # Calcular punto medio
            # m = (a + b) / 2
            m = fp._tabla['x'][i]
            dot_m = Dot(axes.c2p(m, 0), color=RED).scale(escala)
            label_m = MathTex(f"m_{i}").scale(0.6 * escala).next_to(dot_m, UP * escala, buff=0.05)
            self.play(
                FadeIn(dot_m), FadeIn(label_m), run_time=1.5
            )
            self.wait(1)
            # 1. Convertimos los puntos 'a' y 'b' a coordenadas de pantalla
            coord_a = axes.c2p(a, 0)
            coord_b = axes.c2p(b, 0)

            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_b[0] - coord_a[0])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.5

            # Opcional (¡Muy recomendado!):
            # Evitar que la cámara haga un zoom infinito si 'a' y 'b' están casi pegados.
            # Esto establece que el ancho nunca sea menor a 1 unidad.
            # nuevo_ancho = max(nuevo_ancho, 1.0)

            # 4. Aplicamos el ancho exacto con set_width
            self.play(
                self.camera.frame.animate.set_width(nuevo_ancho).move_to(axes.c2p(0.5 * (a + b), 0)),
                run_time=1.5
            )
            # self.play(
            #     FadeIn(dot_m), FadeIn(label_m),
            #     #Write(label_m),
            #     self.camera.frame.animate.scale(0.65).move_to(axes.c2p(m, 0)),
            #     run_time=1.5
            # )
            self.wait(1)

            # Lógica de bisección para la siguiente iteración
            # if f(a) * f(m) < 0:
            #     b = m
            # else:
            #     a = m
            if f(a) * f(m) < 0:
                self.play(dot_b.animate.move_to(axes.c2p(m, 0)), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(linea_punteada), FadeOut(dot_m), FadeOut(label_a),
                    FadeOut(dot_a), FadeOut(dot_b),
                    FadeOut(label_b), FadeOut(label_m)
                )

            else:
                self.play(dot_a.animate.move_to(axes.c2p(m, 0)), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(linea_punteada), FadeOut(dot_m), FadeOut(label_a),
                    FadeOut(dot_a), FadeOut(dot_b),
                    FadeOut(label_b), FadeOut(label_m)
                )

            # Limpiar para la siguiente iteración
            # self.play(
            #     FadeOut(line_a), FadeOut(line_b), FadeOut(dot_a),
            #     FadeOut(dot_b), FadeOut(dot_m), FadeOut(label_a),
            #     FadeOut(label_b), FadeOut(label_m), run_time=2.5
            # )

            # escala*=0.65
            escala = nuevo_ancho / config.frame_width

        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)
