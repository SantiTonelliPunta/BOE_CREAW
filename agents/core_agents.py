from crewai import Agent
from tools import (
    BOETools, 
    AnalysisTools, 
    DatabaseTools,
    ReportTools,
    QualityTools,
    NotificationTools
)

class BOEAgents:
    def __init__(self):
        self.monitor_agent = Agent(
            name="BOE Monitor",
            role="BOE Data Collector",
            goal="Monitorear y extraer eficientemente información del BOE",
            backstory="Especialista en recopilación y procesamiento de documentos oficiales del BOE",
            tools=[
                BOETools.rss_processor,
                BOETools.xml_extractor,
                BOETools.document_formatter,
                BOETools.url_converter
            ]
        )

        self.analysis_agent = Agent(
            name="Content Analyzer",
            role="Content Analyzer",
            goal="Analizar y categorizar contenido del BOE usando Claude 3.5",
            backstory="Experto en análisis de documentos legales y clasificación",
            tools=[
                AnalysisTools.claude_analyzer,
                AnalysisTools.categorizer,
                AnalysisTools.relevance_scorer,
                AnalysisTools.keyword_extractor
            ]
        )

        self.database_agent = Agent(
            name="Data Manager",
            role="Database Manager",
            goal="Gestionar la persistencia y recuperación eficiente de datos",
            backstory="Especialista en gestión de datos con enfoque en integridad",
            tools=[
                DatabaseTools.postgres_manager,
                DatabaseTools.cache_handler,
                DatabaseTools.data_validator,
                DatabaseTools.query_optimizer
            ]
        )

        self.report_agent = Agent(
            name="Report Specialist",
            role="Executive Report Specialist",
            goal="Crear informes consolidados y personalizados",
            backstory="Experto en comunicación ejecutiva y síntesis de información legal",
            tools=[
                ReportTools.generator,
                ReportTools.summarizer,
                ReportTools.profile_manager,
                ReportTools.format_adapter
            ]
        )

        self.quality_agent = Agent(
            name="Quality Control",
            role="Quality Assurance Specialist",
            goal="Garantizar la precisión y calidad del contenido procesado",
            backstory="Especialista en control de calidad de documentación legal",
            tools=[
                QualityTools.checker,
                QualityTools.validator,
                QualityTools.consistency_monitor,
                QualityTools.error_detector
            ]
        )

        self.notification_agent = Agent(
            name="Notification Manager",
            role="Communication Manager",
            goal="Entregar informes y notificaciones de manera eficiente",
            backstory="Experto en comunicaciones y gestión de notificaciones",
            tools=[
                NotificationTools.email_composer,
                NotificationTools.template_manager,
                NotificationTools.priority_handler,
                NotificationTools.delivery_tracker
            ]
        )

    def get_all_agents(self):
        return [
            self.monitor_agent,
            self.analysis_agent,
            self.database_agent,
            self.report_agent,
            self.quality_agent,
            self.notification_agent
        ] 