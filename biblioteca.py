from manim import *
import numpy as np
from mnspy import *
from mnspy.utilidades import _formato_float_latex
from mnspy.ecuaciones_diferenciales_parciales.mef.ensamble import es_viga, es_resorte

mi_plantilla = TexTemplate()
mi_plantilla.add_to_preamble(r"\usepackage{cancel}")
mi_plantilla.add_to_preamble(r"\usepackage{xcolor}")


# config.tex_template = TexTemplate()
# config.tex_template.add_to_preamble(r"\usepackage{cancel}")
# config.tex_template.add_to_preamble(r"\usepackage{xcolor}")


class EnsambleAnimacion(Ensamble):
    def __init__(self, lista_elementos: list[Elemento], escala: float | int | None = None):
        super().__init__(lista_elementos)
        min_x, max_x = self._graf['lim_x'][0], self._graf['lim_x'][1]
        min_y, max_y = self._graf['lim_y'][0], self._graf['lim_y'][1]
        if min_y == np.inf and max_y == -np.inf:
            min_y = max_y = 0.0
        centro = ((min_x + max_x) / 2, (min_y + max_y) / 2)
        if 16.0 * (max_y - min_y) > 9.0 * (max_x - min_x):
            rango_y = [min_y, max_y, 1]
            rango_x = [centro[0] - 0.5 * (max_y - min_y) * 16 / 9, centro[0] + 0.5 * (max_y - min_y) * 16 / 9, 1]
        else:
            rango_x = [min_x, max_x, 1]
            rango_y = [centro[1] - 0.5 * (max_x - min_x) * 9 / 16, centro[1] + 0.5 * (max_x - min_x) * 9 / 16, 1]
        if escala is None:
            f_escala = 0.9 * 8.0 / (rango_y[1] - rango_y[0])
        else:
            f_escala = escala
        ejes_planos = NumberPlane(
            x_range=rango_x,
            y_range=rango_y,
            axis_config={
                "stroke_width": 0,  # Ejes más gruesos para resaltarlos
            },
            background_line_style={"stroke_opacity": 0.2}
        ).scale(f_escala)
        self.ejes = ejes_planos

    def c2p(self, coor: list[float | int] | ndarray):
        return self.ejes.c2p(coor)

    def ecuacion_vector_etiquetas_desplazamientos(self, EI_cte: bool = False, color_incognitas: ManimColor = BLUE,
                                                  reducida: bool = False, tol_cero: float = 1E-10,
                                                  formato: str = '{:.10g}') -> VMobject:
        etiquetas = []
        etiquetas_reducidas = []
        for item in self._lista_nodos:
            for n, gl in item.grados_libertad.items():
                if reducida and not gl.valor:
                    continue
                if self._union._k.grados is not None:
                    if n not in self._union._k.grados:
                        continue
                if item.rotado:
                    label = gl.label_desplazamiento_rotado + '_{' + item.nombre + '}'
                else:
                    label = gl.label_desplazamiento + '_{' + item.nombre + '}'
                if EI_cte and gl.valor:
                    if item.rotado:
                        label = label if gl.desplazamiento_rotado is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento_rotado, tol_cero, formato) + '/EI'
                    else:
                        label = label if gl.desplazamiento is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento, tol_cero, formato) + '/EI'
                else:
                    if item.rotado:
                        label = label if gl.desplazamiento_rotado is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento_rotado, tol_cero, formato)
                    else:
                        label = label if gl.desplazamiento is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento, tol_cero, formato)

                if gl.valor:
                    etiquetas_reducidas.append(label)
                etiquetas.append(label)
        return Matrix(np.array(etiquetas).reshape(-1, 1), element_to_mobject_config={
            "tex_to_color_map": {
                item: color_incognitas for item in etiquetas_reducidas
            }
        }, left_bracket=r"\{", right_bracket=r"\}")

    def ecuacion_vector_etiquetas_desplazamientos_elemento(self, elemento: Elemento, EI_cte: bool = False,
                                                           color_incognitas: ManimColor = BLUE,
                                                           reducida: bool = False, tol_cero: float = 1E-10,
                                                           formato: str = '{:.10g}') -> VMobject:
        etiquetas = []
        etiquetas_reducidas = []
        for item in elemento.get_lista_nodos():
            for n, gl in item.grados_libertad.items():
                if reducida and not gl.valor:
                    continue
                if elemento._k.grados is not None:
                    if n not in elemento._k.grados:
                        continue
                if item.rotado:
                    label = gl.label_desplazamiento_rotado + '_{' + item.nombre + '}'
                else:
                    label = gl.label_desplazamiento + '_{' + item.nombre + '}'
                if EI_cte and gl.valor:
                    if item.rotado:
                        label = label if gl.desplazamiento_rotado is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento_rotado, tol_cero, formato) + '/EI'
                    else:
                        label = label if gl.desplazamiento is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento, tol_cero, formato) + '/EI'
                else:
                    if item.rotado:
                        label = label if gl.desplazamiento_rotado is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento_rotado, tol_cero, formato)
                    else:
                        label = label if gl.desplazamiento is None else label + '=' + _formato_float_latex(
                            gl.desplazamiento, tol_cero, formato)

                if gl.valor:
                    etiquetas_reducidas.append(label)
                etiquetas.append(label)
        return Matrix(np.array(etiquetas).reshape(-1, 1), element_to_mobject_config={
            "tex_to_color_map": {
                item: color_incognitas for item in etiquetas_reducidas
            }
        }, left_bracket=r"\{", right_bracket=r"\}")

    def ecuacion_vector_etiquetas_fuerzas_internas_viga(self, ele: Viga, mostrar_valores: bool = False,
                                                        formato: str = '%.3g') -> VMobject:
        etiquetas_fuerzas = ele._obtener_etiquetas_fuerzas()
        if mostrar_valores:
            fuerzas = (np.matmul(ele._k.k,
                                 ele._obtener_desplazamientos()) - ele._obtener_fuerzas() - ele._obtener_fuerzas_por_rotula()).reshape(
                1, -1).flatten()
            etiquetas_fuerzas = etiquetas_fuerzas + np.array(['=', '=', '=', '=']) + np.char.mod(formato, fuerzas)
        return Matrix(np.array(etiquetas_fuerzas).reshape(-1, 1)
                      , left_bracket=r"\{", right_bracket=r"\}")

    def ecuacion_vector_etiquetas_reacciones(self, color_incognitas: ManimColor = BLUE,
                                             reducida: bool = False, tol_cero: float = 1E-10,
                                             formato: str = '{:.10g}') -> VMobject:
        mi_plantilla = TexTemplate()
        mi_plantilla.add_to_preamble(r"\usepackage{cancel}")
        etiquetas = []
        etiquetas_reducidas = []
        for item in self._lista_nodos:
            for n, gl in item.grados_libertad.items():
                if reducida and not gl.valor:
                    continue
                if self._union._k.grados is not None:
                    if n not in self._union._k.grados:
                        continue
                sub = gl.gl if 'eje' not in gl.gl else ''
                if item.rotado:
                    label = gl.label_reaccion_rotado
                else:
                    label = gl.label_reaccion
                label += '_{' + item.nombre + sub + '}'
                if gl.valor:
                    etiquetas.append(r'\cancel{' + label + '}')
                else:
                    if item.rotado:
                        label = label if gl.reaccion_rotado is None else label + '=' + _formato_float_latex(
                            gl.reaccion_rotado, tol_cero, formato)
                    else:
                        label = label if gl.reaccion is None else label + '=' + _formato_float_latex(gl.reaccion,
                                                                                                     tol_cero, formato)
                    etiquetas.append(label)
                    etiquetas_reducidas.append(label)
                    # _formato_float_latex(10)
        return Matrix(np.array(etiquetas).reshape(-1, 1), element_to_mobject_config={
            "tex_to_color_map": {
                item: color_incognitas for item in etiquetas_reducidas
            }, "tex_template": mi_plantilla,
        }, left_bracket=r"\{", right_bracket=r"\}")

    def ecuacion_vector_fuerzas_nodales(self, reducida: bool = False, **kwargs) -> VMobject:
        return ecuacion_array_a_matriz(np.array(self._union._k.obtener_fuerzas(reducida)), left_bracket=r"\{",
                                       right_bracket=r"\}", **kwargs)

    def ecuacion_matriz_rigidez_global(self, reducida: bool = False, **kwargs) -> VMobject:
        return ecuacion_array_a_matriz(np.array(self._union._k.obtener_matriz(reducida)), **kwargs)

    def sistema_ecuaciones_matriz_rigidez_global(self, EI_cte: bool = False, reducida: bool = False,
                                                 h_buff_k: float | int = 1.8) -> VMobject:
        vec_r_global = self.ecuacion_vector_etiquetas_reacciones(reducida=reducida)
        vec_f_global = self.ecuacion_vector_fuerzas_nodales(reducida=reducida)
        vec_k_global = self.ecuacion_matriz_rigidez_global(reducida=reducida, h_buff=h_buff_k)
        vec_d_global = self.ecuacion_vector_etiquetas_desplazamientos(EI_cte=EI_cte, reducida=reducida)
        if EI_cte:
            return VGroup(vec_r_global, ecuacion_signo_igual(), ecuacion_EI(), vec_k_global, vec_d_global,
                          ecuacion_signo_menos(), vec_f_global)
        else:
            return VGroup(vec_r_global, ecuacion_signo_igual(), vec_k_global, vec_d_global, ecuacion_signo_menos(),
                          vec_f_global)

    def get_cargas_puntuales(self, longitud: float | int = 2.0) -> VGroup:
        cargas = VGroup()
        for carga_puntual in self._lista_cargas_puntuales:
            p_1 = np.array(carga_puntual[1][0])
            p_2 = np.array(carga_puntual[1][1])
            p = p_1 + carga_puntual[2] * (p_2 - p_1) / np.linalg.norm(p_2 - p_1)
            cp = elemento_carga(p, self.ejes, longitud, ang=90, saliente=False, h=0.25 / 2)
            valor = MathTex(str(abs(carga_puntual[0])) + r"\,kN").next_to(cp, UP, buff=0.1).scale(0.5)
            cargas.add(cp)
            cargas.add(valor)
        return cargas

    def get_cargas_puntuales_nodales(self, longitud: float | int = 2.0) -> VGroup:
        cargas = VGroup()
        for n in self._lista_nodos:
            if n.fuerzas_externas.get('x', 0.0) != 0.0:
                sentido = True if n.fuerzas_externas['x'] > 0.0 else False
                p = n.punto
                cp = elemento_carga(p, self.ejes, longitud, ang=0, saliente=sentido, h=0.0)
                valor = MathTex(str(abs(n.fuerzas_externas['x'])) + r"\,kN").scale(0.5).next_to(cp, RIGHT, buff=0.1)
                cargas.add(cp)
                cargas.add(valor)
            if n.fuerzas_externas.get('y', 0.0) != 0.0:
                sentido = True if n.fuerzas_externas['y'] > 0.0 else False
                p = n.punto
                cp = elemento_carga(p, self.ejes, longitud, ang=90, saliente=sentido, h=0.0)
                valor = MathTex(str(abs(n.fuerzas_externas['y'])) + r"\,kN").scale(0.5).next_to(cp, UP, buff=0.1)
                cargas.add(cp)
                cargas.add(valor)
        return cargas

    def get_cargas_distribuidas(self, longitud: float | int = 2.0) -> VGroup:
        cargas = VGroup()
        for carga_distribuida in self._lista_cargas_distribuidas:
            cp = elemento_carga_distribuida(carga_distribuida[1][0], carga_distribuida[1][1], self.ejes, 0.25 / 2,
                                            saliente=False, longitud=longitud, n_cargas=20)
            valor_1 = MathTex(str(abs(carga_distribuida[0][0])) + r"\,kN/m").next_to(cp, UL, buff=0.0).scale(0.5).shift(
                RIGHT * 0.7)
            valor_2 = MathTex(str(abs(carga_distribuida[0][1])) + r"\,kN/m").next_to(cp, UR, buff=0.0).scale(0.5).shift(
                LEFT * 0.7)
            cargas.add(cp)
            cargas.add(valor_1)
            cargas.add(valor_2)
        return cargas

    def get_nodos_y_soportes(self) -> list[VGroup]:
        # Determinación de tipo de soporte
        # [Tipo Apoyo, Estilo]
        # Tipo Apoyo: 0 Pivotado, 1 empotrado
        # Estilo:
        #       Tipo Apoyo: 0 Pivotado
        #           0: inferior Móvil
        #           1: inferior Fijo
        #           2: superior Móvil
        #           3: superior Fijo
        #           4: izquierda Móvil
        #           5: izquierda Fijo
        #           6: derecha Móvil
        #           7: derecha Fijo
        #       Tipo Apoyo: 1 empotrado
        #           0: fijo izquierdo
        #           1: fijo derecha
        #           2: fijo inferior
        #           3: fijo superior
        #           4: fijo izquierdo con deslizadera
        #           5: fijo derecha con deslizadera
        #           6: fijo inferior con deslizadera
        #           7: fijo superior con deslizadera
        for n in self._lista_nodos:
            if 'x' in n.grados_libertad.keys():
                if n.grados_libertad['x'].valor:
                    if 'y' in n.grados_libertad.keys():
                        if n.grados_libertad['y'].valor:
                            if 'eje_z' in n.grados_libertad.keys():
                                if n.grados_libertad['eje_z'].valor:
                                    pass
                                    # Libre en los 3 grados
                                else:
                                    # Se mueve en x, y, y fijo en eje z
                                    # No válido o no implementado
                                    pass
                            else:
                                # Se mueve en x, y
                                pass
                        elif 'eje_z' in n.grados_libertad.keys():
                            if n.grados_libertad['eje_z'].valor:
                                # Se mueve en x y eje z, fijo en y
                                if n.punto[1] == self._graf['lim_y'][0]:
                                    i = 0
                                elif n.punto[1] == self._graf['lim_y'][1]:
                                    i = 2
                                else:
                                    i = 0
                                if len(n.get_soporte()) == 0:
                                    n.set_soporte([0, i])
                                # lista_soportes.append([n.punto[0:2], [0, i]])
                            else:
                                # Se mueve en x, y fijo en y, y eje z
                                # No válido o no implementado
                                pass
                        else:
                            # Se mueve en x, fijo en y
                            if n.punto[1] == self._graf['lim_y'][0]:
                                i = 0
                            elif n.punto[1] == self._graf['lim_y'][1]:
                                i = 2
                            else:
                                i = 0
                            if len(n.get_soporte()) == 0:
                                n.set_soporte([0, i])
                    elif 'eje_z' in n.grados_libertad.keys():
                        if n.grados_libertad['eje_z'].valor:
                            # Se mueve solo en x, y eje z
                            # Sería una viga vertical, no aplica
                            pass
                        else:
                            # Se mueve en x, y fijo en eje z
                            # No aplica
                            pass
                    else:
                        # Se mueve solo en x
                        pass
                elif 'y' in n.grados_libertad.keys():
                    if n.grados_libertad['y'].valor:
                        if 'eje_z' in n.grados_libertad.keys():
                            if n.grados_libertad['eje_z'].valor:
                                if n.punto[0] == self._graf['lim_x'][0]:
                                    i = 4
                                elif n.punto[0] == self._graf['lim_x'][1]:
                                    i = 6
                                else:
                                    i = 4
                                if len(n.get_soporte()) == 0:
                                    n.set_soporte([0, i])
                            else:
                                # Se mueve en x, y, y fijo en z
                                # No válido o no implementado
                                pass
                        else:
                            # Se mueve en y, fijo en x
                            if n.punto[0] == self._graf['lim_x'][0]:
                                i = 4
                            elif n.punto[0] == self._graf['lim_x'][1]:
                                i = 6
                            else:
                                i = 6
                            if len(n.get_soporte()) == 0:
                                n.set_soporte([0, i])
                    else:
                        if 'eje_z' in n.grados_libertad.keys():
                            if n.grados_libertad['eje_z'].valor:
                                # Fijo en x, y, y libre en eje z
                                if n.punto[1] == self._graf['lim_y'][0]:
                                    i = 1
                                elif n.punto[1] == self._graf['lim_y'][1]:
                                    i = 3
                                elif n.punto[0] == self._graf['lim_x'][0]:
                                    i = 5
                                elif n.punto[0] == self._graf['lim_x'][1]:
                                    i = 7
                                else:
                                    i = 1
                                if len(n.get_soporte()) == 0:
                                    n.set_soporte([0, i])
                            else:
                                # Fijo en x, y, y eje z aplica para marcos
                                if n.punto[1] == self._graf['lim_y'][0]:
                                    i = 2
                                elif n.punto[1] == self._graf['lim_y'][1]:
                                    i = 3
                                elif n.punto[0] == self._graf['lim_x'][0]:
                                    i = 0
                                elif n.punto[0] == self._graf['lim_x'][1]:
                                    i = 1
                                else:
                                    i = 0
                                if len(n.get_soporte()) == 0:
                                    n.set_soporte([1, i])
                                # lista_soportes.append([n.punto[0:2], [0, i]])
                        else:  # Solo grados x, y fijos
                            if n.punto[1] == self._graf['lim_y'][0]:
                                i = 1
                            elif n.punto[1] == self._graf['lim_y'][1]:
                                i = 3
                            elif n.punto[0] == self._graf['lim_x'][0]:
                                i = 5
                            elif n.punto[0] == self._graf['lim_x'][1]:
                                i = 7
                            else:
                                i = 1
                            if len(n.get_soporte()) == 0:
                                n.set_soporte([0, i])
                elif 'eje_z' in n.grados_libertad.keys():
                    if n.grados_libertad['eje_z'].valor:
                        # Se mueve solo en eje z, fijo en x
                        # No aplica
                        pass
                        # self._graf['ax'].plot(n.punto[0], n.punto[1], c='navy', marker='.')
                    else:
                        # Fijo en x, y eje z
                        # No aplica, sería viga vertical
                        pass
                else:
                    # Fijo en x
                    if n.punto[0] == self._graf['lim_x'][0]:
                        i = 0
                    elif n.punto[0] == self._graf['lim_x'][1]:
                        i = 1
                    else:
                        i = 0
                    if len(n.get_soporte()) == 0:
                        n.set_soporte([1, i])
                    # lista_soportes.append([n.punto[0:2], [1, i]])
            elif 'y' in n.grados_libertad.keys():
                if n.grados_libertad['y'].valor:
                    if 'eje_z' in n.grados_libertad.keys():
                        if n.grados_libertad['eje_z'].valor:
                            # Se mueve en y, y eje z
                            pass
                        else:
                            # Se mueve en y, y fijo en z
                            if n.punto[0] == self._graf['lim_x'][0]:
                                i = 4
                            elif n.punto[0] == self._graf['lim_x'][1]:
                                i = 5
                            else:
                                i = 4
                            if len(n.get_soporte()) == 0:
                                n.set_soporte([1, i])
                            pass
                    else:
                        # Se mueve en y
                        pass
                elif 'eje_z' in n.grados_libertad.keys():
                    if n.grados_libertad['eje_z'].valor:
                        # Fijo en y, y móvil en el eje z
                        if n.punto[1] == self._graf['lim_y'][0]:
                            i = 0
                        elif n.punto[1] == self._graf['lim_y'][1]:
                            i = 2
                        else:
                            i = 0
                        if len(n.get_soporte()) == 0:
                            n.set_soporte([0, i])
                        # lista_soportes.append([n.punto[0:2], [0, i]])
                    else:
                        # Fijo en y, y en el eje z
                        if n.punto[0] == self._graf['lim_x'][0]:
                            i = 0
                        elif n.punto[0] == self._graf['lim_x'][1]:
                            i = 1
                        else:
                            i = 0
                        if len(n.get_soporte()) == 0:
                            n.set_soporte([1, i])
                        # lista_soportes.append([n.punto[0:2], [1, i]])
                else:
                    # Fijo en y
                    if n.punto[1] == self._graf['lim_y'][0]:
                        i = 2
                    elif n.punto[1] == self._graf['lim_y'][1]:
                        i = 3
                    else:
                        i = 2
                    if len(n.get_soporte()) == 0:
                        n.set_soporte([1, i])
            else:
                # No valido ni grado x, ni y
                pass
        nodos = VGroup()
        label_nodos = VGroup().set_z_index(1.5)
        soportes = VGroup().set_z_index(1)
        for n in self._lista_nodos:
            nodos.add(Dot(self.ejes.c2p(n.punto), color=BLUE_A))
            label_nodos.add(
                LabeledDot(MathTex(n.nombre, color=WHITE), color=GREEN, stroke_color=GREEN, stroke_width=1,
                           fill_opacity=0.8).next_to(self.ejes.c2p(n.punto), DR, buff=-0.1).scale(0.5))
            tipo_sop = n.get_soporte()
            if len(tipo_sop) == 2:
                tipo, estilo = tipo_sop
                if tipo == 0:  # pivotado
                    if estilo == 0:  # móvil
                        soportes.add(elemento_soporte(n.punto, self.ejes, 0, ang=0))
                    elif estilo == 1:  # fijo
                        soportes.add(elemento_soporte(n.punto, self.ejes, 1, ang=0))
                    elif estilo == 2:  # móvil
                        soportes.add(elemento_soporte(n.punto, self.ejes, 0, ang=180))
                    elif estilo == 3:  # fijo
                        soportes.add(elemento_soporte(n.punto, self.ejes, 1, ang=180))
                    elif estilo == 4:  # móvil
                        soportes.add(elemento_soporte(n.punto, self.ejes, 0, ang=270))
                    elif estilo == 5:  # fijo
                        soportes.add(elemento_soporte(n.punto, self.ejes, 1, ang=270))
                    elif estilo == 6:  # móvil
                        soportes.add(elemento_soporte(n.punto, self.ejes, 0, ang=90))
                    elif estilo == 7:  # fijo
                        soportes.add(elemento_soporte(n.punto, self.ejes, 1, ang=90))
                elif tipo == 1:  # empotrado
                    if estilo == 0:  # izquierda
                        soportes.add(elemento_soporte(n.punto, self.ejes, 2, ang=0))
                    elif estilo == 1:  # derecha
                        soportes.add(elemento_soporte(n.punto, self.ejes, 2, ang=180))
                    elif estilo == 2:  # abajo
                        soportes.add(elemento_soporte(n.punto, self.ejes, 2, ang=90))
                    elif estilo == 3:  # arriba
                        soportes.add(elemento_soporte(n.punto, self.ejes, 2, ang=270))
                    elif estilo == 4:  # izquierda con deslizadera
                        soportes.add(elemento_soporte(n.punto, self.ejes, 3, ang=0))
                    elif estilo == 5:  # derecha con deslizadera
                        soportes.add(elemento_soporte(n.punto, self.ejes, 3, ang=180))
                    elif estilo == 6:  # abajo con deslizadera
                        soportes.add(elemento_soporte(n.punto, self.ejes, 3, ang=90))
                    elif estilo == 7:  # arriba con deslizadera
                        soportes.add(elemento_soporte(n.punto, self.ejes, 3, ang=270))
        return [nodos, label_nodos, soportes]

    def get_elementos(self) -> list[VGroup]:
        elementos = VGroup()
        label_elementos = VGroup().set_z_index(1.5)
        for el in self._lista_elementos:
            if es_viga(el):
                elementos.add(elemento_viga(el.get_nodo_inicial().punto[0], el.get_nodo_final().punto[0], 0.25, self.ejes))
            elif es_resorte(el):
                elementos.add(Resorte(el.get_nodo_inicial().punto, el.get_nodo_final().punto, n=40))
            punto_medio = self.ejes.c2p(
                (np.array(el.get_nodo_inicial().punto) + np.array(el.get_nodo_final().punto)) / 2)
            # 1. Crear solo el texto
            texto = MathTex(el.nombre, color=WHITE)

            # 2. Crear el fondo que envuelve automáticamente al texto
            fondo = SurroundingRectangle(
                texto,
                color=RED,  # Color del fondo
                fill_opacity=0.8,  # Opacidad
                stroke_width=1,  # Sin línea de borde
                buff=0.1  # Padding
            )
            # 3. Agrupar, escalar y posicionar
            etiqueta_completa = VGroup(fondo, texto).scale(0.5)
            etiqueta_completa.move_to(punto_medio).shift(DOWN * 0.4)
            # 4. Añadir a la colección
            label_elementos.add(etiqueta_completa)
        return [elementos, label_elementos]

    def elemento_fuerza_interna_viga(self, ele: Viga, unidades: list[str] | None = None,
                                     mostrar_valores: bool = False) -> VMobject:
        if unidades is None:
            unidades = [r"\,kN", r"\,kN\cdot m"]
        n_1 = ele.get_nodo_inicial()
        n_2 = ele.get_nodo_final()
        etiquetas_fuerzas = ele._obtener_etiquetas_fuerzas()
        sentido_fuerzas = np.array([True, True, True, True])
        if mostrar_valores:
            etiquetas_fuerzas = (np.matmul(ele._k.k,
                                           ele._obtener_desplazamientos()) - ele._obtener_fuerzas() - ele._obtener_fuerzas_por_rotula()).reshape(
                1, -1).flatten()
            sentido_fuerzas = (etiquetas_fuerzas > 0.0).reshape(1, -1).flatten()
            etiquetas_fuerzas = np.char.mod('%.3g', abs(etiquetas_fuerzas))
        fuerzas_internas = VGroup()
        f_1 = elemento_carga(n_1.punto, self.ejes, longitud=1, saliente=sentido_fuerzas[0], ang=90, color_carga=WHITE)
        label_f_1 = MathTex(etiquetas_fuerzas[0] + unidades[0]).next_to(f_1, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_1 = elemento_momento(n_1.punto, self.ejes, positivo=not sentido_fuerzas[1], color_carga=WHITE)
        label_m_1 = MathTex(etiquetas_fuerzas[1] + unidades[1]).next_to(m_1, UP, buff=-0.2, aligned_edge=LEFT).scale(
            0.5).shift(RIGHT * 0.4)
        f_2 = elemento_carga(n_2.punto, self.ejes, longitud=1, saliente=sentido_fuerzas[2], ang=90, color_carga=WHITE)
        label_f_2 = MathTex(etiquetas_fuerzas[2] + unidades[0]).next_to(f_2, UP, buff=0.0).scale(0.5).shift(
            RIGHT * 0.0)
        m_2 = elemento_momento(n_2.punto, self.ejes, positivo=not sentido_fuerzas[3], color_carga=WHITE)
        label_m_2 = MathTex(etiquetas_fuerzas[3] + unidades[1]).next_to(m_2, UP, buff=-0.2, aligned_edge=LEFT).scale(
            0.5).shift(RIGHT * 0.4)
        fuerzas_internas.add(VGroup(f_1, f_2, m_1, m_2))
        fuerzas_internas.add(VGroup(label_f_1, label_f_2, label_m_1, label_m_2))
        return fuerzas_internas

    def get_grados_libertad(self, n: Nodo, gl: str, **kwargs) -> VMobject:
        grados = elemento_grado_libertad(n.punto, self.ejes, gdl=gl, libre=n.grados_libertad[gl].valor, **kwargs)
        return grados


def elemento_viga(x_i: float, x_f: float, h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p((x_i, 0))
    coord_j = ejes.c2p((x_f, 0))
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    viga = Rectangle(height=h, width=L, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=1).move_to(centro)
    # nodo_i = Dot(coord_i, color=RED)
    # nodo_j = Dot(coord_j, color=RED)
    # return VGroup(viga, nodo_i, nodo_j)
    return viga


def elemento_armadura(nodo_i: tuple[float, float], nodo_j: tuple[float, float], h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0])

    # nodo_i = Dot(coord_i, color=RED)
    # nodo_j = Dot(coord_j, color=RED)
    armadura = RoundedRectangle(height=h, width=L + h, color=BLUE, fill_color=BLUE, fill_opacity=0.5,
                                corner_radius=h / 2, stroke_width=1)
    armadura.move_to(centro).rotate(angle=ang)
    # return VGroup(armadura, nodo_i, nodo_j)
    return armadura


def elemento_marco(nodo_i: tuple[float, float], nodo_j: tuple[float, float], h: float | int, ejes: Axes) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    centro = (coord_i + coord_j) / 2
    L = np.linalg.norm(coord_j - coord_i)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0])

    # nodo_i = Dot(coord_i, color=BLUE_A)
    # nodo_j = Dot(coord_j, color=BLUE_A)
    armadura = RoundedRectangle(height=h, width=L + h, color=BLUE, fill_color=BLUE, fill_opacity=1,
                                corner_radius=h / 2, stroke_width=0)
    armadura.move_to(centro).rotate(angle=ang)
    # return VGroup(armadura, nodo_i, nodo_j)
    return armadura


def elemento_soporte(nodo: tuple[float | int, float | int], ejes: Axes, tipo_soporte: int = 0,
                     ang: float = 0.0) -> VMobject:
    ang = np.deg2rad(ang)
    punto = ejes.c2p(*nodo)
    soporte = VGroup()
    achurado = VGroup()
    p_1 = punto + np.array([-0.3, -0.6, 0])
    p_2 = punto + np.array([0.3, -0.6, 0])
    if tipo_soporte == 0:  # pivotado móvil:
        pol = Polygon(punto, p_1, p_2, fill_color=GRAY_B, stroke_width=1, fill_opacity=0.95, color=WHITE)
        pol.rotate(ang, about_point=punto)
        for i in range(3):
            soporte.add(Circle(radius=0.1, color=WHITE, stroke_width=1).move_to(
                p_1 + np.array([i * 0.2 + 0.1, -0.1, 0.0])).rotate(ang, about_point=punto))
        soporte.add(pol)
        soporte.add(Circle(radius=0.05, color=WHITE, stroke_width=1).set_fill(BLACK, opacity=1).move_to(punto))
    elif tipo_soporte == 1:  # pivotado fijo
        pol = Polygon(punto, p_1, p_2, fill_color=GRAY_B, stroke_width=1, fill_opacity=0.95, color=WHITE)
        pol.rotate(ang, about_point=punto)
        h = 0.2
        for p in np.linspace(p_1, p_2 + np.array([h, 0.0, 0.0]), 10):
            r = h
            q = 0.0
            delta_r = p[0] - p_1[0]
            delta_q = p[0] - p_2[0]
            r = delta_r if delta_r < r else r
            q = q if delta_q < 0 else delta_q
            linea = Line(p - q * np.array([1, 1, 0]), p - r * np.array([1, 1, 0]), color=WHITE, stroke_width=1)
            achurado.add(linea)
        achurado.rotate(ang, about_point=punto)
        soporte.add(pol, achurado)
        soporte.add(Circle(radius=0.05, color=WHITE, stroke_width=1).set_fill(BLACK, opacity=1).move_to(punto))
    elif tipo_soporte == 2:  # empotrado por defecto empotrado izquierdo
        h = 0.3
        z = 0.5
        p_1 = punto + z * np.array([0, 1, 0])
        p_2 = punto - z * np.array([0, 1, 0])
        linea_base = Line(p_1, p_2, color=WHITE, stroke_width=4)
        linea_base.rotate(ang, about_point=punto)
        for p in np.linspace(p_1, p_2 + np.array([0.0, -h, 0.0]), 10):
            r = h
            q = 0.0
            delta_r = p_1[1] - p[1]
            delta_q = p_2[1] - p[1]
            r = delta_r if delta_r < r else r
            q = q if delta_q < 0 else delta_q
            linea = Line(p - q * np.array([1, -1, 0]), p - r * np.array([1, -1, 0]), color=WHITE, stroke_width=1)
            achurado.add(linea)
        achurado.rotate(ang, about_point=punto)
        soporte.add(linea_base, achurado)
    else:  # empotrado con rodamientos por defecto empotrado izquierdo
        h = 0.3
        z = 0.5
        p_1 = punto + z * np.array([0, 1, 0])
        p_2 = punto - z * np.array([0, 1, 0])
        linea_base = Line(p_1, p_2, color=WHITE, stroke_width=4)
        linea_base.rotate(ang, about_point=punto)
        for p in np.linspace(p_1, p_2 + np.array([0.0, -h, 0.0]), 10):
            r = h
            q = 0.0
            delta_r = p_1[1] - p[1]
            delta_q = p_2[1] - p[1]
            r = delta_r if delta_r < r else r
            q = q if delta_q < 0 else delta_q
            linea = Line(p - q * np.array([1, -1, 0]), p - r * np.array([1, -1, 0]), color=WHITE, stroke_width=1)
            achurado.add(linea)
        achurado.rotate(ang, about_point=punto)
        n_rod = 4
        for i in range(n_rod):
            soporte.add(Circle(radius=0.1, color=WHITE, stroke_width=1).move_to(
                p_1 + np.array([-(h + 0.1), -(i * (2 * z - 0.2) / (n_rod - 1) + 0.1), 0.0])).rotate(ang,
                                                                                                    about_point=punto))
        linea_base_2 = Line(p_1 - np.array([h, 0.0, 0.0]), p_2 - np.array([h, 0.0, 0.0]), color=WHITE, stroke_width=4)
        linea_base_2.rotate(ang, about_point=punto)
        soporte.add(linea_base, linea_base_2, achurado)
    return soporte


def elemento_direccion_eje(punto: tuple[float | int, float | int] | ndarray, longitud: float = 0.5, ang: float = 0.0,
                           color: ManimColor = BLUE, **kwargs) -> VMobject:
    ang = np.deg2rad(ang)
    inicio = punto
    final = np.array(inicio) + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    p_1 = np.array(inicio) + (np.array(
        [[np.cos(ang + np.pi / 2), -np.sin(ang + np.pi / 2), 0.0],
         [np.sin(ang + np.pi / 2), np.cos(ang + np.pi / 2), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[0.07], [0.0], [0.0]])).flatten()
    p_2 = np.array(inicio) + (np.array(
        [[np.cos(ang - np.pi / 2), -np.sin(ang - np.pi / 2), 0.0],
         [np.sin(ang - np.pi / 2), np.cos(ang - np.pi / 2), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[0.07], [0.0], [0.0]])).flatten()
    vector = Arrow(
        start=inicio,
        end=final,
        buff=0,  # ¡Fundamental para que toque los puntos exactamente!
        color=color,
        stroke_width=4,  # Grosor de la línea
        tip_shape=StealthTip,  # Aquí cambias la forma
        max_tip_length_to_length_ratio=0.10 / longitud  # Controla el tamaño de la punta
    )
    base = Line(p_1, p_2, stroke_width=2, color=color)
    return VGroup(vector, base, **kwargs)


def elemento_carga(nodo: tuple[float | int, float | int], ejes: Axes, longitud: float = 2.0, h: float | int = 0,
                   ang: float = 0.0, saliente: bool = True, color_carga: ManimColor = BLUE) -> VMobject:
    ang = np.deg2rad(ang)
    inicio = ejes.c2p(*nodo) + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    final = np.array(inicio) + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    if not saliente:
        inicio, final = final, inicio
    fuerza_arrow = Arrow(
        start=inicio,
        end=final,
        buff=0,  # ¡Fundamental para que toque los puntos exactamente!
        color=color_carga,
        stroke_width=4,  # Grosor de la línea
        tip_shape=StealthTip,  # Aquí cambias la forma
        max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
    )
    return fuerza_arrow


def elemento_carga_distribuida(nodo_i: tuple[float | int, float | int], nodo_j: tuple[float | int, float | int],
                               ejes: Axes, h: float | int = 0, longitud: float = 2.0, n_cargas: int = 10,
                               saliente=True) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0]) + np.pi / 2
    coord_i += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    coord_j += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    inicio_vec = np.linspace(coord_i, coord_j, n_cargas, axis=0)
    coord_f_i = coord_i + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    coord_f_j = coord_j + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud], [0.0], [0.0]])).flatten()
    final_vec = np.linspace(coord_f_i, coord_f_j, n_cargas, axis=0)
    carga_distribuida = VGroup()
    for i in range(n_cargas):
        inicio = inicio_vec[i]
        final = final_vec[i]
        if not saliente:
            inicio, final = final, inicio
        fuerza_arrow = Arrow(
            start=inicio,
            end=final,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=BLUE_D,
            stroke_width=4,  # Grosor de la línea
            tip_shape=StealthTip,  # Aquí cambias la forma
            max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
        )
        carga_distribuida.add(fuerza_arrow)
    return carga_distribuida


def elemento_carga_trapezoidal(nodo_i: tuple[float | int, float | int], nodo_j: tuple[float | int, float | int],
                               ejes: Axes, h: float | int = 0, longitud_i: float = 2.0, longitud_f: float = 2.0,
                               n_cargas: int = 10, saliente=True) -> VMobject:
    coord_i = ejes.c2p(*nodo_i)
    coord_j = ejes.c2p(*nodo_j)
    ang = np.arctan2(nodo_j[1] - nodo_i[1], nodo_j[0] - nodo_i[0]) + np.pi / 2
    coord_i += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    coord_j += (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[h], [0.0], [0.0]])).flatten()
    inicio_vec = np.linspace(coord_i, coord_j, n_cargas, axis=0)
    coord_f_i = coord_i + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud_i], [0.0], [0.0]])).flatten()
    coord_f_j = coord_j + (np.array(
        [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[longitud_f], [0.0], [0.0]])).flatten()
    final_vec = np.linspace(coord_f_i, coord_f_j, n_cargas, axis=0)
    carga_trapezoidal = VGroup()
    for i in range(n_cargas):
        inicio = inicio_vec[i]
        final = final_vec[i]
        longitud = np.linalg.norm(final - inicio)
        if not saliente:
            inicio, final = final, inicio
        if longitud > 0.05:
            fuerza_arrow = Arrow(
                start=inicio,
                end=final,
                buff=0,  # ¡Fundamental para que toque los puntos exactamente!
                color=BLUE_D,
                stroke_width=4,  # Grosor de la línea
                tip_shape=StealthTip,  # Aquí cambias la forma
                max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
            )
            carga_trapezoidal.add(fuerza_arrow)
    return carga_trapezoidal


def elemento_momento(nodo: tuple[float | int, float | int], ejes: Axes, radio: float = 0.5,
                     ang: float = 0.0, positivo: bool = True, color_carga: ManimColor = GREEN) -> VMobject:
    ang_i = np.deg2rad(90)
    ang_f = np.deg2rad(325)
    ang = np.deg2rad(ang)
    centro = ejes.c2p(*nodo)
    inicio = np.array(centro) + (np.array(
        [[np.cos(ang_i), -np.sin(ang_i), 0.0], [np.sin(ang_i), np.cos(ang_i), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[radio], [0.0], [0.0]])).flatten()
    final = np.array(centro) + (np.array(
        [[np.cos(ang_f), -np.sin(ang_f), 0.0], [np.sin(ang_f), np.cos(ang_f), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
        [[radio], [0.0], [0.0]])).flatten()
    if positivo:
        inicio, final = final, inicio
        ang_i, ang_f = ang_f, ang_i
    momento = CurvedArrow(
        start_point=inicio,
        end_point=final,
        angle=ang_f - ang_i,  # Ángulo de la curvatura de la flecha
        stroke_width=4,  # Grosor de la línea
        tip_length=0.25,  # Controla el tamaño absoluto de la punta
        tip_shape=StealthTip,  # Aquí cambias la forma
        color=color_carga
    ).move_arc_center_to(centro).rotate(ang, about_point=centro)
    return momento


def elemento_grado_libertad(nodo: tuple[float | int, float | int], ejes: Axes, longitud: float = 0.5,
                            offset: float = 0.0, gdl: str = 'x', libre: bool = True, color: None | str = None,
                            ang: float | int = 0.0) -> VMobject:
    if color is None:
        color = RED if not libre else GREEN
    if gdl == 'x':
        ang = np.deg2rad(ang)  # usado cuando el gdl está rotado
        inicio = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[-longitud / 2 + offset], [0.0], [0.0]])).flatten()
        final = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[longitud / 2 + offset], [0.0], [0.0]])).flatten()
        grado_libertad = DoubleArrow(
            start=inicio,
            end=final,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=color,
            stroke_width=4,  # Grosor de la línea
            tip_shape_start=StealthTip,
            tip_shape_end=StealthTip,
            max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
        )
    elif gdl == 'y':
        ang = np.deg2rad(ang)  # usado cuando el gdl está rotado
        inicio = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[0.0], [-longitud / 2 + offset], [0.0]])).flatten()
        final = ejes.c2p(*nodo) + (np.array(
            [[np.cos(ang), -np.sin(ang), 0.0], [np.sin(ang), np.cos(ang), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[0.0], [longitud / 2 + offset], [0.0]])).flatten()
        grado_libertad = DoubleArrow(
            start=inicio,
            end=final,
            buff=0,  # ¡Fundamental para que toque los puntos exactamente!
            color=color,
            stroke_width=4,  # Grosor de la línea
            tip_shape_start=StealthTip,
            tip_shape_end=StealthTip,
            max_tip_length_to_length_ratio=0.15 / longitud  # Controla el tamaño de la punta
        )
    else:
        radio = longitud / 2
        ang_i = np.deg2rad(90)
        ang_f = np.deg2rad(270)
        ang = np.deg2rad(offset)
        centro = ejes.c2p(*nodo)
        inicio = np.array(centro) + (np.array(
            [[np.cos(ang_i), -np.sin(ang_i), 0.0], [np.sin(ang_i), np.cos(ang_i), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[radio], [0.0], [0.0]])).flatten()
        final = np.array(centro) + (np.array(
            [[np.cos(ang_f), -np.sin(ang_f), 0.0], [np.sin(ang_f), np.cos(ang_f), 0.0], [0.0, 0.0, 0.0]]) @ np.array(
            [[radio], [0.0], [0.0]])).flatten()

        grado_libertad = CurvedDoubleArrow(
            start_point=inicio,
            end_point=final,
            angle=ang_f - ang_i,  # Ángulo de la curvatura de la flecha
            stroke_width=4,  # Grosor de la línea
            tip_length=0.15,  # Controla el tamaño absoluto de la punta
            tip_shape_start=StealthTip,
            tip_shape_end=StealthTip,
            color=color
        ).move_arc_center_to(centro).rotate(ang, about_point=centro)
    return grado_libertad


def crear_cota(p1, p2, texto, color=WHITE, tamano_remate=0.15):
    grupo_cota = VGroup()

    # 1. La línea principal de la cota
    linea_principal = Line(p1, p2, color=color, stroke_width=2)

    # 2. Matemáticas para los remates (ticks) perpendiculares
    vector = p2 - p1
    # Calculamos el vector normal (perpendicular) rotando 90 grados
    normal = np.array([-vector[1], vector[0], 0])
    normal = normal / np.linalg.norm(normal)  # Normalizamos a longitud 1

    # 3. Crear los remates en ambos extremos
    remate_inicio = Line(
        p1 - normal * tamano_remate,
        p1 + normal * tamano_remate,
        color=color, stroke_width=2
    )
    remate_fin = Line(
        p2 - normal * tamano_remate,
        p2 + normal * tamano_remate,
        color=color, stroke_width=2
    )

    # 4. Configurar el texto (Etiqueta)
    etiqueta = MathTex(texto, color=color).scale(0.7)
    # Fondo para que la línea principal no tache el número
    etiqueta.add_background_rectangle(color=BLACK, opacity=1, buff=0.1)
    etiqueta.move_to(linea_principal.get_center())

    # 5. Rotar el texto para que se alinee con la cota
    angulo = np.arctan2(vector[1], vector[0])
    # Si la cota está "al revés", rotamos 180° extra para que el texto no quede de cabeza
    if abs(angulo) > PI / 2:
        angulo -= PI
    etiqueta.rotate(angulo)

    # 6. Agrupar todo
    grupo_cota.add(linea_principal, remate_inicio, remate_fin, etiqueta)
    return grupo_cota


def ecuacion_matriz_rigidez_viga() -> VMobject:
    factor_matrix_rigidez = MathTex(r'\dfrac{EI}{L^{3}}')
    matrix_rigidez = Matrix(
        [['12', '6L', '-12', '6L'],
         ['6L', '4L^{2}', '-6L', '2L^{2}'],
         ['-12', '-6L', '12', '-6L'],
         ['6L', '2L^{2}', '-6L', '4L^{2}']]
    )
    return VGroup(factor_matrix_rigidez, matrix_rigidez)


def ecuacion_vector_fuerza_viga(id_elemento: int | str = '1', id_nodo_inicial: int | str = '1',
                                id_nodo_final: int | str = '2') -> VMobject:
    str_elemento = str(id_elemento)
    str_nodo_ini = str(id_nodo_inicial)
    str_nodo_fin = str(id_nodo_final)
    vector_fuerzas = Matrix(
        [["f^{(" + str_elemento + ")}_{" + str_nodo_ini + "y}"],
         ["m^{(" + str_elemento + ")}_{" + str_nodo_ini + "}"],
         ["f^{(" + str_elemento + ")}_{" + str_nodo_fin + "y}"], ["m^{(" + str_elemento + ")}_{" + str_nodo_fin + "}"]],
        left_bracket=r"\{",  # Llave izquierda
        right_bracket=r"\}"  # Llave derecha
    )
    return vector_fuerzas


def ecuacion_vector_desplazamiento_viga(id_nodo_inicial: int | str = '1', id_nodo_final: int | str = '2') -> VMobject:
    str_nodo_ini = str(id_nodo_inicial)
    str_nodo_fin = str(id_nodo_final)
    vector_deformacion = Matrix(
        [["v_{" + str_nodo_ini + "}"],
         [r"\phi_{" + str_nodo_ini + "}"],
         ["v_{" + str_nodo_fin + "}"],
         [r"\phi_{" + str_nodo_fin + "}"]
         ],
        left_bracket=r"\{",  # Llave izquierda
        right_bracket=r"\}"  # Llave derecha
    )
    return vector_deformacion


def ecuacion_vector_fuerza_nodal_equivalente_viga(id_nodo_inicial: int | str = '1',
                                                  id_nodo_final: int | str = '2') -> VMobject:
    str_nodo_ini = str(id_nodo_inicial)
    str_nodo_fin = str(id_nodo_final)
    vector_fuerzas_nodal = Matrix(
        [["f_{" + str_nodo_ini + "y_{0}}"],
         ["m_{" + str_nodo_ini + "_{0}}"],
         ["f_{" + str_nodo_fin + "y_{0}}"], ["m_{" + str_nodo_fin + "_{0}}"]],
        left_bracket=r"\{",  # Llave izquierda
        right_bracket=r"\}"  # Llave derecha
    )
    return vector_fuerzas_nodal


def ecuacion_array_a_matriz(arr: np.ndarray, formato_num: str = "{x:g}", **kwargs) -> VMobject:
    if arr.ndim == 1:
        kwargs.setdefault("left_bracket", r"\{")
        kwargs.setdefault("right_bracket", r"\}")
        # Usamos .format(x=x) para inyectar el valor en la plantilla
        data = [[formato_num.format(x=x)] for x in arr]
        return Matrix(data, **kwargs)

    data = [[formato_num.format(x=x) for x in row] for row in arr]
    return Matrix(data, **kwargs)


def ecuacion_signo_igual():
    return MathTex('=')


def ecuacion_signo_menos():
    return MathTex('-')


def ecuacion_signo_mas():
    return MathTex('+')


def ecuacion_EI():
    return MathTex('EI')


def ecuacion_EI_inv():
    return MathTex(r'\dfrac{1}{EI}')


def ecuacion_vector_deformaciones(reducida: bool = False):
    return MathTex(r'\dfrac{1}{EI}')


def elemento_label_grados_libertad(n: Nodo, **kwargs) -> VGroup:
    label_grados = VGroup()
    for k, v in n.grados_libertad.items():
        if n.rotado:
            label = n.grados_libertad[k].label_desplazamiento_rotado
        else:
            label = n.grados_libertad[k].label_desplazamiento
        label += '_{' + n.nombre + '}'
        if n.rotado:
            label = label if n.grados_libertad[
                                 k].desplazamiento_rotado is None else label + '=' + _formato_float_latex(
                n.grados_libertad[k].desplazamiento_rotado)
        else:
            label = label if n.grados_libertad[k].desplazamiento is None else label + '=' + _formato_float_latex(
                n.grados_libertad[k].desplazamiento)
        if n.grados_libertad[k].valor:
            color = BLUE
        else:
            color = RED
        label_gl = MathTex(label, color=color, **kwargs)
        label_grados.add(label_gl)
    return label_grados


def titulo(titulo: str, subtitulo: str = '', size_titulo: int = 48) -> VMobject:
    titulo = Text(titulo, font_size=size_titulo, color=BLUE)
    linea = Underline(titulo, color=WHITE)
    if subtitulo != '':
        subtitulo = Text(subtitulo, font_size=28, color=GRAY)
        subtitulo.next_to(linea, DOWN, buff=0.5)
        todo = VGroup(titulo, linea, subtitulo).move_to(ORIGIN)
    else:
        todo = VGroup(titulo, linea).move_to(ORIGIN)
    return todo


def animacion_titulo(titulo: str, subtitulo: str = '') -> VMobject:
    titulo = Text(titulo, font_size=40, color=WHITE)
    caja = BackgroundRectangle(
        titulo,
        buff=0.4,
        color=RED,
        fill_opacity=0.2,
        stroke_width=2,
        stroke_color=RED
    )
    if subtitulo != '':
        subtitulo = Text(subtitulo, font_size=32, color=BLUE_A).shift(DOWN * 1.2)
        todo = VGroup(titulo, caja, subtitulo).move_to(ORIGIN)
    else:
        todo = VGroup(titulo, caja).move_to(ORIGIN)
    return todo


def elemento_tabla(encabezado: list, datos: list, color_tabla: ManimColor = TEAL_C,
                   color_encabezado: ManimColor = TEAL_C) -> VMobject:
    tabla = Table(
        datos,
        col_labels=encabezado.copy(),
        include_outer_lines=True,
        v_buff=0.35,
        h_buff=0.6,
        line_config={"stroke_width": 1.0, "color": color_tabla},
        element_to_mobject=MathTex,
    )
    encabezado = tabla.get_rows()[0]
    encabezado.set_color(color_encabezado)
    lineas_h = tabla.get_horizontal_lines()
    cuadricula = VGroup(
        tabla.get_horizontal_lines(),
        tabla.get_vertical_lines()
    )
    linea_sup = lineas_h[0]
    linea_inf = lineas_h[2]
    fondo_encabezado = Rectangle(
        width=linea_sup.width,  # Toma el ancho exacto de la tabla
        height=abs(linea_sup.get_y() - linea_inf.get_y()),  # Calcula el alto exacto de la celda
        color=color_encabezado,
        fill_opacity=0.2,
        stroke_width=1
    ).move_to((linea_sup.get_center() + linea_inf.get_center()) / 2)
    return VGroup(tabla, cuadricula, fondo_encabezado)


class SegmentoResorte(VMobject):
    """Clase auxiliar para dibujar un eslabón individual del resorte."""

    def __init__(self, p_1, p_2, t, **kwargs):
        super().__init__(**kwargs)

        # Asegurar que los puntos sean arreglos de Manim (3D)
        p_1 = np.array(p_1)
        p_2 = np.array(p_2)

        dx = p_2[0] - p_1[0]
        dy = p_2[1] - p_1[1]
        l_res = np.sqrt(dx ** 2 + dy ** 2)

        if l_res == 0:
            return

        c = dx / l_res
        s = dy / l_res

        x_1, y_1 = p_1[:2]
        x_2, y_2 = p_2[:2]

        # Cálculo de los vértices (manteniendo z=0)
        v0 = np.array([x_1 + 0.5 * t * s, y_1 - 0.5 * t * c, 0])
        v1 = np.array([x_2 + 0.5 * t * s, y_2 - 0.5 * t * c, 0])
        v2 = np.array([x_2 + 0.5 * t * s + 0.7 * t * c, y_2 - 0.5 * t * c + 0.7 * t * s, 0])
        v3 = np.array([x_2 - 0.5 * t * s + 0.7 * t * c, y_2 + 0.5 * t * c + 0.7 * t * s, 0])
        v4 = np.array([x_2 - 0.5 * t * s, y_2 + 0.5 * t * c, 0])
        v5 = np.array([x_1 - 0.5 * t * s, y_1 + 0.5 * t * c, 0])
        v6 = np.array([x_1 - 0.5 * t * s - 0.7 * t * c, y_1 + 0.5 * t * c - 0.7 * t * s, 0])
        v7 = np.array([x_1 + 0.5 * t * s - 0.7 * t * c, y_1 - 0.5 * t * c - 0.7 * t * s, 0])
        v8 = np.array([x_1 + 0.5 * t * s, y_1 - 0.5 * t * c, 0])

        # Trazado equivalente a Matplotlib (MOVETO, LINETO, CURVE4...)
        self.start_new_path(v0)
        self.add_line_to(v1)
        self.add_cubic_bezier_curve_to(v2, v3, v4)
        self.add_line_to(v5)
        self.add_cubic_bezier_curve_to(v6, v7, v8)


class Resorte(VGroup):
    """Objeto Manim que genera un resorte completo."""

    def __init__(self, p_1, p_2, n=30, porc_h: float = 0.1, **kwargs):
        super().__init__(**kwargs)

        p_1 = np.array(p_1)
        p_2 = np.array(p_2)

        dx = p_2[0] - p_1[0]
        dy = p_2[1] - p_1[1]
        l_res = np.sqrt(dx ** 2 + dy ** 2)

        if l_res == 0:
            return

        h = porc_h * l_res
        t = 0.25 * h

        c = dx / l_res
        s = dy / l_res

        x = np.linspace(p_1[0], p_2[0], n)
        y = np.linspace(p_1[1], p_2[1], n)

        # Desplazamiento en zigzag
        for i in range(n - 4):
            if i % 2 == 0:
                x[i + 2] -= h * s
                y[i + 2] += h * c
            else:
                x[i + 2] += h * s
                y[i + 2] -= h * c

        puntos = [np.array([x[i], y[i], 0]) for i in range(n)]

        # Dibujar parte trasera (índices impares)
        for i in range(n - 1):
            if i % 2 == 1:
                segmento = SegmentoResorte(
                    puntos[i], puntos[i + 1], t,
                    fill_color="#4682B4",  # Equivalente a 'steelblue'
                    fill_opacity=1.0,
                    stroke_width=0.0,
                    stroke_color=WHITE  # Ajuste para visibilidad en fondo oscuro
                )
                self.add(segmento)

        # Dibujar parte delantera (índices pares)
        for i in range(n - 1):
            if i % 2 == 0:
                segmento = SegmentoResorte(
                    puntos[i], puntos[i + 1], t,
                    fill_color="#B0C4DE",  # Equivalente a 'lightsteelblue'
                    fill_opacity=1.0,
                    stroke_color="#4169E1",  # Equivalente a 'royalblue'
                    stroke_width=0.0
                )
                self.add(segmento)


def main():
    class demo(Scene):
        def construct(self):
            ejes_coordenados = Axes(
                x_range=[0, 16, 1],
                y_range=[0, 9, 1],
                x_length=16,
                y_length=9,
                axis_config={"include_tip": False, "stroke_width": 2}
            ).scale(0.8)
            ejes_planos = NumberPlane(
                x_range=[0, 10, 1],
                y_range=[0, 8, 1],
                background_line_style={
                    "stroke_opacity": 0.1  # Puedes atenuar las líneas de la cuadrícula si no las quieres ver
                }
            )
            ejes_planos.to_edge(DOWN + LEFT)
            ejes = ejes_planos
            viga = elemento_viga(5, 10, 0.5, ejes)
            armadura = elemento_armadura((0, 0), (5, 5), 0.5, ejes)
            marco = elemento_marco((5, 5), (10, 2), 0.5, ejes)
            fuerza = elemento_carga((10, 2), ejes, ang=30, saliente=False, longitud=4)
            momento = elemento_momento((5, 5), ejes, ang=90, positivo=False)
            carga_d = elemento_carga_distribuida((0, 0), (5, 5), ejes, 0.5 / 2, 1, 20, saliente=False)
            carga_d2 = elemento_carga_trapezoidal((5, 5), (10, 2), ejes, 0.5 / 2, 0, 2.5, 20, saliente=False)
            carga_d2.set_color(BLUE)
            sop = elemento_soporte((1, 1), ejes, 0, 45)
            sop_2 = elemento_soporte((5, 2), ejes, 2, 0)
            sop_3 = elemento_soporte((6, 2), ejes, 3, 180)
            test = np.array([1, 2, 3])
            self.play(FadeIn(ecuacion_array_a_matriz(test, left_bracket=r"[", right_bracket=r"]")), run_time=2)
            mi_plantilla = TexTemplate()
            mi_plantilla.add_to_preamble(r"\usepackage{cancel}")

            # 2. Tu arreglo (nota el uso de r"" en \cancel para evitar errores de Python)
            test = np.array(
                ['F_{1y}', 'M_{1}', 'F_{2y}', 'M_{2}', 'F_{3y}', r'\cancel{M_{3}}', 'F_{4y}', 'M_{4}']).reshape((-1, 1))

            # 3. Crear la matriz pasando la plantilla a los elementos internos
            matriz = Matrix(
                test,
                left_bracket=r"[",
                right_bracket=r"]",
                # Esto le dice a Manim que use tu plantilla para compilar cada entrada
                element_to_mobject_config={"tex_template": mi_plantilla}
            )

            self.play(FadeIn(matriz), run_time=2)
            self.play(FadeIn(ejes), run_time=2)
            # self.play(FadeIn(viga[1], viga[2]), run_time=2)
            self.play(FadeIn(viga[0]), run_time=2)
            self.play(FadeIn(armadura), run_time=2)
            self.play(FadeIn(carga_d2), run_time=2)
            self.play(FadeIn(crear_cota(ejes.c2p([2, 1, 0]), ejes.c2p([8, 1, 0]), r'6\,m', GRAY, 0.15)), run_time=2)
            # self.add(ejes)
            # self.add(armadura)
            # self.add(viga)
            self.add(marco)
            self.add(fuerza)
            self.add(momento)
            self.add(carga_d)
            self.add(sop)
            self.add(sop_2)
            self.add(sop_3)
            self.wait(2)

    demo().render()


if __name__ == '__main__':
    main()
