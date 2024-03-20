from experta import Rule, Fact, KnowledgeEngine, P

class EstiloLiderazgo(Fact): #Clase que hereda de Fact, es una clase base que proporciona experta para representar hechos de reglas
    pass

class MotorLiderazgo(KnowledgeEngine): #Clase que hereda de KnowledgeEngine, es la clase principal que define y ejecuta motores de inferencia en experta 
    
    def __init__(self):
        super().__init__() #Se llama al constructor de la clase base para inicializar el motor de inferencia
        self.resultado = ""  # Variable para almacenar el resultado

    #Ej SIN USAR LAMBDA
    
# def condicion_menor_o_igual_a_5(x):
#    return x <= 5

# def condicion_mayor_o_igual_a_5_punto_1(x):
#    return x >= 5.1

# @Rule(
#     EstiloLiderazgo(total_orientacion_personas=P(condicion_menor_o_igual_a_5), total_orientacion_produccion=P(condicion_menor_o_igual_a_5))
# )
# def rule_ajeno(self):
# Acciones de la regla
    
    @Rule(
        EstiloLiderazgo(total_orientacion_personas=P(lambda x: x <= 5), total_orientacion_produccion=P(lambda x: x <= 5)) #Lambda se utiliza en conjunto con el modulo P de experta oara definir condiciones especificas que determinan cuando se activa una regla
    )
    def rule_ajeno(self):
        self.resultado = "Estilo de liderazgo: Ajeno (Indiferente en lo social y en las tareas)"
      
        self.declare(EstiloLiderazgo(resultado=self.resultado))

    @Rule(
        EstiloLiderazgo(total_orientacion_personas=P(lambda x: x >= 5.1), total_orientacion_produccion=P(lambda x: x <= 5))
    )
    def rule_social(self):
        self.resultado = "Estilo de liderazgo: Social (Centrado en lo social)"
    
        self.declare(EstiloLiderazgo(resultado=self.resultado))

    @Rule(
        EstiloLiderazgo(total_orientacion_personas=P(lambda x: x <= 5), total_orientacion_produccion=P(lambda x: x >= 5.1))
    )
    def rule_autoritario(self):
        self.resultado = "Estilo de liderazgo: Autoritario (Centrado en las tareas)"
      
        self.declare(EstiloLiderazgo(resultado=self.resultado))

    @Rule(
        EstiloLiderazgo(total_orientacion_personas=P(lambda x: x >= 5.1), total_orientacion_produccion=P(lambda x: x >= 5.1))
    )
    def rule_equipo(self):
        self.resultado = "Estilo de liderazgo: Líder de equipo (Centrado en lo social y en las tareas)"
      
        self.declare(EstiloLiderazgo(resultado=self.resultado))
