"""Template renderer for module code, tests and documentation generation.
Version: 1.0.0
"""
from typing import Dict, Any, Optional
from pathlib import Path
import os
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils.error_handler import TemplateError
from utils.logging import setup_logging

logger = setup_logging()

class TemplateRenderer:
    """Handles template rendering for module generation."""
    
    def __init__(self, template_dir: str):
        """Initialize renderer with template directory.
        
        Args:
            template_dir: Path to directory containing templates
        """
        try:
            self.env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape(['html', 'xml']),
                trim_blocks=True,
                lstrip_blocks=True
            )
            
            # Add custom filters
            self.env.filters['snake_case'] = self._to_snake_case
            self.env.filters['camel_case'] = self._to_camel_case
            self.env.filters['title_case'] = self._to_title_case
            
        except Exception as e:
            logger.error(f"Failed to initialize template renderer: {str(e)}")
            raise TemplateError(f"Template renderer initialization failed: {str(e)}")
            
    def render_module(self, template_name: str, module_spec: Dict[str, Any]) -> str:
        """Render a module code template.
        
        Args:
            template_name: Name of template file
            module_spec: Module specification dictionary
            
        Returns:
            Rendered template string
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**module_spec)
            
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {str(e)}")
            raise TemplateError(f"Template rendering failed: {str(e)}")
            
    def render_test(self, template_name: str, test_spec: Dict[str, Any]) -> str:
        """Render a test code template.
        
        Args:
            template_name: Name of template file
            test_spec: Test specification dictionary
            
        Returns:
            Rendered template string
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**test_spec)
            
        except Exception as e:
            logger.error(f"Failed to render test template {template_name}: {str(e)}")
            raise TemplateError(f"Test template rendering failed: {str(e)}")
            
    def render_doc(self, template_name: str, doc_spec: Dict[str, Any]) -> str:
        """Render a documentation template.
        
        Args:
            template_name: Name of template file
            doc_spec: Documentation specification dictionary
            
        Returns:
            Rendered template string
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**doc_spec)
            
        except Exception as e:
            logger.error(f"Failed to render doc template {template_name}: {str(e)}")
            raise TemplateError(f"Doc template rendering failed: {str(e)}")
            
    def _to_snake_case(self, value: str) -> str:
        """Convert string to snake_case.
        
        Args:
            value: String to convert
            
        Returns:
            Snake case string
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
    def _to_camel_case(self, value: str) -> str:
        """Convert string to camelCase.
        
        Args:
            value: String to convert
            
        Returns:
            Camel case string
        """
        components = value.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
        
    def _to_title_case(self, value: str) -> str:
        """Convert string to Title Case.
        
        Args:
            value: String to convert
            
        Returns:
            Title case string
        """
        return ' '.join(word.capitalize() for word in value.split('_'))
