# question_detector.py
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from enum import Enum
import spacy
import re

class QuestionType(Enum):
    # Preguntas Técnicas
    TECHNICAL_KNOWLEDGE = "technical_knowledge"
    CODING = "coding"
    SYSTEM_DESIGN = "system_design"
    DEBUGGING = "debugging"
    ARCHITECTURE = "architecture"
    
    # Preguntas de Comportamiento
    BEHAVIORAL = "behavioral"
    TEAMWORK = "teamwork"
    LEADERSHIP = "leadership"
    CONFLICT = "conflict_resolution"
    
    # Preguntas Situacionales
    SITUATIONAL = "situational"
    PROBLEM_SOLVING = "problem_solving"
    DECISION_MAKING = "decision_making"
    
    # Preguntas de Experiencia
    EXPERIENCE = "experience"
    PROJECT = "project_specific"
    CHALLENGE = "challenge_faced"
    
    # Otras
    THEORETICAL = "theoretical"
    GENERAL = "general"

@dataclass
class QuestionAnalysis:
    text: str
    question_type: QuestionType
    confidence: float
    complexity: str
    keywords: List[str]
    context: Optional[str]
    language: str
    requires_code_example: bool
    expected_response_length: str  # short, medium, long
    follow_up_potential: bool

class QuestionPatterns:
    def __init__(self):
        self.patterns = {
            'es': {
                'technical': {
                    'keywords': {
                        'implementar', 'desarrollar', 'código', 'programar',
                        'diseñar', 'arquitectura', 'optimizar', 'debug',
                        'resolver', 'explicar', 'cómo funciona'
                    },
                    'patterns': [
                        r'cómo (?:implementarías|desarrollarías)',
                        r'explica(?:r)? (?:el|la|los|las) (?:funcionamiento|arquitectura)',
                        r'diseña(?:r)? un sistema',
                    ]
                },
                'behavioral': {
                    'keywords': {
                        'equipo', 'conflicto', 'situación', 'experiencia',
                        'trabajar', 'liderar', 'manejar', 'resolver'
                    },
                    'patterns': [
                        r'describe una situación',
                        r'cómo manejarías',
                        r'cuéntame sobre una vez'
                    ]
                },
                'situational': {
                    'keywords': {
                        'si tuvieras', 'qué harías', 'cómo manejarías',
                        'en caso de', 'frente a', 'situación'
                    },
                    'patterns': [
                        r'qué harías si',
                        r'cómo manejarías una situación',
                        r'en caso de que'
                    ]
                }
            },
            'en': {
                'technical': {
                    'keywords': {
                        'implement', 'develop', 'code', 'program',
                        'design', 'architecture', 'optimize', 'debug',
                        'solve', 'explain', 'how does'
                    },
                    'patterns': [
                        r'how would you implement',
                        r'explain the (?:architecture|system)',
                        r'design a system'
                    ]
                },
                'behavioral': {
                    'keywords': {
                        'team', 'conflict', 'situation', 'experience',
                        'work', 'lead', 'handle', 'resolve'
                    },
                    'patterns': [
                        r'describe a situation',
                        r'how would you handle',
                        r'tell me about a time'
                    ]
                },
                'situational': {
                    'keywords': {
                        'if you had', 'what would you do', 'how would you handle',
                        'in case of', 'faced with', 'situation'
                    },
                    'patterns': [
                        r'what would you do if',
                        r'how would you handle a situation',
                        r'in case of'
                    ]
                }
            }
        }

class QuestionDetector:
    def __init__(self):
        # Cargar modelos de spaCy
        self.nlp_es = spacy.load("es_core_news_sm")
        self.nlp_en = spacy.load("en_core_web_sm")
        self.patterns = QuestionPatterns().patterns
        
    def analyze_text(self, text: str) -> List[QuestionAnalysis]:
        """Analiza el texto completo en busca de preguntas."""
        # Detectar idioma
        language = self._detect_language(text)
        nlp = self.nlp_es if language == 'es' else self.nlp_en
        
        # Procesar texto
        doc = nlp(text)
        questions = []
        
        # Analizar cada oración
        for sent in doc.sents:
            if self._is_question(sent.text, language):
                analysis = self._analyze_question(sent.text, language)
                if analysis.confidence > 0.5:  # Umbral de confianza
                    questions.append(analysis)
        
        return questions

    def _detect_language(self, text: str) -> str:
        """Detecta el idioma del texto."""
        # Contar palabras clave en cada idioma
        es_patterns = sum(1 for pattern in self.patterns['es']['technical']['keywords'] 
                         if pattern in text.lower())
        en_patterns = sum(1 for pattern in self.patterns['en']['technical']['keywords'] 
                         if pattern in text.lower())
        
        return 'es' if es_patterns >= en_patterns else 'en'

    def _is_question(self, text: str, language: str) -> bool:
        """Determina si un texto es una pregunta."""
        text_lower = text.lower()
        
        # Verificar signos de interrogación
        if '?' in text:
            return True
            
        # Verificar patrones de pregunta
        patterns = self.patterns[language]
        for category in patterns.values():
            if any(re.search(pattern, text_lower) for pattern in category['patterns']):
                return True
                
        return False

    def _analyze_question(self, text: str, language: str) -> QuestionAnalysis:
        """Realiza un análisis completo de la pregunta."""
        text_lower = text.lower()
        
        # Determinar tipo de pregunta
        question_type = self._determine_question_type(text_lower, language)
        
        # Análisis de complejidad
        complexity = self._analyze_complexity(text, language)
        
        # Extraer palabras clave
        keywords = self._extract_keywords(text, language)
        
        # Análisis adicional
        requires_code = self._requires_code_example(text_lower, language)
        response_length = self._estimate_response_length(text_lower, language)
        follow_up = self._has_follow_up_potential(text_lower, language)
        
        return QuestionAnalysis(
            text=text,
            question_type=question_type,
            confidence=self._calculate_confidence(text, language),
            complexity=complexity,
            keywords=keywords,
            context=self._extract_context(text, language),
            language=language,
            requires_code_example=requires_code,
            expected_response_length=response_length,
            follow_up_potential=follow_up
        )

    def _determine_question_type(self, text: str, language: str) -> QuestionType:
        """Determina el tipo específico de pregunta."""
        patterns = self.patterns[language]
        
        # Verificar patrones técnicos
        if any(keyword in text for keyword in patterns['technical']['keywords']):
            if 'código' in text or 'code' in text:
                return QuestionType.CODING
            elif 'arquitectura' in text or 'architecture' in text:
                return QuestionType.ARCHITECTURE
            elif 'debug' in text:
                return QuestionType.DEBUGGING
            return QuestionType.TECHNICAL_KNOWLEDGE
            
        # Verificar patrones de comportamiento
        if any(keyword in text for keyword in patterns['behavioral']['keywords']):
            if 'equipo' in text or 'team' in text:
                return QuestionType.TEAMWORK
            elif 'liderar' in text or 'lead' in text:
                return QuestionType.LEADERSHIP
            elif 'conflicto' in text or 'conflict' in text:
                return QuestionType.CONFLICT
            return QuestionType.BEHAVIORAL
            
        # Verificar patrones situacionales
        if any(keyword in text for keyword in patterns['situational']['keywords']):
            return QuestionType.SITUATIONAL
            
        return QuestionType.GENERAL

    def _analyze_complexity(self, text: str, language: str) -> str:
        """Analiza la complejidad de la pregunta."""
        # Factores de complejidad
        factors = {
            'length': len(text.split()),
            'technical_terms': len(self._extract_technical_terms(text, language)),
            'nested_concepts': text.count('y') + text.count('and'),
            'conditional_statements': text.count('si') + text.count('if')
        }
        
        # Calcular score de complejidad
        complexity_score = (
            factors['length'] * 0.3 +
            factors['technical_terms'] * 0.4 +
            factors['nested_concepts'] * 0.2 +
            factors['conditional_statements'] * 0.1
        )
        
        if complexity_score > 8:
            return "high"
        elif complexity_score > 5:
            return "medium"
        return "low"

    def _extract_keywords(self, text: str, language: str) -> List[str]:
        """Extrae palabras clave relevantes."""
        nlp = self.nlp_es if language == 'es' else self.nlp_en
        doc = nlp(text)
        
        # Extraer sustantivos, verbos y adjetivos importantes
        keywords = [token.text for token in doc 
                   if token.pos_ in ['NOUN', 'VERB', 'ADJ'] 
                   and not token.is_stop]
        
        return list(set(keywords))  # Eliminar duplicados

    def _calculate_confidence(self, text: str, language: str) -> float:
        """Calcula el nivel de confianza de la detección."""
        confidence = 0.0
        
        # Factores que aumentan la confianza
        if '?' in text:
            confidence += 0.4
        
        if any(pattern in text.lower() 
               for pattern in self.patterns[language]['technical']['patterns']):
            confidence += 0.3
            
        if len(self._extract_keywords(text, language)) > 2:
            confidence += 0.2
            
        return min(confidence + 0.1, 1.0)

    def _requires_code_example(self, text: str, language: str) -> bool:
        """Determina si la pregunta requiere ejemplo de código."""
        code_indicators = {
            'es': ['código', 'implementar', 'programar', 'desarrollar', 
                  'función', 'clase', 'método', 'algoritmo'],
            'en': ['code', 'implement', 'program', 'develop', 
                  'function', 'class', 'method', 'algorithm']
        }
        
        # Verificar indicadores de código
        return any(indicator in text.lower() 
                  for indicator in code_indicators[language])

    def _estimate_response_length(self, text: str, language: str) -> str:
        """Estima la longitud esperada de la respuesta."""
        # Factores que influyen en la longitud de la respuesta
        factors = {
            'question_length': len(text.split()),
            'complexity': len(self._extract_technical_terms(text, language)),
            'multiple_parts': text.count('y') + text.count('and') + 
                            text.count(','),
            'depth_indicators': sum(1 for word in ['explica', 'describe', 
                                                 'explain', 'describe', 
                                                 'elaborate', 'detail'] 
                                  if word in text.lower())
        }
        
        # Calcular score
        length_score = (
            factors['question_length'] * 0.3 +
            factors['complexity'] * 0.3 +
            factors['multiple_parts'] * 0.2 +
            factors['depth_indicators'] * 0.2
        )
        
        if length_score > 10:
            return "long"
        elif length_score > 5:
            return "medium"
        return "short"

    def _has_follow_up_potential(self, text: str, language: str) -> bool:
        """Determina si la pregunta tiene potencial para preguntas de seguimiento."""
        follow_up_indicators = {
            'es': ['proceso', 'metodología', 'enfoque', 'estrategia', 
                  'ejemplo', 'caso', 'experiencia'],
            'en': ['process', 'methodology', 'approach', 'strategy', 
                  'example', 'case', 'experience']
        }
        
        return any(indicator in text.lower() 
                  for indicator in follow_up_indicators[language])

    def _extract_technical_terms(self, text: str, language: str) -> Set[str]:
        """Extrae términos técnicos del texto."""
        technical_terms = {
            'es': {
                'programación': ['algoritmo', 'función', 'clase', 'método', 
                               'variable', 'objeto', 'interfaz', 'api',
                               'base de datos', 'framework', 'biblioteca'],
                'arquitectura': ['diseño', 'patrón', 'arquitectura', 'sistema',
                               'microservicio', 'escalabilidad', 'cache'],
                'desarrollo': ['testing', 'debug', 'deployment', 'ci/cd',
                             'versión', 'git', 'docker', 'kubernetes']
            },
            'en': {
                'programming': ['algorithm', 'function', 'class', 'method',
                              'variable', 'object', 'interface', 'api',
                              'database', 'framework', 'library'],
                'architecture': ['design', 'pattern', 'architecture', 'system',
                               'microservice', 'scalability', 'cache'],
                'development': ['testing', 'debug', 'deployment', 'ci/cd',
                              'version', 'git', 'docker', 'kubernetes']
            }
        }
        
        found_terms = set()
        terms_dict = technical_terms[language]
        
        for category in terms_dict.values():
            for term in category:
                if term in text.lower():
                    found_terms.add(term)
                    
        return found_terms

    def _extract_context(self, text: str, language: str) -> Optional[str]:
        """Extrae el contexto relevante de la pregunta."""
        nlp = self.nlp_es if language == 'es' else self.nlp_en
        doc = nlp(text)
        
        # Extraer frases preposicionales y contexto
        context_parts = []
        
        for token in doc:
            # Buscar frases preposicionales
            if token.dep_ in ['prep', 'pobj']:
                context_parts.append(token.text)
            
            # Buscar cláusulas subordinadas
            if token.dep_ in ['advcl', 'relcl']:
                context_parts.append(token.subtree._._get_subtree_text())
                #subtree_text = " ".join([t.text for t in token.subtree])
                #context_parts.append(subtree_text)
                
        return " ".join(context_parts) if context_parts else None

    def _get_subtree_text(self, token) -> str:
        """Obtiene el texto de un subárbol sintáctico."""
        return " ".join([t.text for t in token.subtree])

    def get_question_statistics(self, questions: List[QuestionAnalysis]) -> Dict:
        """Genera estadísticas sobre las preguntas analizadas."""
        stats = {
            'total_questions': len(questions),
            'by_type': {},
            'by_complexity': {
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'by_language': {
                'es': 0,
                'en': 0
            },
            'requires_code': 0,
            'average_confidence': 0,
            'response_length': {
                'short': 0,
                'medium': 0,
                'long': 0
            }
        }
        
        for q in questions:
            # Contar por tipo
            q_type = q.question_type.value
            stats['by_type'][q_type] = stats['by_type'].get(q_type, 0) + 1
            
            # Contar por complejidad
            stats['by_complexity'][q.complexity] += 1
            
            # Contar por idioma
            stats['by_language'][q.language] += 1
            
            # Contar preguntas que requieren código
            if q.requires_code_example:
                stats['requires_code'] += 1
                
            # Acumular confianza
            stats['average_confidence'] += q.confidence
            
            # Contar por longitud de respuesta
            stats['response_length'][q.expected_response_length] += 1
            
        # Calcular promedio de confianza
        if questions:
            stats['average_confidence'] /= len(questions)
            
        return stats
