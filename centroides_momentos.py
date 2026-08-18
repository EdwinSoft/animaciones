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
        self.add(ejes, labels)

        # Dimensiones basadas en la imagen
        # La figura principal es un polígono
        # Puntos aproximados (escalados para ajustar a los ejes):
        # Origen (0,0) está en la esquina inferior izquierda de la figura.
        
        # Coordenadas:
        # A: (0, 0) - esquina inferior izquierda
        # B: (17, 0) - esquina inferior derecha (3+6+2+2+5 = 18? No, 3+6+2+2+5 = 18 total. 3+6+8?
        # Revisando: 3 (izq) + 6 (diámetro) + 2 (espacio) + 2 (ancho rect) + 5 (der) = 18.
        # Altura: 2+4+4 = 10.
        
        # Obtener factor de escala para convertir unidades del gráfico a unidades de Manim
        # ejes.c2p(1, 0) - ejes.c2p(0, 0) da el vector unitario en el eje X
        unit_x = ejes.c2p(1, 0) - ejes.c2p(0, 0)
        scale_factor = unit_x[0] 
        
        # Definición de la placa principal
        placa = Polygon(
            ejes.c2p(0, 0),
            ejes.c2p(18, 0),
            ejes.c2p(12, 10),
            ejes.c2p(0, 10),
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_width=0
        )
        
        # Hueco rectangular: ancho 2, alto 4 (unidades)
        hueco_rectangular = Rectangle(
            width=2 * scale_factor, 
            height=4 * scale_factor, 
            fill_color=BLACK, 
            fill_opacity=1,
            stroke_width=0
        )
        hueco_rectangular.move_to(ejes.c2p(12, 4))
        
        # Semicírculo: radio 3 (unidades)
        semicirculo = Arc(
            radius=3 * scale_factor, 
            start_angle=0, 
            angle=PI, 
            fill_color=BLACK, 
            fill_opacity=1,
            stroke_width=0
        )
        semicirculo.move_to(ejes.c2p(6, 0), aligned_edge=DOWN)
        
        # Primero añadimos las figuras
        self.add(placa, semicirculo, hueco_rectangular)
        
        # Puntos característicos
        coordenadas = [
            (0, 0), (3, 0), (6, 0), (9, 0), (18, 0),
            (12, 10), (0, 10), (11, 2), (13, 6)
        ]
        puntos = VGroup(*[Dot(ejes.c2p(x, y), color=RED, radius=0.04) for x, y in coordenadas])
        self.add(puntos)
        
        # Luego añadimos los ejes y etiquetas para que queden al frente
        self.add(ejes, labels)
