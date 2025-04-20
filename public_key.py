from manim import *
import numpy as np


class IntroScene(Scene):
    def construct(self):
        title = Text("Открытый ключ (PublicKey)", font_size=48)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(1)
        self.play(FadeOut(title, shift=UP), run_time=1)
        self.wait(1)

        title = Text("В схеме гомоморфного шифрования CKKS", font_size=36)
        self.play(FadeIn(title, shift=UP), run_time=2)
        self.wait(1)


class PublicKeyScene(Scene):
    def construct(self):
        formula = MathTex(r"\text{PublicKey} = (b, a)", font_size=52)
        self.play(FadeIn(formula, shift=UP), run_time=1.5)
        self.wait(0.5)

        b = formula[0][11]  # символ b
        a = formula[0][13]  # символ a

        self.play(b.animate.scale(1.3).set_color(YELLOW), run_time=0.5)
        self.play(b.animate.scale(1/1.3).set_color(WHITE), run_time=0.5)

        self.play(a.animate.scale(1.3).set_color(YELLOW), run_time=0.5)
        self.play(a.animate.scale(1/1.3).set_color(WHITE), run_time=0.5)

        self.wait(1)


class AGeneration(Scene):
    def construct(self):
        a_coeffs = [5384, 3687, 1621, 4352, 7388, 370, 3112, 5389]
        q = 7681
        
        # Заголовок с Text (поддерживает кириллицу)
        title = Text("Коэффициенты полинома a ∈ [0, q−1]", font_size=36)
        title.to_edge(UP, buff=1.7)
        self.play(FadeIn(title, shift=UP), run_time=1)

        # Отдельные коэффициенты
        terms = VGroup()
        for i, coeff in enumerate(a_coeffs):
            term = MathTex(f"{coeff}", font_size=32)
            term.move_to(RIGHT * (i - len(a_coeffs)/2) * 1.2 + DOWN * 0.4)
            terms.add(term)

        self.play(LaggedStartMap(FadeIn, terms, lag_ratio=0.1), run_time=1.5)
        self.wait(0.5)

        # Центрированный полином
        poly_expr = " + ".join([
            f"{c}" if i == 0 else f"{c}x^{{{i}}}" for i, c in enumerate(a_coeffs)
        ])
        poly_tex = MathTex(f"a(x) = {poly_expr}", font_size=36)
        poly_tex.move_to(ORIGIN)

        self.play(FadeOut(terms), run_time=0.5)
        self.play(Write(poly_tex), run_time=1.5)
        self.wait(2)


class BGeneration(Scene):
    def construct(self):
        b_coeffs = [1776, 5323, 73, 4724, 2643, 1410, 1630, 6051]
        q = 7681

        # Формула
        formula = MathTex(
            r"b = -(a \cdot s) + e \mod q", font_size=48
        )
        formula.to_edge(UP, buff=1.4)

        self.play(Write(formula), run_time=1.5)
        self.wait(0.5)

        # Пояснения
        explanation = VGroup(
            Text("s — секретный ключ", font_size=28, color=BLUE),
            Text("e — небольшой шум", font_size=28, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(formula, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(FadeIn(explanation, shift=UP), run_time=1)
        self.wait(1)

        # Отображение полинома b(x)
        terms = VGroup()
        for i, coeff in enumerate(b_coeffs):
            if i == 0:
                term = MathTex(f"{coeff}", font_size=32)
            else:
                term = MathTex(f"{coeff}x^{{{i}}}", font_size=32)
            term.move_to(RIGHT * (i - len(b_coeffs)/2) * 1.2 + DOWN * 0.5)
            terms.add(term)

        self.play(LaggedStartMap(FadeIn, terms, lag_ratio=0.1), run_time=1.5)
        self.wait(0.5)

        # Объединённая запись b(x)
        poly_expr = " + ".join([
            f"{c}" if i == 0 else f"{c}x^{{{i}}}" for i, c in enumerate(b_coeffs)
        ])
        poly_tex = MathTex(f"b(x) = {poly_expr}", font_size=36)
        poly_tex.move_to(ORIGIN)

        self.play(FadeOut(terms), run_time=0.5)
        self.play(Write(poly_tex), run_time=1.5)
        self.wait(2)


class NoiseAndSecret(Scene):
    def construct(self):
        # === 1. Гауссов шум ===
        title = Text("e — небольшой шум", font_size=36)
        title.to_edge(UP, buff=0.7)
        self.play(FadeIn(title, shift=DOWN), run_time=1)

        graph = Axes(
            x_range=[-3, 3], y_range=[0, 1], axis_config={"include_tip": False},
            x_length=6, y_length=3
        )
        gaussian = graph.plot(lambda x: np.exp(-x**2), color=BLUE)
        e_label = MathTex("e", font_size=36).next_to(graph.c2p(0, 1), UP, buff=0.2)

        self.play(Create(graph), Create(gaussian), FadeIn(e_label))
        self.wait(0.5)

        # === 2. Полином шума в виде массива ===
        noise_poly = [3, 3, -3, -2, 1, 0, 4, 2]
        array_str = "[" + ", ".join(str(x) for x in noise_poly) + "]"
        noise_array = Text(array_str, font_size=30)
        noise_array.next_to(graph, DOWN, buff=0.8)

        self.play(FadeIn(noise_array))
        self.wait(1)

        self.play(FadeOut(VGroup(graph, gaussian, e_label, title, noise_array)))
        self.wait(0.3)

        # === 3. Секретный ключ как массив ===
        sk_title = Text("s — секретный ключ", font_size=36)
        sk_title.to_edge(UP, buff=0.7)
        self.play(FadeIn(sk_title, shift=DOWN), run_time=1)

        sk_poly = [0, 0, 0, 0, -1, 0, 1, -1]
        sk_str = "[" + ", ".join(str(x) for x in sk_poly) + "]"
        sk_array = Text(sk_str, font_size=30)
        sk_array.move_to(ORIGIN)

        self.play(FadeIn(sk_array))
        self.wait(2)


class EquationMeaning(Scene):
    def construct(self):
        # Шаг 1: заголовок
        title = Text("Математический смысл", font_size=36)
        title.to_edge(UP, buff=0.7)
        self.play(FadeIn(title, shift=DOWN))
        self.wait(0.5)

        # Шаг 2: Вывод — формула по частям
        a_dot_s = MathTex("a \\cdot s", font_size=48).move_to(LEFT * 3)
        plus_b = MathTex("+\\ b", font_size=48).next_to(a_dot_s, RIGHT)
        approx_e = MathTex("\\approx e\\ (\\mod\\ q)", font_size=48).next_to(plus_b, RIGHT)

        self.play(Write(a_dot_s))
        self.wait(0.3)
        self.play(Write(plus_b))
        self.wait(0.3)
        self.play(Write(approx_e))
        self.wait(1)

        # Шаг 3: Пояснение — текст
        explain_text = Text(
            "Пара (b, a) — это зашумлённое уравнение.\n"
            "Без знания s невозможно отделить e от полезной части.",
            font_size=28,
            line_spacing=1.3
        ).next_to(approx_e, DOWN, buff=1)
        self.play(FadeIn(explain_text, shift=UP), run_time=1.5)
        self.wait(2)

        # Шаг 4: Подсветим e (шум)
        self.play(approx_e.animate.set_color_by_tex("e", RED))
        self.wait(1)

        # Опционально: fade out всё
        self.play(FadeOut(VGroup(title, a_dot_s, plus_b, approx_e, explain_text)))
        self.wait(0.5)

