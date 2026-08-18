from manim import *
from biblioteca import *


class CentroideAnimacion(Scene):
    def construct(self):
        ejes = NumberPlane(
            x_range=[0, 19, 1],
            y_range=[0, 11, 1],
            x_axis_config={
                "include_numbers": True,
                "include_tip": True,
                "tip_shape": StealthTip,
                "label_direction": DOWN
            },
            y_axis_config={
                "include_numbers": True,
                "include_tip": True,
                "tip_shape": StealthTip,
                "label_direction": LEFT
            },
            background_line_style={
                "stroke_opacity": 0.1
            }
        )
        ejes.scale(0.6)
        labels = ejes.get_axis_labels(x_label="x", y_label="y")

        # 1. Crear ejes
        self.play(Create(ejes), Write(labels))

        unit_x = ejes.c2p(1, 0) - ejes.c2p(0, 0)
        scale_factor = unit_x[0]

        # Definir elementos para DrawBorderThenFill
        placa = Polygon(
            ejes.c2p(0, 0), ejes.c2p(18, 0), ejes.c2p(12, 10), ejes.c2p(0, 10),
            fill_color=BLUE, fill_opacity=0.5, stroke_width=4, stroke_color=BLUE
        )
        hueco_rectangular = Rectangle(
            width=2 * scale_factor, height=4 * scale_factor,
            fill_color=BLACK, fill_opacity=1, stroke_width=4, stroke_color=BLACK
        ).move_to(ejes.c2p(12, 4))
        
        semicirculo = Arc(
            radius=3 * scale_factor, start_angle=0, angle=PI,
            fill_color=BLACK, fill_opacity=1, stroke_width=4, stroke_color=BLACK
        ).move_to(ejes.c2p(6, 0), aligned_edge=DOWN)

        # 2. Puntos polígono
        pts_poligono = VGroup(*[Dot(ejes.c2p(x, y), color=RED, radius=0.04) for x, y in [(0, 0), (18, 0), (12, 10), (0, 10)]])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pts_poligono], lag_ratio=0.2))
        
        # 3. Polígono
        self.play(DrawBorderThenFill(placa))
        
        # 4. Puntos semicírculo
        pts_semi = VGroup(*[Dot(ejes.c2p(x, y), color=RED, radius=0.04) for x, y in [(3, 0), (6, 0), (9, 0)]])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pts_semi], lag_ratio=0.2))
        
        # 5. Semicírculo
        self.play(DrawBorderThenFill(semicirculo))
        
        # 6. Puntos rectángulo
        pts_rect = VGroup(*[Dot(ejes.c2p(x, y), color=RED, radius=0.04) for x, y in [(11, 2), (13, 6)]])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pts_rect], lag_ratio=0.2))
        
        # 7. Rectángulo
        self.play(DrawBorderThenFill(hueco_rectangular))
        self.wait(2)
