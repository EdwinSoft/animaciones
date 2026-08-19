from manim import *
import numpy as np
from mnspy import Biseccion, FalsaPosicion, PuntoFijo, NewtonRaphson, Secante


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
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True, "stroke_width": 2}
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
            coord_a = axes.c2p(a, f(a))
            coord_b = axes.c2p(b, f(b))
            coord_centro = axes.c2p(0.5 * (a + b), 0.5 * (f(a) + f(b)))
            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_b[0] - coord_a[0])
            distancia_y = abs(coord_b[1] - coord_a[1])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.1
            nueva_altura = distancia_y * 1.1
            escala = max(nuevo_ancho / config.frame_width, nueva_altura / config.frame_height)
            line_a = axes.get_vertical_line(axes.c2p(a, f(a)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
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
                self.camera.frame.animate.set_height(escala * config.frame_height).move_to(coord_centro),
                run_time=1.5
            )
            self.wait(1)
            #####################
            self.play(FadeOut(grafica), run_time=2)
            etiquetas = [Tex('Iteración')] + [MathTex(k) for k in
                                              ['a', 'b', 'm', r'f\left(m\right)', r'\varepsilon_{a}']] + [
                            Tex('Tolerancia')]
            tabla = Table(
                rows[:i + 1],
                col_labels=etiquetas.copy(),
                include_outer_lines=True,
                v_buff=0.35,
                h_buff=0.6,
                line_config={"stroke_width": 1.0 * escala, "color": GRAY_C},
                element_to_mobject=MathTex,
            ).scale(0.5 * escala).move_to(coord_centro)
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
            # Hacemos que la línea divisoria debajo del encabezado sea más gruesa y del color de acento
            lineas_h = tabla.get_horizontal_lines()
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
                    lag_ratio=0.5  # 0.2 significa 20% de retraso entre cada celda
                ),
                run_time=1
            )
            self.wait(2)
            if i == len(bis._tabla['x']) - 1:
                tabla.get_rows()[-1][5].set_color('RED')
                self.wait(2)
                self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
                break
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


class FalsaPosicionAnimacion(MovingCameraScene):
    def construct(self):
        # Definir la función para Falsa Posición: f(x) = sin(cos(e^x))
        def f(x):
            return np.sin(np.cos(np.exp(x)))

        # Se cálcula la tabla de iteración con el paquete mnspy
        fp = FalsaPosicion(f, -0.8, 1.5, 0.1, tipo_error='%')
        # Configurar los ejes cartesianos
        axes = Axes(
            x_range=[-1.0, 2.0, 1],
            y_range=[-1.0, 1.2, 1],
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True, "stroke_width": 2}
        )
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(f, color=BLUE_D, x_range=[-1, 1.5])
        graph_label = axes.get_graph_label(graph, label=r"\sin(\cos(e^x))", x_val=-1.0, buff=0.2, direction=UR)

        self.play(Create(axes), Write(labels), run_time=3)
        self.play(Create(graph), Write(graph_label), run_time=3)
        self.wait(1)

        a, b, r = fp._tabla['x_min'][0], fp._tabla['x_max'][0], fp._tabla['x'][0]
        pos_a = ValueTracker(a)
        pos_b = ValueTracker(b)
        pos_r = ValueTracker(r)

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
        dot_r = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_r.get_value(), 0),  # Tu coordenada fija o variable
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
        dot_r.set_opacity(0)
        # self.play(
        #     FadeIn(dot_r), run_time=1.5
        # )
        rows = list()
        for i in range(len(fp._tabla['x'])):
            rows.append((str('{:' + fp._fmt['iter'] + '}').format(i + 1),
                         str('{:' + fp._fmt['x_l'] + '}').format(fp._tabla["x_min"][i]),
                         str('{:' + fp._fmt['x_u'] + '}').format(fp._tabla["x_max"][i]),
                         str('{:' + fp._fmt['x'] + '}').format(fp._tabla["x"][i]),
                         str('{:' + fp._fmt['f'] + '}').format(f(fp._tabla["x"][i])),
                         str(str('{:' + fp._fmt['E_a'] + '}').format(fp._tabla["Ea"][i])).replace("%", r"\%"),
                         str('{:' + fp._fmt['tol'] + '}').format(
                             0.5 * (fp._tabla["x_max"][i] - fp._tabla["x_min"][i]))))
        grafica = VGroup(axes, graph, dot_a, dot_b, dot_r, graph_label, *labels)
        for i in range(len(fp._tabla['x'])):
            # Dibujar el intervalo [a, b]
            a, b, r = fp._tabla['x_min'][i], fp._tabla['x_max'][i], fp._tabla['x'][i]
            # 1. Convertimos los puntos 'a' y 'b' a coordenadas de pantalla
            coord_a = axes.c2p(a, f(a))
            coord_b = axes.c2p(b, f(b))
            coord_centro = axes.c2p(0.5 * (a + b), 0.5 * (f(a) + f(b)))
            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_b[0] - coord_a[0])
            distancia_y = abs(coord_b[1] - coord_a[1])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.1
            nueva_altura = distancia_y * 1.1
            escala = max(nuevo_ancho / config.frame_width, nueva_altura / config.frame_height)
            line_a = axes.get_vertical_line(axes.c2p(a, f(a)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            line_b = axes.get_vertical_line(axes.c2p(b, f(b)), color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            line_r = axes.get_vertical_line(axes.c2p(r, f(r)), color=RED, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            line_fp = DashedLine(
                start=axes.c2p(a, f(a)),
                end=axes.c2p(b, f(b)),
                dash_length=0.05 * escala,  # Longitud de cada rayita
                # dashed_ratio=0.5,  # Proporción entre la rayita y el espacio vacío
                color=YELLOW  # Color de la línea
                , stroke_width=2 * escala
            )
            label_a = MathTex(f"a_{{{i + 1}}}").scale(1 * escala).next_to(dot_a,
                                                                          UP * escala if f(a) < 0 else DOWN * escala,
                                                                          buff=0.05)
            label_b = MathTex(f"b_{{{i + 1}}}").scale(1 * escala).next_to(dot_b,
                                                                          UP * escala if f(b) < 0 else DOWN * escala,
                                                                          buff=0.05)
            # label_r = MathTex(f"m_{{{i + 1}}}").scale(1 * escala).next_to(dot_r,
            #                                                               UP * escala if f(r) < 0 else DOWN * escala,
            #                                                               buff=0.05)
            self.play(
                self.camera.frame.animate.set_height(escala * config.frame_height).move_to(coord_centro),
                run_time=1.5
            )
            self.wait(1)
            #####################
            self.play(FadeOut(grafica), run_time=2)
            etiquetas = [Tex('Iteración')] + [MathTex(k) for k in
                                              ['a', 'b', 'r', r'f\left(r\right)', r'\varepsilon_{a}']] + [
                            Tex('Tolerancia')]
            tabla = Table(
                rows[:i + 1],
                col_labels=etiquetas.copy(),
                include_outer_lines=True,
                v_buff=0.35,
                h_buff=0.6,
                line_config={"stroke_width": 1.0 * escala, "color": GRAY_C},
                element_to_mobject=MathTex,
            ).scale(0.5 * escala).move_to(coord_centro)
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
            # Hacemos que la línea divisoria debajo del encabezado sea más gruesa y del color de acento
            lineas_h = tabla.get_horizontal_lines()
            # ==========================================
            # 3. ESTILIZACIÓN DE LOS DATOS (Foco Visual)
            # ==========================================
            # Si hay más de una fila de datos, atenuamos las iteraciones pasadas a gris
            if len(tabla.get_rows()) > 2:
                for fila_pasada in tabla.get_rows()[1:-1]:
                    fila_pasada.set_color(GRAY_B)

            tabla.get_rows()[-1].set_color(YELLOW)
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
                    lag_ratio=0.5  # 0.2 significa 20% de retraso entre cada celda
                ),
                run_time=1
            )
            self.wait(2)
            if i == len(fp._tabla['x']) - 1:
                tabla.get_rows()[-1][5].set_color('RED')
                self.wait(2)
                self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
                break
            self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
            #####################
            self.play(Create(line_a), Create(line_b), Create(line_fp), FadeIn(label_a), FadeIn(label_b))
            self.wait(1)
            dot_r.set_opacity(1)
            self.play(pos_r.animate.set_value(fp._tabla['x'][i]), run_time=2)
            self.wait(1)
            label_r = MathTex(f"r_{{{i + 1}}}").scale(1 * escala).next_to(dot_r,
                                                                          UP * escala if f(r) < 0 else DOWN * escala,
                                                                          buff=0.05)
            self.play(Create(line_r), FadeIn(label_r), run_time=2)
            self.wait(1)
            if f(a) * f(r) < 0:
                self.play(pos_b.animate.set_value(r), run_time=2)
                # self.play(pos_r.animate.set_value(fp._tabla['x'][i+1]), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(line_r), FadeOut(line_fp), FadeOut(label_a),
                    FadeOut(label_b), FadeOut(label_r)
                )
            else:
                self.play(pos_a.animate.set_value(r), run_time=2)
                # self.play(pos_r.animate.set_value(fp._tabla['x'][i+1]), run_time=2)
                self.play(
                    FadeOut(line_a), FadeOut(line_b), FadeOut(line_r), FadeOut(line_fp), FadeOut(label_a),
                    FadeOut(label_b), FadeOut(label_r)
                )
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)


class PuntoFijoAnimacion(MovingCameraScene):
    def construct(self):
        # Definir la función para Falsa Posición: f(x) = sin(cos(e^x))
        def f(x):
            return np.sin(np.cos(np.exp(x))) + x

        # Se cálcula la tabla de iteración con el paquete mnspy
        pf = PuntoFijo(f, 0.5, 0.1, tipo_error='%')
        # Configurar los ejes cartesianos
        axes = Axes(
            x_range=[-1.0, 2.0, 1],
            y_range=[-1.0, 1.2, 1],
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True, "stroke_width": 2}
        )
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(f, color=BLUE_D, x_range=[-1, 1.5])
        graph_2 = axes.plot(lambda x: x, color=WHITE, x_range=[-1, 1.5])
        label_g_1 = axes.get_graph_label(graph, label=r"g\left(x\right)=\sin(\cos(e^x))+x",
                                           x_val=-1.5, buff=3.2,
                                           direction=UL).scale(0.7)
        label_g_2 = axes.get_graph_label(graph_2, label=r"y\left(x\right)=x",
                                           x_val=1.5,
                                           direction=UL).scale(0.7)
        graph_label=VGroup(label_g_1, label_g_2)

        self.play(Create(axes), Write(labels), run_time=3)
        self.play(Create(graph), Create(graph_2), Write(graph_label), run_time=3)
        self.wait(1)

        r = pf._tabla['x'][0]
        # m=(a+b)/2
        # pos_a = ValueTracker(a)
        # pos_b = ValueTracker(b)
        a = pf._x_0
        pos_r = ValueTracker(a)

        self.camera.frame.save_state()
        # Guardamos la altura original de la cámara (por defecto suele ser 8.0)
        altura_original = self.camera.frame.height
        # dot_a = always_redraw(lambda:
        #                       Dot(
        #                           point=axes.c2p(pos_a.get_value(), 0),  # Tu coordenada fija o variable
        #                           radius=0.08 * (self.camera.frame.height / altura_original),
        #                           # Modifica el radio real en cada frame
        #                           color=YELLOW
        #                       )
        #                       )
        # dot_b = always_redraw(lambda:
        #                       Dot(
        #                           point=axes.c2p(pos_b.get_value(), 0),  # Tu coordenada fija o variable
        #                           radius=0.08 * (self.camera.frame.height / altura_original),
        #                           # Modifica el radio real en cada frame
        #                           color=YELLOW
        #                       )
        #                       )
        dot_r = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_r.get_value(), pos_r.get_value()),  # Tu coordenada fija o variable
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
        graph_2.add_updater(
            lambda mob: mob.set_stroke(width=2 * (self.camera.frame.height / altura_original))
        )
        # dot_a.add_updater
        # self.play(FadeIn(dot_a, dot_b), run_time=1.5)
        self.play(
            FadeIn(dot_r), run_time=1.5
        )
        rows = list()
        for i in range(len(pf._tabla['x'])):
            rows.append((str('{:' + pf._fmt['iter'] + '}').format(i + 1),
                         str('{:' + pf._fmt['x'] + '}').format(pf._tabla["x"][i]),
                         str('{:' + pf._fmt['f'] + '}').format(f(pf._tabla["x"][i])),
                         str(str('{:' + pf._fmt['E_a'] + '}').format(pf._tabla["Ea"][i])).replace("%", r"\%")))
        grafica = VGroup(axes, graph, graph_2, dot_r, graph_label, *labels)
        for i in range(len(pf._tabla['x'])):
            r = pf._tabla['x'][i]
            # 1. Convertimos los puntos 'a' y 'b' a coordenadas de pantalla
            coord_a = axes.c2p(a, f(a))
            coord_r = axes.c2p(r, f(r))
            coord_centro = axes.c2p(0.5 * (a + r), 0.5 * 0.5 * (a + r))
            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_r[0] - coord_a[0])
            distancia_y = abs(f(r))
            distancia_y = max(abs(f(r)), abs(f(a)))
            # distancia_y = abs(coord_r[1] - coord_a[1])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.1
            nueva_altura = distancia_y * 4
            # escala = max(nuevo_ancho / config.frame_width, nueva_altura / config.frame_height)
            escala = nueva_altura / config.frame_height
            line_a = axes.get_vertical_line(coord_a, color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            # line_b = axes.get_vertical_line(axes.c2p(b, f(b)), color=YELLOW, stroke_width=2 * escala,
            #                                 line_config={"dash_length": 0.05 * escala})
            # line_r = axes.get_vertical_line(axes.c2p(r, f(r)), color=RED, stroke_width=2 * escala,
            #                                 line_config={"dash_length": 0.05 * escala})
            line_pf = DashedLine(
                start=axes.c2p(a, f(a)),
                end=axes.c2p(r, r),
                dash_length=0.05 * escala,  # Longitud de cada rayita
                # dashed_ratio=0.5,  # Proporción entre la rayita y el espacio vacío
                color=YELLOW  # Color de la línea
                , stroke_width=2 * escala
            )
            # label_a = MathTex(f"a_{{{i + 1}}}").scale(1 * escala).next_to(dot_a,
            #                                                               UP * escala if f(a) < 0 else DOWN * escala,
            #                                                               buff=0.05)
            # label_b = MathTex(f"b_{{{i + 1}}}").scale(1 * escala).next_to(dot_b,
            #                                                               UP * escala if f(b) < 0 else DOWN * escala,
            #                                                               buff=0.05)

            self.play(
                self.camera.frame.animate.set_height(escala * config.frame_height).move_to(coord_centro),
                run_time=1.5
            )
            self.wait(1)
            self.play(Create(line_a), run_time=1)
            self.play(Create(line_pf), run_time=1)
            self.play(pos_r.animate.set_value(pf._tabla['x'][i]), run_time=2)
            label_r = MathTex(f"r_{{{i + 1}}}").scale(0.7 * escala).next_to(dot_r,
                                                                            UP * escala if f(r) > 0 else DOWN * escala,
                                                                            buff=0.05)
            self.play(FadeIn(label_r))
            self.wait(2)
            a = r
            #####################
            self.play(FadeOut(grafica, line_a, line_pf, label_r), run_time=2)
            etiquetas = [Tex('Iteración')] + [MathTex(k) for k in ['r', r'f\left(r\right)', r'\varepsilon_{a}']]
            tabla = Table(
                rows[:i + 1],
                col_labels=etiquetas.copy(),
                include_outer_lines=True,
                v_buff=0.35,
                h_buff=0.6,
                line_config={"stroke_width": 1.0 * escala, "color": GRAY_C},
                element_to_mobject=MathTex,
            ).scale(0.5 * escala).move_to(coord_centro)
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
            # Hacemos que la línea divisoria debajo del encabezado sea más gruesa y del color de acento
            lineas_h = tabla.get_horizontal_lines()
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
                    lag_ratio=0.5  # 0.2 significa 20% de retraso entre cada celda
                ),
                run_time=1
            )
            self.wait(2)
            if i == len(pf._tabla['x']) - 1:
                tabla.get_rows()[-1][3].set_color('RED')
                self.wait(2)
                self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
                break
            self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
            #####################

            # self.play(
            #     FadeOut(line_a), FadeOut(line_pf), FadeOut(label_r)
            # )
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)


class NewtonRaphsonAnimacion(MovingCameraScene):
    def construct(self):
        # Definir la función para Falsa Posición: f(x) = sin(cos(e^x))
        def f(x):
            return np.sin(np.cos(np.exp(x)))

        def df(x):
            return -np.exp(x) * np.sin(np.exp(x)) * np.cos(np.cos(np.exp(x)))

        # Se cálcula la tabla de iteración con el paquete mnspy
        nr = NewtonRaphson(f, df, 0.0, 0.1, tipo_error='%')
        # Configurar los ejes cartesianos
        axes = Axes(
            x_range=[-1.0, 2.0, 1],
            y_range=[-1.0, 1.2, 1],
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True, "stroke_width": 2}
        )
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(f, color=BLUE_D, x_range=[-1, 1.5])
        graph_label = axes.get_graph_label(graph, label=r"f\left(x\right)=\sin(\cos(e^x))",
                                           x_val=-1.5, buff=0.2,
                                           direction=UL).scale(0.7)

        self.play(Create(axes), Write(labels), run_time=3)
        self.play(Create(graph), Write(graph_label), run_time=3)
        self.wait(1)

        r = nr._tabla['x'][0]
        # m=(a+b)/2
        # pos_a = ValueTracker(a)
        # pos_b = ValueTracker(b)
        a = nr._x_0
        pos_r = ValueTracker(a)

        self.camera.frame.save_state()
        # Guardamos la altura original de la cámara (por defecto suele ser 8.0)
        altura_original = self.camera.frame.height
        # dot_a = always_redraw(lambda:
        #                       Dot(
        #                           point=axes.c2p(pos_a.get_value(), 0),  # Tu coordenada fija o variable
        #                           radius=0.08 * (self.camera.frame.height / altura_original),
        #                           # Modifica el radio real en cada frame
        #                           color=YELLOW
        #                       )
        #                       )
        # dot_b = always_redraw(lambda:
        #                       Dot(
        #                           point=axes.c2p(pos_b.get_value(), 0),  # Tu coordenada fija o variable
        #                           radius=0.08 * (self.camera.frame.height / altura_original),
        #                           # Modifica el radio real en cada frame
        #                           color=YELLOW
        #                       )
        #                       )
        dot_r = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_r.get_value(), 0),  # Tu coordenada fija o variable
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
        # self.play(FadeIn(dot_a, dot_b), run_time=1.5)
        self.play(
            FadeIn(dot_r), run_time=1.5
        )
        rows = list()
        for i in range(len(nr._tabla['x'])):
            rows.append((str('{:' + nr._fmt['iter'] + '}').format(i + 1),
                         str('{:' + nr._fmt['x'] + '}').format(nr._tabla["x"][i]),
                         str('{:' + nr._fmt['f'] + '}').format(f(nr._tabla["x"][i])),
                         str(str('{:' + nr._fmt['E_a'] + '}').format(nr._tabla["Ea"][i])).replace("%", r"\%")))
        grafica = VGroup(axes, graph, dot_r, graph_label, *labels)
        for i in range(len(nr._tabla['x'])):
            r = nr._tabla['x'][i]

            coord_a = axes.c2p(a, f(a))
            coord_r = axes.c2p(r, f(r))
            coord_centro = axes.c2p(0.5 * (a + r), 0.5 * (max(f(a), f(r), 0.0) + min(f(a), f(r), 0.0)))
            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_r[0] - coord_a[0])
            # distancia_y = abs(coord_a[1] )
            distancia_y = max(coord_r[1], coord_a[1], 0.0) - min(coord_r[1], coord_a[1], 0.0)
            # distancia_y = abs(coord_r[1] - coord_a[1])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.1
            nueva_altura = distancia_y * 1.1
            escala = max(nuevo_ancho / config.frame_width, nueva_altura / config.frame_height)
            # escala = nueva_altura / config.frame_height
            line_a = axes.get_vertical_line(coord_a, color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            # line_b = axes.get_vertical_line(axes.c2p(b, f(b)), color=YELLOW, stroke_width=2 * escala,
            #                                 line_config={"dash_length": 0.05 * escala})
            # line_r = axes.get_vertical_line(axes.c2p(r, f(r)), color=RED, stroke_width=2 * escala,
            #                                 line_config={"dash_length": 0.05 * escala})
            line_nr = Line(
                start=axes.c2p(a, f(a)),
                end=axes.c2p(r, 0),
                # dash_length=0.05 * escala,  # Longitud de cada rayita
                # dashed_ratio=0.5,  # Proporción entre la rayita y el espacio vacío
                color=RED  # Color de la línea
                , stroke_width=2 * escala
            )
            line_nr.scale(4, about_point=line_nr.get_center())
            # label_a = MathTex(f"a_{{{i + 1}}}").scale(1 * escala).next_to(dot_a,
            #                                                               UP * escala if f(a) < 0 else DOWN * escala,
            #                                                               buff=0.05)
            # label_b = MathTex(f"b_{{{i + 1}}}").scale(1 * escala).next_to(dot_b,
            #                                                               UP * escala if f(b) < 0 else DOWN * escala,
            #                                                               buff=0.05)

            self.play(
                self.camera.frame.animate.set_height(escala * config.frame_height).move_to(coord_centro),
                run_time=1.5
            )
            self.wait(1)
            self.play(Create(line_a), run_time=2)
            self.play(Create(line_nr), run_time=2)
            self.play(pos_r.animate.set_value(nr._tabla['x'][i]), run_time=2)
            label_r = MathTex(f"r_{{{i + 1}}}").scale(0.7 * escala).next_to(dot_r,
                                                                            UP * escala if f(r) < 0 else DOWN * escala,
                                                                            buff=0.05)
            self.play(FadeIn(label_r), run_time=2)
            self.wait(2)
            a = r
            #####################
            self.play(FadeOut(grafica, line_a, line_nr, label_r), run_time=2)
            etiquetas = [Tex('Iteración')] + [MathTex(k) for k in ['r', r'f\left(r\right)', r'\varepsilon_{a}']]
            tabla = Table(
                rows[:i + 1],
                col_labels=etiquetas.copy(),
                include_outer_lines=True,
                v_buff=0.35,
                h_buff=0.6,
                line_config={"stroke_width": 1.0 * escala, "color": GRAY_C},
                element_to_mobject=MathTex,
            ).scale(0.5 * escala).move_to(coord_centro)
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
            # Hacemos que la línea divisoria debajo del encabezado sea más gruesa y del color de acento
            lineas_h = tabla.get_horizontal_lines()
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
                    lag_ratio=0.5  # 0.2 significa 20% de retraso entre cada celda
                ),
                run_time=1
            )
            self.wait(2)
            if i == len(nr._tabla['x']) - 1:
                tabla.get_rows()[-1][3].set_color('RED')
                self.wait(2)
                self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
                break
            self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
            #####################

            # self.play(
            #     FadeOut(line_a), FadeOut(line_pf), FadeOut(label_r)
            # )
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)


class SecanteAnimacion(MovingCameraScene):
    def construct(self):
        # Definir la función para Falsa Posición: f(x) = sin(cos(e^x))
        def f(x):
            return np.sin(np.cos(np.exp(x)))

        # Se cálcula la tabla de iteración con el paquete mnspy
        sc = Secante(f, 0.0, 1.0, 0.1, tipo_error='%')
        # Configurar los ejes cartesianos
        axes = Axes(
            x_range=[-1.0, 2.0, 1],
            y_range=[-1.0, 1.2, 1],
            axis_config={"include_tip": True, 'tip_shape': StealthTip, "include_numbers": True, "stroke_width": 2}
        )
        axes.to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(f, color=BLUE_D, x_range=[-1, 1.5])
        graph_label = axes.get_graph_label(graph, label=r"f\left(x\right)=\sin(\cos(e^x))",
                                           x_val=-1.5, buff=0.2,
                                           direction=UL).scale(0.7)

        self.play(Create(axes), Write(labels), run_time=3)
        self.play(Create(graph), Write(graph_label), run_time=3)
        self.wait(1)

        r = sc._tabla['x'][0]
        x_0 = sc._x_0
        x_1 = sc._x_1
        pos_r = ValueTracker(r)
        pos_x_0 = ValueTracker(x_0)
        pos_x_1 = ValueTracker(x_1)

        self.camera.frame.save_state()
        # Guardamos la altura original de la cámara (por defecto suele ser 8.0)
        altura_original = self.camera.frame.height
        dot_a = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_x_0.get_value(), 0),  # Tu coordenada fija o variable
                                  radius=0.08 * (self.camera.frame.height / altura_original),
                                  # Modifica el radio real en cada frame
                                  color=YELLOW
                              )
                              )
        dot_b = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_x_1.get_value(), 0),  # Tu coordenada fija o variable
                                  radius=0.08 * (self.camera.frame.height / altura_original),
                                  # Modifica el radio real en cada frame
                                  color=YELLOW
                              )
                              )
        dot_r = Dot(
            point=axes.c2p(r, 0),  # Tu coordenada fija o variable
            radius=0.08, color=RED
        ).set_opacity(0)
        self.add(dot_r)

        dot_r = always_redraw(lambda:
                              Dot(
                                  point=axes.c2p(pos_r.get_value(), 0),  # Tu coordenada fija o variable
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
        self.play(FadeIn(dot_a, dot_b), run_time=1.5)
        # dot_a.add_updater
        # self.play(FadeIn(dot_a, dot_b), run_time=1.5)
        # self.play(
        #     FadeIn(dot_r), run_time=1.5
        # )

        rows = list()
        for i in range(len(sc._tabla['x'])):
            rows.append((str('{:' + sc._fmt['iter'] + '}').format(i + 1),
                         str('{:' + sc._fmt['x'] + '}').format(sc._tabla["x"][i]),
                         str('{:' + sc._fmt['f'] + '}').format(f(sc._tabla["x"][i])),
                         str(str('{:' + sc._fmt['E_a'] + '}').format(sc._tabla["Ea"][i])).replace("%", r"\%")))
        grafica = VGroup(axes, graph, dot_r, dot_a, dot_b, graph_label, *labels)
        for i in range(len(sc._tabla['x'])):
            r = sc._tabla['x'][i]

            coord_x_0 = axes.c2p(x_0, f(x_0))
            coord_x_1 = axes.c2p(x_1, f(x_1))
            coord_centro = axes.c2p(0.5 * (x_0 + x_1), 0.5 * (max(f(x_0), f(x_1), 0.0) + min(f(x_0), f(x_1), 0.0)))
            # 2. Calculamos la distancia física en el eje X (índice 0)
            distancia_x = abs(coord_x_1[0] - coord_x_0[0])
            # distancia_y = abs(coord_a[1] )
            distancia_y = max(coord_x_1[1], coord_x_0[1], 0.0) - min(coord_x_1[1], coord_x_0[1], 0.0)
            # distancia_y = abs(coord_r[1] - coord_a[1])

            # 3. Le añadimos un margen (e.g., multiplicarlo por 1.5 añade un 50% de espacio extra)
            nuevo_ancho = distancia_x * 1.1
            nueva_altura = distancia_y * 1.1
            escala = max(nuevo_ancho / config.frame_width, nueva_altura / config.frame_height)
            # escala = nueva_altura / config.frame_height
            line_a = axes.get_vertical_line(coord_x_0, color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            line_b = axes.get_vertical_line(coord_x_1, color=YELLOW, stroke_width=2 * escala,
                                            line_config={"dash_length": 0.05 * escala})
            # line_r = axes.get_vertical_line(axes.c2p(r, f(r)), color=RED, stroke_width=2 * escala,
            #                                 line_config={"dash_length": 0.05 * escala})
            line_sc = Line(
                start=coord_x_0,
                end=coord_x_1,
                color=RED  # Color de la línea
                , stroke_width=2 * escala
            )
            line_sc.scale(4, about_point=line_sc.get_center())
            self.play(pos_x_0.animate.set_value(x_0), run_time=2)
            self.play(pos_x_1.animate.set_value(x_1), run_time=2)
            self.play(
                self.camera.frame.animate.set_height(escala * config.frame_height).move_to(coord_centro),
                run_time=1.5
            )
            self.wait(1)
            self.play(Create(line_a), Create(line_b), run_time=2)
            self.play(Create(line_sc), run_time=2)
            if i == 0:
                dot_r.scale(escala)
                self.play(dot_r.animate.set_opacity(1), run_time=1)

            self.play(pos_r.animate.set_value(sc._tabla['x'][i]), run_time=2)
            dot_r.set_z_index(1)
            label_r = MathTex(f"r_{{{i + 1}}}").scale(0.7 * escala).next_to(dot_r,
                                                                            UP * escala if f(r) < 0 else DOWN * escala,
                                                                            buff=0.05)
            self.play(FadeIn(label_r), run_time=2)
            self.wait(2)
            x_0 = x_1
            x_1 = r
            #####################
            self.play(FadeOut(grafica, line_a, line_b, line_sc, label_r), run_time=2)
            etiquetas = [Tex('Iteración')] + [MathTex(k) for k in ['r', r'f\left(r\right)', r'\varepsilon_{a}']]
            tabla = Table(
                rows[:i + 1],
                col_labels=etiquetas.copy(),
                include_outer_lines=True,
                v_buff=0.35,
                h_buff=0.6,
                line_config={"stroke_width": 1.0 * escala, "color": GRAY_C},
                element_to_mobject=MathTex,
            ).scale(0.5 * escala).move_to(coord_centro)
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
            # Hacemos que la línea divisoria debajo del encabezado sea más gruesa y del color de acento
            lineas_h = tabla.get_horizontal_lines()
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
                color=YELLOW,
                fill_opacity=0.2,
                stroke_width=2
            ).move_to((linea_sup.get_center() + linea_inf.get_center()) / 2)  # Lo centra entre las dos líneas
            # self.play(FadeIn(tabla))

            self.play(Create(cuadricula), Create(fondo_encabezado), run_time=1)
            self.play(FadeIn(tabla.get_rows()[:i + 1]))
            # self.play(Write(tabla.get_rows()[i + 1]), run_time=2)
            self.play(
                LaggedStart(
                    *[FadeIn(celda, shift=UP * 0.2) for celda in tabla.get_rows()[i + 1]],
                    lag_ratio=0.5  # 0.2 significa 20% de retraso entre cada celda
                ),
                run_time=1
            )
            self.wait(2)
            if i == len(sc._tabla['x']) - 1:
                tabla.get_rows()[-1][3].set_color('RED')
                self.wait(2)
                self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
                break
            self.play(FadeOut(tabla, fondo_encabezado), FadeIn(grafica), run_time=2)
            #####################

            # self.play(
            #     FadeOut(line_a), FadeOut(line_pf), FadeOut(label_r)
            # )
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)
