"""
Update ele304.ts with RA/CE data from CATEDU for the 5 missing modules.
"""
import json
import re

# Data from CATEDU (manually extracted from fetch results)
MODULES_DATA = {
    "1665": {
        "name": "Digitalización aplicada a los sectores productivos (GS)",
        "hours": 33,
        "course": "1º",
        "ras": [
            {
                "id": "RA1",
                "descripcion": "Analiza el concepto de digitalización y su repercusión en los sectores productivos teniendo en cuenta la actividad de la empresa e identificando entornos IT (Information Technology: tecnología de la información) y OT (Operation Technology: tecnología de operación) característicos",
                "criterios_evaluacion": [
                    {"id": "CE1.1", "descripcion": "Se ha descrito en qué consiste el concepto de digitalización"},
                    {"id": "CE1.2", "descripcion": "Se ha relacionado la implantación de la tecnología digital con la organización de las empresas"},
                    {"id": "CE1.3", "descripcion": "Se han establecido las diferencias y similitudes entre los entornos IT y OT"},
                    {"id": "CE1.4", "descripcion": "Se han identificado los departamentos típicos de las empresas que pueden constituir entornos IT"},
                    {"id": "CE1.5", "descripcion": "Se han seleccionado las tecnologías típicas de la digitalización en planta y en negocio"},
                    {"id": "CE1.6", "descripcion": "Se ha analizado la importancia de la conexión entre entornos IT y OT"},
                    {"id": "CE1.7", "descripcion": "Se han analizado las ventajas de digitalizar una empresa industrial de extremo a extremo"}
                ]
            },
            {
                "id": "RA2",
                "descripcion": "Caracteriza las tecnologías habilitadoras digitales necesarias para la adecuación/transformación de las empresas a entornos digitales describiendo sus características y aplicaciones",
                "criterios_evaluacion": [
                    {"id": "CE2.1", "descripcion": "Se han identificado las principales tecnologías habilitadoras digitales"},
                    {"id": "CE2.2", "descripcion": "Se han relacionado las THD con el desarrollo de productos y servicios"},
                    {"id": "CE2.3", "descripcion": "Se ha relacionado la importancia de las THD con la economía sostenible y eficiente"},
                    {"id": "CE2.4", "descripcion": "Se han identificado nuevos mercados generados por las THD"},
                    {"id": "CE2.5", "descripcion": "Se ha analizado la implicación de THD tanto en la parte de negocio como en la parte de planta"},
                    {"id": "CE2.6", "descripcion": "Se han identificado las mejoras producidas debido a la implantación de las tecnologías habilitadoras en relación con los entornos IT y OT"},
                    {"id": "CE2.7", "descripcion": "Se ha elaborado un informe que relacione, las tecnologías con sus características y áreas de aplicación"}
                ]
            },
            {
                "id": "RA3",
                "descripcion": "Identifica sistemas basados en cloud/nube y su influencia en el desarrollo de los sistemas digitales",
                "criterios_evaluacion": [
                    {"id": "CE3.1", "descripcion": "Se han identificado los diferentes niveles de la cloud/nube"},
                    {"id": "CE3.2", "descripcion": "Se han identificado las principales funciones de la cloud/nube (procesamiento de datos, intercambio de información, ejecución de aplicaciones, entre otros)"},
                    {"id": "CE3.3", "descripcion": "Se ha descrito el concepto de edge computing y su relación con la cloud/nube"},
                    {"id": "CE3.4", "descripcion": "Se han definido los conceptos de fog y mist y sus zonas de aplicación en el conjunto"},
                    {"id": "CE3.5", "descripcion": "Se han identificado las ventajas que proporciona la utilización de la cloud/nube en los sistemas conectados"}
                ]
            },
            {
                "id": "RA4",
                "descripcion": "Identifica aplicaciones de la IA (inteligencia artificial) en entornos del sector donde está enmarcado el título describiendo las mejoras implícitas en su implementación",
                "criterios_evaluacion": [
                    {"id": "CE4.1", "descripcion": "Se ha identificado la importancia de la IA en la automatización de procesos y su optimización"},
                    {"id": "CE4.2", "descripcion": "Se ha relacionado la IA con la recogida masiva de datos (Big Data) y su tratamiento (análisis) con la rentabilidad de las empresas"},
                    {"id": "CE4.3", "descripcion": "Se ha valorado la importancia presente y futura de la IA"},
                    {"id": "CE4.4", "descripcion": "Se han identificado los sectores con implantación más relevante de IA"},
                    {"id": "CE4.5", "descripcion": "Se han identificado los lenguajes de programación en IA"},
                    {"id": "CE4.6", "descripcion": "Se ha descrito como influye la IA en el sector del título"}
                ]
            },
            {
                "id": "RA5",
                "descripcion": "Evalúa la importancia de los datos, así como su protección en una economía digital globalizada, definiendo sistemas de seguridad y ciberseguridad tanto a nivel de equipo/sistema, como globales",
                "criterios_evaluacion": [
                    {"id": "CE5.1", "descripcion": "Se ha establecido la diferencia entre dato e información"},
                    {"id": "CE5.2", "descripcion": "Se ha descrito el ciclo de vida del dato"},
                    {"id": "CE5.3", "descripcion": "Se ha identificado la relación entre Big Data, análisis de datos y ciberseguridad"},
                    {"id": "CE5.4", "descripcion": "Se han identificado los riesgos asociados a la protección de datos"},
                    {"id": "CE5.5", "descripcion": "Se han definido los sistemas de seguridad y ciberseguridad a nivel de equipo/sistema"},
                    {"id": "CE5.6", "descripcion": "Se han definido los sistemas de seguridad y ciberseguridad a nivel global"}
                ]
            }
        ]
    },
    "0179": {
        "name": "Inglés Profesional",
        "hours": 67,
        "course": "1º",
        "ras": [
            {
                "id": "RA1",
                "descripcion": "Comprende información, de índole profesional, académica y cotidiana, contenida en todo tipo de discursos orales, emitidos por cualquier medio de comunicación en lengua estándar, interpretando con precisión el contenido del mensaje",
                "criterios_evaluacion": [
                    {"id": "CE1.1", "descripcion": "Se ha identificado la idea principal de mensajes en lengua estándar relacionados con la vida social, profesional o académica"},
                    {"id": "CE1.2", "descripcion": "Se ha reconocido la finalidad de mensajes directos o emitidos en cualquier soporte en lengua estándar"},
                    {"id": "CE1.3", "descripcion": "Se ha extraído información específica contenida en distintos discursos orales en lengua estándar, relacionada con la vida social, profesional o académica"},
                    {"id": "CE1.4", "descripcion": "Se ha identificado el punto de vista y la actitud del hablante"},
                    {"id": "CE1.5", "descripcion": "Se ha identificado el hilo argumental de mensajes orales y determinado los roles que aparecen en dichos mensajes"},
                    {"id": "CE1.6", "descripcion": "Se han comprendido adecuadamente mensajes en lengua estándar en ambientes con contaminación acústica"},
                    {"id": "CE1.7", "descripcion": "Se han extraído las ideas principales de conferencias, charlas e informes, y otras formas de presentación académica y profesional, lingüísticamente complejas"},
                    {"id": "CE1.8", "descripcion": "Se ha tomado conciencia de la importancia de comprender globalmente un mensaje sin entender todos y cada uno de los elementos del mismo"}
                ]
            },
            {
                "id": "RA2",
                "descripcion": "Comprende mensajes escritos, de naturaleza profesional, académica y cotidiana, de relativa dificultad, analizando de forma comprensiva su contenido",
                "criterios_evaluacion": [
                    {"id": "CE2.1", "descripcion": "Se ha identificado la idea principal de textos específicos de su ámbito social, profesional o académico"},
                    {"id": "CE2.2", "descripcion": "Se ha reconocido la finalidad de distintos textos escritos en cualquier soporte, en lengua estándar y relacionados con la actividad profesional"},
                    {"id": "CE2.3", "descripcion": "Se ha extraído información específica de textos, de diferente naturaleza, relativos a su profesión, y contenidos en distintos soportes"},
                    {"id": "CE2.4", "descripcion": "Se ha tomado conciencia de la importancia de comprender globalmente un texto sin entender todos y cada uno de los elementos del mismo"},
                    {"id": "CE2.5", "descripcion": "Se han leído y comprendido, de manera autónoma, textos relacionados con el sector con la velocidad y estilo de lectura propia del nivel competencial"},
                    {"id": "CE2.6", "descripcion": "Se ha interpretado la correspondencia relativa a su especialidad, captando fácilmente el significado esencial"},
                    {"id": "CE2.7", "descripcion": "Se han interpretado textos extensos, y de cierta complejidad, relacionados o no con su especialidad, pudiendo realizar varias lecturas del mismo"},
                    {"id": "CE2.8", "descripcion": "Se ha identificado con rapidez el contenido y la importancia de noticias, artículos e informes sobre una amplia serie de temas profesionales"},
                    {"id": "CE2.9", "descripcion": "Se han interpretado instrucciones, con distintos niveles de dificultad, y mensajes técnicos recibidos a través de soportes digitales"},
                    {"id": "CE2.10", "descripcion": "Se han traducido textos de cierta complejidad, utilizando material de apoyo en caso necesario"}
                ]
            },
            {
                "id": "RA3",
                "descripcion": "Produce mensajes orales claros y bien estructurados, analizando el contenido de la situación y adaptándose al registro lingüístico del interlocutor",
                "criterios_evaluacion": [
                    {"id": "CE3.1", "descripcion": "Se han emitido mensajes generales propios de sector y de la vida cotidiana, utilizando nexos y estrategias de interacción"},
                    {"id": "CE3.2", "descripcion": "Se ha intercambiado con fluidez información específica y detallada utilizando estructuras de una complejidad acorde al nivel competencial"},
                    {"id": "CE3.3", "descripcion": "Se han seleccionado y aplicado los registros adecuados para la emisión del mensaje, así como protocolos y normas de relación social propios del país"},
                    {"id": "CE3.4", "descripcion": "Se han realizado presentaciones, bien estructuradas, sobre temas de su ámbito profesional, haciendo uso de los protocolos establecidos"},
                    {"id": "CE3.5", "descripcion": "Se ha utilizado correctamente la terminología de la profesión"}
                ]
            }
        ]
    },
    "1709": {
        "name": "Itinerario personal para la empleabilidad I",
        "hours": 100,
        "course": "1º",
        "ras": [
            {
                "id": "RA1",
                "descripcion": "Distingue las características del sector productivo y define los puestos de trabajo relacionándolos con las competencias profesionales expresadas en el título",
                "criterios_evaluacion": [
                    {"id": "CE1.1", "descripcion": "Se han analizado las principales oportunidades de empleo y de inserción laboral en el sector profesional, identificando las posibilidades de empleo y analizado sus requerimientos actuales para el perfil profesional"},
                    {"id": "CE1.2", "descripcion": "Se ha comparado los diferentes requerimientos exigidos por el mercado laboral con las exigencias para el trabajo en la función pública relacionados con el sector privado"},
                    {"id": "CE1.3", "descripcion": "Se ha reflexionado sobre las actitudes y aptitudes requeridas actualmente para la actividad profesional relacionadas con el título, así como las competencias personales y sociales más relevantes para el sector identificando nuestra zona de desarrollo próximo"}
                ]
            },
            {
                "id": "RA2",
                "descripcion": "Adquiere las competencias necesarias para el desempeño de las funciones de nivel básico en Prevención de Riesgos Laborales",
                "criterios_evaluacion": [
                    {"id": "CE2.1", "descripcion": "Se ha valorado la importancia de la cultura preventiva en todos los ámbitos actividades de la empresa u organismo equiparado relacionado las condiciones laborales con la salud de la persona trabajadora identificando y clasificando los factores de riesgo en la actividad y los daños derivados de los mismos, especialmente las situaciones de riesgo más habituales en los entornos de trabajo del sector profesional relacionado con el título"},
                    {"id": "CE2.2", "descripcion": "Se han clasificado y descrito los tipos de daños profesionales, con especial referencia a accidentes de trabajo y enfermedades profesionales, relacionados con el perfil profesional del título"},
                    {"id": "CE2.3", "descripcion": "Se ha determinado la evaluación de riesgos en la empresa u organismo equiparado y definido las técnicas de prevención y de protección que deben aplicarse para evitar los daños en su origen y minimizar sus consecuencias"},
                    {"id": "CE2.4", "descripcion": "Se han analizado los protocolos de actuación en caso de emergencia"},
                    {"id": "CE2.5", "descripcion": "Se han determinado los principales derechos y deberes en materia de prevención de riesgos laborales"},
                    {"id": "CE2.6", "descripcion": "Se han clasificado las distintas formas de gestión de la prevención en la empresa u organismo equiparado, en función de los distintos criterios establecidos en la normativa sobre prevención de riesgos laborales y determinado las formas de representación de las personas trabajadoras en la empresa u organismo equiparado en materia de prevención"},
                    {"id": "CE2.7", "descripcion": "Se ha valorado la importancia de la existencia de un plan preventivo en la empresa u organismo equiparado que incluya la secuenciación de actuaciones a realizar en caso de emergencia y reflexionado sobre el contenido del mismo"},
                    {"id": "CE2.8", "descripcion": "Se han determinado los requisitos y condiciones para la vigilancia de la salud de la persona trabajadora y su importancia como medida de prevención"},
                    {"id": "CE2.9", "descripcion": "Se han identificado las técnicas básicas de primeros auxilios que han de ser aplicadas en el lugar del accidente ante distintos tipos de daños y la composición y uso del botiquín"}
                ]
            },
            {
                "id": "RA3",
                "descripcion": "Analiza sus condiciones laborales como persona trabajadora por cuenta ajena identificándolas en los principales tipos de cambios y vicisitudes relevantes que se pueden presentar en la relación laboral en la normativa laboral y especialmente en el convenio colectivo del sector",
                "criterios_evaluacion": [
                    {"id": "CE3.1", "descripcion": "Se han analizado los derechos y obligaciones derivados de la relación laboral, así como las condiciones de trabajo pactadas en un convenio colectivo aplicable al sector profesional relacionado con el título"},
                    {"id": "CE3.2", "descripcion": "Se han comparado las principales"}
                ]
            }
        ]
    },
    "1708": {
        "name": "Sostenibilidad aplicada al sistema productivo",
        "hours": 33,
        "course": "2º",
        "ras": [
            {
                "id": "RA1",
                "descripcion": "Identifica los aspectos ambientales, sociales y de gobernanza (ASG) relativos a la sostenibilidad teniendo en cuenta el concepto de desarrollo sostenible y los marcos internacionales que contribuyen a su consecución",
                "criterios_evaluacion": [
                    {"id": "CE1.1", "descripcion": "Se ha descrito el concepto de sostenibilidad, estableciendo los marcos internacionales asociados al desarrollo sostenible"},
                    {"id": "CE1.2", "descripcion": "Se han identificado los asuntos ambientales, sociales y de gobernanza que influyen en el desarrollo sostenible de las organizaciones empresariales"},
                    {"id": "CE1.3", "descripcion": "Se han relacionado los Objetivos de Desarrollo Sostenible (ODS) con su importancia para la consecución de la Agenda 2030"},
                    {"id": "CE1.4", "descripcion": "Se ha analizado la importancia de identificar los aspectos ASG más relevantes para los grupos de interés de las organizaciones relacionándolos con los riesgos y oportunidades que suponen para la propia organización"},
                    {"id": "CE1.5", "descripcion": "Se han identificado los principales estándares de métricas para la evaluación del desempeño en sostenibilidad y su papel en la rendición de cuentas que marca la legislación vigente y las futuras regulaciones en desarrollo"},
                    {"id": "CE1.6", "descripcion": "Se ha descrito la inversión socialmente responsable y el papel de los analistas, inversores, agencias e índices de sostenibilidad en el fomento de la sostenibilidad"}
                ]
            },
            {
                "id": "RA2",
                "descripcion": "Caracteriza los retos ambientales y sociales a los que se enfrenta la sociedad, describiendo los impactos sobre las personas y los sectores productivos y proponiendo acciones para minimizarlos",
                "criterios_evaluacion": [
                    {"id": "CE2.1", "descripcion": "Se han identificado los principales retos ambientales y sociales"},
                    {"id": "CE2.2", "descripcion": "Se han relacionado los retos ambientales y sociales con el desarrollo de la actividad económica"},
                    {"id": "CE2.3", "descripcion": "Se ha analizado el efecto de los impactos ambientales y sociales sobre las personas y los sectores productivos"},
                    {"id": "CE2.4", "descripcion": "Se han identificado las medidas y acciones encaminadas a minimizar los impactos ambientales y sociales"},
                    {"id": "CE2.5", "descripcion": "Se ha analizado la importancia de establecer alianzas y trabajar de manera transversal y coordinada para abordar con éxito los retos ambientales y sociales"}
                ]
            },
            {
                "id": "RA3",
                "descripcion": "Establece la aplicación de criterios de sostenibilidad en el desempeño profesional y personal, identificando los elementos necesarios",
                "criterios_evaluacion": [
                    {"id": "CE3.1", "descripcion": "Se han identificado los ODS más relevantes para la actividad profesional que realiza"},
                    {"id": "CE3.2", "descripcion": "Se han analizado los riesgos y oportunidades que representan los ODS"},
                    {"id": "CE3.3", "descripcion": "Se han identificado las acciones necesarias para atender algunos de los retos ambientales y sociales desde la actividad profesional y el entorno personal"}
                ]
            },
            {
                "id": "RA4",
                "descripcion": "Propón productos y servicios responsables teniendo en cuenta los principios de la economía circular",
                "criterios_evaluacion": [
                    {"id": "CE4.1", "descripcion": "Se ha caracterizado el modelo de producción y consumo actual"},
                    {"id": "CE4.2", "descripcion": "Se han identificado los principios de la economía verde y circular"},
                    {"id": "CE4.3", "descripcion": "Se han contrastado los beneficios de la economía verde y circular frente al modelo clásico de producción"},
                    {"id": "CE4.4", "descripcion": "Se han aplicado principios de ecodiseño"},
                    {"id": "CE4.5", "descripcion": "Se ha analizado el ciclo de vida del producto"},
                    {"id": "CE4.6", "descripcion": "Se han identificado los procesos de producción y los criterios de sostenibilidad aplicados"}
                ]
            },
            {
                "id": "RA5",
                "descripcion": "Realiza actividades sostenibles minimizando el impacto de las mismas en el medio ambiente",
                "criterios_evaluacion": [
                    {"id": "CE5.1", "descripcion": "Se ha caracterizado el modelo de producción y consumo actual"},
                    {"id": "CE5.2", "descripcion": "Se han identificado los principios de la economía verde y circular"},
                    {"id": "CE5.3", "descripcion": "Se han contrastado los beneficios de la economía verde y circular frente al modelo clásico de producción"},
                    {"id": "CE5.4", "descripcion": "Se ha evaluado el impacto de las actividades personales y profesionales en el medio ambiente"}
                ]
            }
        ]
    },
    "1713": {
        "name": "Proyecto intermodular",
        "hours": 67,
        "course": "2º",
        "ras": [
            {
                "id": "RA1",
                "descripcion": "Caracteriza las empresas del sector atendiendo a su organización y al tipo de producto o servicio que ofrecen",
                "criterios_evaluacion": [
                    {"id": "CE1.1", "descripcion": "Se han identificado las empresas tipo más representativas del sector"},
                    {"id": "CE1.2", "descripcion": "Se ha descrito la estructura organizativa de las empresas"},
                    {"id": "CE1.3", "descripcion": "Se han caracterizado los principales departamentos"},
                    {"id": "CE1.4", "descripcion": "Se han determinado las funciones de cada departamento"},
                    {"id": "CE1.5", "descripcion": "Se ha evaluado el volumen de negocio de acuerdo a las necesidades de los clientes"},
                    {"id": "CE1.6", "descripcion": "Se ha definido la estrategia para dar respuesta a las demandas"},
                    {"id": "CE1.7", "descripcion": "Se han valorado los recursos humanos y materiales necesarios"},
                    {"id": "CE1.8", "descripcion": "Se ha realizado el seguimiento de los resultados de acuerdo a la estrategia aplicada"},
                    {"id": "CE1.9", "descripcion": "Se han relacionado los productos o servicios con su posible contribución a los ODS (Objetivos de Desarrollo Sostenible)"}
                ]
            },
            {
                "id": "RA2",
                "descripcion": "Plantea soluciones a las necesidades del sector teniendo en cuenta la viabilidad de las mismas, los costes asociados y elaborando un pequeño proyecto",
                "criterios_evaluacion": [
                    {"id": "CE2.1", "descripcion": "Se han identificado las necesidades"},
                    {"id": "CE2.2", "descripcion": "Se han planteado en grupo posibles soluciones"},
                    {"id": "CE2.3", "descripcion": "Se ha obtenido la información relativa a las soluciones planteadas"},
                    {"id": "CE2.4", "descripcion": "Se han identificado aspectos innovadores que puedan ser de aplicación"},
                    {"id": "CE2.5", "descripcion": "Se ha realizado el estudio de viabilidad técnica"},
                    {"id": "CE2.6", "descripcion": "Se han identificado las partes que componen el proyecto"},
                    {"id": "CE2.7", "descripcion": "Se han previsto los recursos materiales y humanos para realizarlo"},
                    {"id": "CE2.8", "descripcion": "Se ha realizado el presupuesto económico correspondiente"},
                    {"id": "CE2.9", "descripcion": "Se ha definido y elaborado la documentación para su diseño"},
                    {"id": "CE2.10", "descripcion": "Se han identificado los aspectos relacionados con la calidad del proyecto"},
                    {"id": "CE2.11", "descripcion": "Se han presentado en público las ideas más relevantes de los proyectos propuestos"}
                ]
            },
            {
                "id": "RA3",
                "descripcion": "Planifica la ejecución de las actividades propuestas a la solución planteada, determinando el plan de intervención y elaborando la documentación correspondiente",
                "criterios_evaluacion": [
                    {"id": "CE3.1", "descripcion": "Se han temporizado las secuencias de las actividades"},
                    {"id": "CE3.2", "descripcion": "Se han determinado los recursos y la logística de cada actividad"},
                    {"id": "CE3.3", "descripcion": "Se han identificado permisos y autorizaciones en caso de ser necesarios"},
                    {"id": "CE3.4", "descripcion": "Se han identificado las actividades que implican riesgos en su ejecución"},
                    {"id": "CE3.5", "descripcion": "Se ha tenido en cuenta el plan de prevención de riesgos y los medios y equipos necesarios"},
                    {"id": "CE3.6", "descripcion": "Se han asignado recursos materiales y humanos a cada actividad"},
                    {"id": "CE3.7", "descripcion": "Se han tenido en cuenta posibles imprevistos"},
                    {"id": "CE3.8", "descripcion": "Se han propuesto soluciones a los posibles imprevistos"},
                    {"id": "CE3.9", "descripcion": "Se ha elaborado la documentación necesaria"}
                ]
            },
            {
                "id": "RA4",
                "descripcion": "Realiza el seguimiento de la ejecución de las actividades planteadas, verificando que se cumple con la planificación",
                "criterios_evaluacion": [
                    {"id": "CE4.1", "descripcion": "Se ha definido el procedimiento de seguimiento de las actividades"},
                    {"id": "CE4.2", "descripcion": "Se ha verificado la calidad de los resultados de las actividades"},
                    {"id": "CE4.3", "descripcion": "Se han identificado posibles desviaciones de la planificación y/o los resultados esperados"},
                    {"id": "CE4.4", "descripcion": "Se ha informado de las desviaciones en caso de ser necesario"},
                    {"id": "CE4.5", "descripcion": "Se han solucionado las desviaciones y se han documentado las intervenciones"},
                    {"id": "CE4.6", "descripcion": "Se ha definido y elaborado la documentación necesaria para la evaluación de las actividades y del proyecto en su conjunto"}
                ]
            },
            {
                "id": "RA5",
                "descripcion": "Transmite información con claridad, de manera ordenada y estructurada",
                "criterios_evaluacion": [
                    {"id": "CE5.1", "descripcion": "Se ha mantenido una actitud ordenada y metódica en la transmisión de la información"},
                    {"id": "CE5.2", "descripcion": "Se ha transmitido información verbal tanto horizontal como verticalmente"},
                    {"id": "CE5.3", "descripcion": "Se ha transmitido información entre los miembros del grupo utilizando medios informáticos"},
                    {"id": "CE5.4", "descripcion": "Se han conocido los términos técnicos en otras lenguas que sean estándares del sector"}
                ]
            }
        ]
    }
}

# Read the file
with open('frontend/src/data/curriculos/ele304.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace each module's empty resultados_aprendizaje array
for code, data in MODULES_DATA.items():
    # Find the module block
    pattern = rf'(\{{\s*"codigo":\s*"{code}",\s*"nombre":\s*"[^"]+",\s*"horas":\s*\d+,\s*"curso":\s*"[^"]+",\s*"resultados_aprendizaje":\s*\[\])'
    
    # Build the RA array string
    ra_array = '[\n'
    for ra in data['ras']:
        ra_array += f'        {{\n'
        ra_array += f'          "id": "{ra["id"]}",\n'
        ra_array += f'          "descripcion": "{ra["descripcion"]}",\n'
        ra_array += f'          "criterios_evaluacion": [\n'
        for ce in ra['criterios_evaluacion']:
            ra_array += f'            {{\n'
            ra_array += f'              "id": "{ce["id"]}",\n'
            ra_array += f'              "descripcion": "{ce["descripcion"]}"\n'
            ra_array += f'            }},\n'
        ra_array = ra_array.rstrip(',\n') + '\n'
        ra_array += f'          ]\n'
        ra_array += f'        }},\n'
    ra_array = ra_array.rstrip(',\n') + '\n      ]'
    
    # Replace
    content = re.sub(pattern, lambda m: m.group(1).replace('[]', ra_array), content)

# Write back
with open('frontend/src/data/curriculos/ele304.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated ele304.ts with RA/CE data for missing modules")
