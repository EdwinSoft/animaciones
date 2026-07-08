from manim import *
import numpy as np

class ResorteRigidezAnimacion(Scene):
    def construct(self):
        # 1. TÍTULO
        title = Text("Polígono Cerrado con Curva", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        # 2. DEFINIR PUNTOS CLAVE
        # Puntos de anclaje (vértices)
        top_p = UP * 2
        right_p = RIGHT * 2 + DOWN * 0.5
        bottom_p = DOWN * 2
        left_p = LEFT * 2 + DOWN * 0.5

        # Puntos de control para las curvas de Bézier
        c1_1 = RIGHT * 2.5 + DOWN * 1
        c1_2 = RIGHT * 1 + DOWN * 2
        c2_1 = LEFT * 1 + DOWN * 2
        c2_2 = LEFT * 2.5 + DOWN * 1

        # 3. CREAR LOS SEGMENTOS INDIVIDUALES
        # Una recta de arriba a la derecha
        l1 = Line(top_p, right_p)
        # Una curva de Bézier de la derecha hacia abajo
        c1 = CubicBezier(right_p, c1_1, c1_2, bottom_p)
        # Una curva de Bézier de abajo hacia la izquierda
        c2 = CubicBezier(bottom_p, c2_1, c2_2, left_p)
        # Una recta para cerrar de la izquierda hacia arriba
        l2 = Line(left_p, top_p)

        # 4. ENSAMBLAR LA FORMA FINAL
        shape = VMobject()
        shape.set_style(
            stroke_width=6,
            stroke_color=YELLOW,
            fill_opacity=0.3,
            fill_color=YELLOW_D
        )

        # Concatenamos los puntos de cada segmento en nuestro VMobject principal
        shape.append_points(l1.points)
        shape.append_points(c1.points)
        shape.append_points(c2.points)
        shape.append_points(l2.points)

        # 5. ANIMACIONES
        # Mostrar los puntos de anclaje
        dots = VGroup(*[Dot(p, color=RED, radius=0.08) for p in [top_p, right_p, bottom_p, left_p]])
        label_points = Text("Anclajes (Vértices)", font_size=20, color=RED).next_to(dots[2], DOWN)

        self.play(FadeIn(dots, shift=UP), Write(label_points), run_time=1.5)

        # Trazar el contorno ensamblado
        self.play(Create(shape), run_time=3)
        self.wait(1)

        # Rellenar la forma
        self.play(shape.animate.set_fill(YELLOW_E, opacity=0.8), FadeOut(label_points), run_time=1.5)

        # Resaltar la parte curva (Opcional, para visualizar dónde está la curva de Bézier)
        curve_label = Text("Curvas Bézier Cúbicas", font_size=24, color=ORANGE).next_to(bottom_p, DOWN)
        self.play(Write(curve_label))

        # Trazamos una línea naranja sobre las partes curvas para resaltarlas
        resalte_curvas = VMobject(color=ORANGE, stroke_width=6)
        resalte_curvas.append_points(c1.points)
        resalte_curvas.append_points(c2.points)
        self.play(Create(resalte_curvas))

        self.wait(3)