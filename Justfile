# Justfile for rendering Manim scenes

# Путь к python-файлу
FILE := "public_key_demo.py"

# Рендер всех сцен
render-all:
    manim -pql {{FILE}} IntroScene
    manim -pql {{FILE}} FormulaScene
    manim -pql {{FILE}} AGeneration
    manim -pql {{FILE}} NoiseAndSecret
    manim -pql {{FILE}} EquationMeaning
