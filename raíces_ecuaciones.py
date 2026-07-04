from manim import *
import numpy as np
from mnspy import Biseccion, FalsaPosicion


class BiseccionAnimacion(MovingCameraScene):
    def construct(self):
        # Definir la función para Bisección: f(x) = sin(cos(e^x))
        def f(x):
            return np.sin(np.cos(np.exp(x)))

        # Se cálcula la tabla de iteración con el paquete mnspy
        bis = Biseccion(f, -0.8, 1.5, 0.1, tipo_error='%')
        # Configurar los ejes cartesianos
        axes = Axes(
            x_range=[-1.0, 2.0, 1],
            y_range=[-1.0, 1.2, 1],
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True}
        )
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(f, color=BLUE_D, x_range=[-1, 1.5])
        graph_label = axes.get_graph_label(graph, label=r"\sin(\cos(e^x))", x_val=-1.0, buff=0.2, direction=UR)

        self.play(Create(axes), Write(labels), run_time=3)
        self.play(Create(graph), Write(graph_label), run_time=3)
        self.wait(1)

        a, b, m = bis._tabla['x_min'][0], bis._tabla['x_max'][0], bis._tabla['x'][0]
        pos_a = ValueTracker(a)
        pos_b = ValueTracker(b)
        pos_m = ValueTracker(m)

        self.camera.frame.save_state()
        # Guardamos la altura original de la cámara (por defecto suele ser 8.0)
        altura_original = self.camera.frame.height
        dot_a = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_a.get_value(), 0),  # Tu coordenada fija o variable
                                  radius=0.08 * (self.camera.frame.height / altura_original),
                                  # Modifica el radio real en cada frame
                                  color=YELLOW
                              )
                              )
        dot_b = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_b.get_value(), 0),  # Tu coordenada fija o variable
                                  radius=0.08 * (self.camera.frame.height / altura_original),
                                  # Modifica el radio real en cada frame
                                  color=YELLOW
                              )
                              )
        dot_m = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_m.get_value(), 0),  # Tu coordenada fija o variable
                                  radius=0.08 * (self.camera.frame.height / altura_original),
                                  # Modifica el radio real en cada frame
                                  color=RED
                              )
                              )

        axes.add_updater(
            lambda mob: mob.set_stroke(width=2 * (self.camera.frame.height / altura_original))
        )
        graph.add_updater(
            lambda mob: mob.set_stroke(width=2 * (self.camera.frame.height / altura_original))
        )
        # dot_a.add_updater
        self.play(FadeIn(dot_a, dot_b), run_time=1.5)
        self.play(
            FadeIn(dot_m), run_time=1.5
        )
        # etiquetas = [Tex('Iteracion')] + [MathTex(k) for k in
        #                                   ['x_{l}', 'x_{u}', 'x_{r}', r'f\left(x_{r}\right)', r'\varepsilon_{a}']] + [
        #                 Tex('Tolerancia')]
        # labels = [MathTex('Iteracion'),MathTex('Iteracion'),MathTex('Iteracion'),MathTex('Iteracion'),MathTex('Iteracion'),MathTex('Iteracion'),MathTex('Iteracion')]
        # bis._tabla["Ea"][0]=0
        # bis._fmt['E_a']=bis._fmt['tol']
        rows = list()
        for i in range(len(bis._tabla['x'])):
            rows.append((str('{:' + bis._fmt['iter'] + '}').format(i + 1),
                         str('{:' + bis._fmt['x_l'] + '}').format(bis._tabla["x_min"][i]),
                         str('{:' + bis._fmt['x_u'] + '}').format(bis._tabla["x_max"][i]),
                         str('{:' + bis._fmt['x'] + '}').format(bis._tabla["x"][i]),
                         str('{:' + bis._fmt['f'] + '}').format(f(bis._tabla["x"][i])),
                         str(str('{:' + bis._fmt['E_a'] + '}').format(bis._tabla["Ea"][i])).replace("%", r"\%"),
                         str('{:' + bis._fmt['tol'] + '}').format(
                             0.5 * (bis._tabla["x_max"][i] - bis._tabla["x_min"][i]))))
        grafica = VGroup(axes, graph, dot_a, dot_b, dot_m, graph_label, *labels)
        for i in range(len(bis._tabla['x'])):
            # Dibujar el intervalo [a, b]
            a, b, m = bis._tabla['x_min'][i], bis._tabla['x_max'][i], bis._tabla['x'][i]
            # 1. Convertimos los puntos 'a' y 'b' a coordenadas de pantalla
            coord_a = axes.c2p(a, 0)
            coord_b = axes.c2p(b, 0)

            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_b[0] - coord_a[0])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.8
            escala = nuevo_ancho / config.frame_width
            line_a = axes.get_vertical_line(axes.c2p(a, f(a)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            # line_a = line_a.to_dashed(dash_length=0.15, spacing=0.1)
            line_b = axes.get_vertical_line(axes.c2p(b, f(b)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            line_m = axes.get_vertical_line(axes.c2p(m, f(m)), color=RED, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            label_a = MathTex(f"a_{{{i + 1}}}").scale(1 * escala).next_to(dot_a,
                                                                          UP * escala if f(a) < 0 else DOWN * escala,
                                                                          buff=0.05)
            label_b = MathTex(f"b_{{{i + 1}}}").scale(1 * escala).next_to(dot_b,
                                                                          UP * escala if f(b) < 0 else DOWN * escala,
                                                                          buff=0.05)
            label_m = MathTex(f"m_{{{i + 1}}}").scale(1 * escala).next_to(dot_m,
                                                                          UP * escala if f(m) < 0 else DOWN * escala,
                                                                          buff=0.05)

            self.play(
                self.camera.frame.animate.set_width(nuevo_ancho).move_to(axes.c2p(pos_m.get_value(), 0)),
                run_time=1.5
            )
            self.wait(1)
            #####################
            self.play(FadeOut(grafica), run_time=2)
            etiquetas = [Tex('Iteración')] + [MathTex(k) for k in
                                              ['a', 'b', 'm', r'f\left(m\right)',
                                               r'\varepsilon_{a}']] + [
                            Tex('Tolerancia')]
            tabla = Table(
                rows[:i + 1],
                col_labels=etiquetas.copy(),
                include_outer_lines=True,
                v_buff=0.35,
                h_buff=0.6,
                line_config={"stroke_width": 1.0 * escala, "color": GRAY_C},
                element_to_mobject=MathTex,
            ).scale(0.5 * escala).move_to(axes.c2p(m, 0))
            # Creamos un rectángulo de fondo para aislar visualmente el encabezado
            encabezado = tabla.get_rows()[0]
            encabezado.set_color(TEAL_C)

            # Obtenemos dinámicamente la cantidad de columnas directamente de la tabla
            num_columnas = len(tabla.get_columns())

            for col_idx in range(1, num_columnas + 1):
                tabla.add_highlighted_cell(
                    (1, col_idx),
                    color=TEAL_E,
                    fill_opacity=0.2  # <--- Pasamos la opacidad directamente aquí
                )

            # fondo_encabezado = SurroundingRectangle(
            #     tabla.get_rows()[0],
            #     color=TEAL_E,
            #     fill_opacity=0.2,
            #     stroke_width=0,
            #     buff=0.15
            # )
            # add_to_back asegura que el fondo quede detrás del texto y las líneas

            # Hacemos que la línea divisoria debajo del encabezado sea más gruesa y del color de acento
            lineas_h = tabla.get_horizontal_lines()
            # if len(lineas_h) > 1:
            #     # El índice 1 corresponde a la línea que separa la cabecera de la fila 1
            #     lineas_h[2].set_stroke(width=3.0, color=TEAL_C)

            # ==========================================
            # 3. ESTILIZACIÓN DE LOS DATOS (Foco Visual)
            # ==========================================
            # Si hay más de una fila de datos, atenuamos las iteraciones pasadas a gris
            if len(tabla.get_rows()) > 2:
                for fila_pasada in tabla.get_rows()[1:-1]:
                    fila_pasada.set_color(GRAY_B)

            tabla.get_rows()[-1].set_color(YELLOW)
            # --- SOLUCIÓN AL ERROR ---
            # 3. Agrupamos las líneas horizontales y verticales de la tabla
            cuadricula = VGroup(
                tabla.get_horizontal_lines(),
                tabla.get_vertical_lines()
            )
            linea_sup = lineas_h[0]
            linea_inf = lineas_h[2]

            fondo_encabezado = Rectangle(
                width=linea_sup.width,  # Toma el ancho exacto de la tabla
                height=abs(linea_sup.get_y() - linea_inf.get_y()),  # Calcula el alto exacto de la celda
                color=TEAL_E,
                fill_opacity=0.2,
                stroke_width=0
            ).move_to((linea_sup.get_center() + linea_inf.get_center()) / 2)  # Lo centra entre las dos líneas
            # self.play(FadeIn(tabla))

            self.play(Create(cuadricula), Create(fondo_encabezado), run_time=1)
            self.play(FadeIn(tabla.get_rows()[:i + 1]))
            # self.play(Write(tabla.get_rows()[i + 1]), run_time=2)
            self.play(
                LaggedStart(
                    *[FadeIn(celda, shift=UP * 0.2) for celda in tabla.get_rows()[i + 1]],
                    lag_ratio=0.2  # 0.2 significa 20% de retraso entre cada celda
                ),
                run_time=1
            )
            # self.play(Write(tabla.get_rows()[i]), run_time=2)
            self.wait(2)
            # self.play(FadeOut(tabla), run_time=2)
            if i == len(bis._tabla['x']) - 1:
                tabla.get_rows()[-1][5].set_color('RED')
                self.wait(2)
            self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
            #####################
            self.play(Create(line_a), Create(line_b), Create(line_m), FadeIn(label_a), FadeIn(label_b), FadeIn(label_m))
            self.wait(1)
            if f(a) * f(m) < 0:
                self.play(pos_b.animate.set_value(m), run_time=2)
                self.play(pos_m.animate.set_value(0.5 * (pos_a.get_value() + pos_b.get_value())), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(line_m), FadeOut(label_a),
                    FadeOut(label_b), FadeOut(label_m)
                )
            else:
                self.play(pos_a.animate.set_value(m), run_time=2)
                self.play(pos_m.animate.set_value(0.5 * (pos_a.get_value() + pos_b.get_value())), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(line_m), FadeOut(label_a),
                    FadeOut(label_b), FadeOut(label_m)
                )
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)

        # bis._fmt['iter'], bis._fmt['x_l'], bis._fmt['x_u'], bis._fmt['x'], bis._fmt['f'],bis._fmt['E_a'], bis._fmt['tol']

        # rows.append(('1', '1', '1', '1', '1', '1', '1'))
        # rows = list(zip(*[[f"{val:.2f}" for val in col] for col in bis._tabla.values()]))

        # Configuración de la tabla estricta y compacta
        # tabla = Table(
        #     rows,
        #     col_labels=labels,
        #     include_outer_lines=True,
        #     v_buff=0.35,
        #     h_buff=0.6,
        #     line_config={"stroke_width": 1.5, "color": GRAY_B},
        #     element_to_mobject=MathTex
        # ).scale(0.5).move_to(ORIGIN)
        #
        #
        # # --- SOLUCIÓN AL ERROR ---
        # # 3. Agrupamos las líneas horizontales y verticales de la tabla
        # cuadricula = VGroup(
        #     tabla.get_horizontal_lines(),
        #     tabla.get_vertical_lines()
        # )

        # 4. Animamos primero la cuadrícula (los bordes)
        # self.play(Create(cuadricula), run_time=1)
        # self.play(Write(tabla.get_rows()[0]), run_time=2)
        # 5. Animamos el contenido fila por fila
        # for row in tabla.get_rows():
        #     self.play(Write(row), run_time=0.4)
        #
        # self.wait()

        # self.play(FadeOut(grafica))
        # for i in range(len(bis._tabla['x'])):
        #     etiquetas = [Tex('Iteracion')] + [MathTex(k) for k in
        #                                       ['x_{l}', 'x_{u}', 'x_{r}', r'f\left(x_{r}\right)',
        #                                        r'\varepsilon_{a}']] + [
        #                     Tex('Tolerancia')]
        #     tabla = Table(
        #         rows[:i+1],
        #         col_labels=etiquetas.copy(),
        #         include_outer_lines=True,
        #         v_buff=0.35,
        #         h_buff=0.6,
        #         line_config={"stroke_width": 1.0, "color": GRAY_C},
        #         element_to_mobject=MathTex,
        #     ).scale(0.5).move_to(ORIGIN)
        #     # Creamos un rectángulo de fondo para aislar visualmente el encabezado
        #     fondo_encabezado = SurroundingRectangle(
        #         tabla.get_rows()[0],
        #         color=TEAL_E,
        #         fill_opacity=0.2,
        #         stroke_width=0,
        #         buff=0.15
        #     )
        #     # add_to_back asegura que el fondo quede detrás del texto y las líneas
        #     tabla.add_to_back(fondo_encabezado)
        #     # Hacemos que la línea divisoria debajo del encabezado sea más gruesa y del color de acento
        #     lineas_h = tabla.get_horizontal_lines()
        #     if len(lineas_h) > 1:
        #         # El índice 1 corresponde a la línea que separa la cabecera de la fila 1
        #         lineas_h[1].set_stroke(width=3.0, color=TEAL_C)
        #
        #     # ==========================================
        #     # 3. ESTILIZACIÓN DE LOS DATOS (Foco Visual)
        #     # ==========================================
        #     # Si hay más de una fila de datos, atenuamos las iteraciones pasadas a gris
        #     if len(tabla.get_rows()) > 2:
        #         for fila_pasada in tabla.get_rows()[1:-1]:
        #             fila_pasada.set_color(GRAY_B)
        #
        #     tabla.get_rows()[-1].set_color(YELLOW)
        #     # --- SOLUCIÓN AL ERROR ---
        #     # 3. Agrupamos las líneas horizontales y verticales de la tabla
        #     cuadricula = VGroup(
        #         tabla.get_horizontal_lines(),
        #         tabla.get_vertical_lines()
        #     )
        #     # self.play(FadeIn(tabla))
        #     self.play(Create(cuadricula), Create(fondo_encabezado), run_time=1)
        #     self.play(FadeIn(tabla.get_rows()[:i+1]))
        #     self.play(Write(tabla.get_rows()[i+1]), run_time=2)
        #     #self.play(Write(tabla.get_rows()[i]), run_time=2)
        #     self.wait(2)
        #     self.play(FadeOut(tabla), run_time=2)
        # self.play(FadeIn(tabla), run_time=2)
        # self.wait(2)
        # tabla.get_rows()[-1][5].set_color('RED')
        # #self.play(FadeOut(tabla.get_rows()[-1][5]), run_time=2)
        # self.wait(2)
        # # tabla = Table(rows, col_labels=labels)
        # # for row in tabla.get_rows():
        # #     self.play(Create(row.scale(0.2)))


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
