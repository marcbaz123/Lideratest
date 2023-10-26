from experta import Rule, Fact, KnowledgeEngine, P

class EstiloLiderazgo(Fact):
    pass

class MotorLiderazgo(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.resultado = ""  # Variable para almacenar el resultado

    @Rule(
        EstiloLiderazgo(total_orientacion_personas=P(lambda x: x <= 5), total_orientacion_produccion=P(lambda x: x <= 5))
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
