"""Module generator for generating code, tests and documentation from IR definitions.
Version: 1.0.0
Compatible with Core PRD v3.6.3
"""
from typing import Dict, List, Any, Optional
import os
import json
import re
from .prd_parser import PRDParser
from .interface_parser import InterfaceParser
from .dependency_graph import DependencyGraph
from .template_renderer import TemplateRenderer
from utils.error_handler import (
    GenerationError,
    ValidationError,
    TemplateError
)
from utils.logging import setup_logging

logger = setup_logging()

class ModuleGenerator:
    """Handles generation of module code, tests and documentation from IR definitions."""
    
    def __init__(self):
        self.prd_parser = PRDParser()
        self.interface_parser = InterfaceParser()
        self.dep_graph = DependencyGraph()
        
    def generate_module(self, ir_definition: Dict[str, Any], output_dir: str) -> None:
        """Generate a complete module including code, tests and documentation.
        
        Args:
            ir_definition: IR definition dictionary containing module specs
            output_dir: Directory to write generated files to
            
        Raises:
            GenerationError: If module generation fails
            ValidationError: If IR definition is invalid
            TemplateError: If template processing fails
        """
        try:
            # Parse and validate IR definition
            module_spec = self.prd_parser.parse(ir_definition)
            self.validate_module_spec(module_spec)
            
            # Generate source code
            self.generate_source_code(module_spec, output_dir)
            logger.info("Module source code generated successfully")
            
            # Generate tests
            self.generate_tests(module_spec, output_dir)
            logger.info("Module tests generated successfully")
            
            # Generate documentation
            self.generate_documentation(module_spec, output_dir)
            logger.info("Module documentation generated successfully")
            
        except Exception as e:
            logger.error(f"Module generation failed: {str(e)}")
            raise GenerationError(f"Failed to generate module: {str(e)}")
            
    def validate_module_spec(self, module_spec: Dict[str, Any]) -> None:
        """Validate module specification from IR definition.
        
        Args:
            module_spec: Parsed module specification
            
        Raises:
            ValidationError: If specification is invalid
        """
        try:
            # Validate basic structure
            required_fields = ['name', 'version', 'interfaces', 'functions']
            for field in required_fields:
                if field not in module_spec:
                    raise ValidationError(f"Missing required field: {field}")
                    
            # Validate interfaces
            for interface in module_spec['interfaces']:
                self.interface_parser.validate_interface(interface)
                
            # Check dependency graph for cycles
            self.dep_graph.build_graph(module_spec)
            cycles = self.dep_graph.detect_cycles()
            if cycles:
                raise ValidationError(f"Dependency cycles detected: {cycles}")
                
        except Exception as e:
            logger.error(f"Module spec validation failed: {str(e)}")
            raise ValidationError(f"Invalid module specification: {str(e)}")
            
    def generate_source_code(self, module_spec: Dict[str, Any], output_dir: str) -> None:
        """Generate module source code files.
        
        Args:
            module_spec: Validated module specification
            output_dir: Directory to write generated files to
            
        Raises:
            GenerationError: If code generation fails
        """
        try:
            module_dir = os.path.join(output_dir, module_spec['name'])
            os.makedirs(module_dir, exist_ok=True)
            
            # Generate main module file
            self._generate_main_module(module_spec, module_dir)
            
            # Generate interface implementations
            for interface in module_spec['interfaces']:
                self._generate_interface_impl(interface, module_dir)
                
        except Exception as e:
            logger.error(f"Source code generation failed: {str(e)}")
            raise GenerationError(f"Failed to generate source code: {str(e)}")
            
    def generate_tests(self, module_spec: Dict[str, Any], output_dir: str) -> None:
        """Generate module test files.
        
        Args:
            module_spec: Validated module specification
            output_dir: Directory to write generated files to
            
        Raises:
            GenerationError: If test generation fails
        """
        try:
            test_dir = os.path.join(output_dir, module_spec['name'], 'tests')
            os.makedirs(test_dir, exist_ok=True)
            
            # Generate test files  
            self._generate_unit_tests(module_spec, test_dir)
            self._generate_integration_tests(module_spec, test_dir)
            
        except Exception as e:
            logger.error(f"Test generation failed: {str(e)}")
            raise GenerationError(f"Failed to generate tests: {str(e)}")
    
    def generate_documentation(self, module_spec: Dict[str, Any], output_dir: str) -> None:
        """Generate module documentation files.
        
        Args:
            module_spec: Validated module specification
            output_dir: Directory to write generated files to
            
        Raises:
            GenerationError: If documentation generation fails
        """
        try:
            doc_dir = os.path.join(output_dir, module_spec['name'], 'docs')
            os.makedirs(doc_dir, exist_ok=True)
            
            # Generate documentation files
            self._generate_readme(module_spec, doc_dir)
            self._generate_prd(module_spec, doc_dir)
            self._generate_api_docs(module_spec, doc_dir)
            
        except Exception as e:
            logger.error(f"Documentation generation failed: {str(e)}")
            raise GenerationError(f"Failed to generate documentation: {str(e)}")
            
    def _generate_main_module(self, module_spec: Dict[str, Any], module_dir: str) -> None:
        """Generate the main module implementation file.
        
        Args:
            module_spec: Module specification
            module_dir: Directory to write file to
        """
        # Generate main module code from template
        module_code = self._render_module_template(module_spec)
        
        # Write to file
        module_path = os.path.join(module_dir, f"{module_spec['name']}.py")
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(module_code)
            
    def _generate_interface_impl(self, interface: Dict[str, Any], module_dir: str) -> None:
        """Generate implementation for a module interface.
        
        Args:
            interface: Interface specification
            module_dir: Directory to write file to
            
        Raises:
            ValidationError: If interface specification is invalid
            GenerationError: If implementation generation fails
        """
        try:
            # Validate interface specification
            if not interface.get('name'):
                raise ValidationError("Interface must have a name")
            if not interface.get('methods'):
                raise ValidationError(f"Interface {interface['name']} has no methods defined")

            # Generate interface implementation
            impl_code = self._render_interface_template(interface)
            
            # Create implementation file with snake_case name
            impl_name = re.sub('([A-Z])', r'_\1', interface['name']).lower().lstrip('_')
            impl_path = os.path.join(module_dir, f"{impl_name}_impl.py")
            
            # Write implementation file
            os.makedirs(os.path.dirname(impl_path), exist_ok=True)
            with open(impl_path, 'w', encoding='utf-8') as f:
                f.write(impl_code)
                
            logger.info(f"Generated interface implementation: {impl_path}")
                
        except Exception as e:
            logger.error(f"Failed to generate interface implementation: {str(e)}")
            raise GenerationError(f"Interface implementation generation failed: {str(e)}")
            
    def _render_module_template(self, module_spec: Dict[str, Any]) -> str:
        """Render the module code template.
        
        Args:
            module_spec: Module specification
            
        Returns:
            str: Rendered module code
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            renderer = TemplateRenderer(template_dir)
            return renderer.render_module('module.py.jinja', module_spec)
            
        except Exception as e:
            logger.error(f"Module template rendering failed: {str(e)}")
            raise TemplateError(f"Failed to render module template: {str(e)}")
            
    def _render_interface_template(self, interface: Dict[str, Any]) -> str:
        """Render the interface implementation template.
        
        Args:
            interface: Interface specification
            
        Returns:
            str: Rendered interface code
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            renderer = TemplateRenderer(template_dir)

            # Prepare interface implementation context
            impl_context = {
                'module_name': interface['name'] + 'Impl',
                'interface_name': interface['name'],
                'interface_methods': [{
                    'name': method['name'],
                    'params': self._format_method_params(method),
                    'return_annotation': method.get('return_type', 'None'),
                    'docstring': method.get('description', ''),
                    'param_docs': [{
                        'name': param['name'],
                        'description': param.get('description', '')
                    } for param in method.get('parameters', [])],
                    'return_doc': method.get('return_description', ''),
                    'raises': method.get('raises', ['NotImplementedError'])
                } for method in interface.get('methods', [])]
            }

            return renderer.render_module('interface_impl.py.jinja', impl_context)
            
        except Exception as e:
            logger.error(f"Interface template rendering failed: {str(e)}")
            raise TemplateError(f"Failed to render interface template: {str(e)}")

    def _format_method_params(self, method: Dict[str, Any]) -> List[str]:
        """Format method parameters for template rendering.
        
        Args:
            method: Method specification dictionary
            
        Returns:
            List of formatted parameter strings
        """
        params = ['self']  # Start with self for instance methods
        if method.get('parameters'):
            for param in method['parameters']:
                annotation = f": {param['type']}"
                if param.get('optional'):
                    annotation += " = None"
                params.append(f"{param['name']}{annotation}")
        return params

    def _generate_unit_tests(self, module_spec: Dict[str, Any], test_dir: str) -> None:
        """Generate unit test files.
        
        Args:
            module_spec: Module specification 
            test_dir: Directory to write test files to
        """
        # Generate unit tests from template
        test_code = self._render_unit_test_template(module_spec)
        
        # Write to file
        test_path = os.path.join(test_dir, f"test_{module_spec['name']}.py")
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_code)

    def _generate_integration_tests(self, module_spec: Dict[str, Any], test_dir: str) -> None:
        """Generate integration test files.
        
        Args:
            module_spec: Module specification
            test_dir: Directory to write test files to
        """
        # Generate integration tests from template  
        test_code = self._render_integration_test_template(module_spec)
        
        # Write to file
        test_path = os.path.join(test_dir, f"test_{module_spec['name']}_integration.py")
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
            
    def _render_unit_test_template(self, module_spec: Dict[str, Any]) -> str:
        """Render the unit test code template.
        
        Args:
            module_spec: Module specification
            
        Returns:
            str: Rendered test code
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            renderer = TemplateRenderer(template_dir)
            return renderer.render_test('test_module.py.jinja', module_spec)
            
        except Exception as e:
            logger.error(f"Unit test template rendering failed: {str(e)}")
            raise TemplateError(f"Failed to render unit test template: {str(e)}")

    def _render_integration_test_template(self, module_spec: Dict[str, Any]) -> str:
        """Render the integration test code template.
        
        Args:
            module_spec: Module specification
            
        Returns:
            str: Rendered test code
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            renderer = TemplateRenderer(template_dir)
            return renderer.render_test('test_module_integration.py.jinja', module_spec)
            
        except Exception as e:
            logger.error(f"Integration test template rendering failed: {str(e)}")
            raise TemplateError(f"Failed to render integration test template: {str(e)}")
            
    def _generate_readme(self, module_spec: Dict[str, Any], doc_dir: str) -> None:
        """Generate module README documentation.
        
        Args:
            module_spec: Module specification
            doc_dir: Directory to write docs to
        """
        # Generate README from template
        readme = self._render_readme_template(module_spec)
        
        # Write to file
        readme_path = os.path.join(doc_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme)
            
    def _generate_prd(self, module_spec: Dict[str, Any], doc_dir: str) -> None:
        """Generate module PRD documentation.
        
        Args:
            module_spec: Module specification
            doc_dir: Directory to write docs to
        """
        # Generate PRD from template
        prd = self._render_prd_template(module_spec)
        
        # Write to file
        prd_path = os.path.join(doc_dir, f"module-prd-{module_spec['name']}-v{module_spec['version']}.md")
        with open(prd_path, 'w', encoding='utf-8') as f:
            f.write(prd)
            
    def _generate_api_docs(self, module_spec: Dict[str, Any], doc_dir: str) -> None:
        """Generate module API documentation.
        
        Args:
            module_spec: Module specification
            doc_dir: Directory to write docs to
        """
        # Generate API docs from template
        api_docs = self._render_api_docs_template(module_spec)
        
        # Write to file
        api_path = os.path.join(doc_dir, "api.md")
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(api_docs)
            
    def _render_readme_template(self, module_spec: Dict[str, Any]) -> str:
        """Render the README documentation template.
        
        Args:
            module_spec: Module specification
            
        Returns:
            str: Rendered README
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            renderer = TemplateRenderer(template_dir)
            return renderer.render_doc('README.md.jinja', module_spec)
            
        except Exception as e:
            logger.error(f"README template rendering failed: {str(e)}")
            raise TemplateError(f"Failed to render README template: {str(e)}")
            
    def _render_prd_template(self, module_spec: Dict[str, Any]) -> str:
        """Render the PRD documentation template.
        
        Args:
            module_spec: Module specification
            
        Returns:
            str: Rendered PRD
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            renderer = TemplateRenderer(template_dir)
            return renderer.render_doc('module-prd.md.jinja', module_spec)
            
        except Exception as e:
            logger.error(f"PRD template rendering failed: {str(e)}")
            raise TemplateError(f"Failed to render PRD template: {str(e)}")
            
    def _render_api_docs_template(self, module_spec: Dict[str, Any]) -> str:
        """Render the API documentation template.
        
        Args:
            module_spec: Module specification
            
        Returns:
            str: Rendered API docs
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            renderer = TemplateRenderer(template_dir)
            return renderer.render_doc('api.md.jinja', module_spec)
            
        except Exception as e:
            logger.error(f"API docs template rendering failed: {str(e)}")
            raise TemplateError(f"Failed to render API docs template: {str(e)}")
