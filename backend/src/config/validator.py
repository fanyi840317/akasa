# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import yaml
import os
import requests
from urllib.parse import urlparse

from .base import BaseConfig, ConfigLoader
from .system import SystemConfig
from .agents import AgentConfig
from .tools import ToolConfig
from .llm import LLMConfig


class ValidationLevel(Enum):
    """Validation levels for configuration."""
    BASIC = "basic"  # Basic syntax and structure validation
    STANDARD = "standard"  # Standard validation with connectivity checks
    STRICT = "strict"  # Strict validation with all checks enabled
    CUSTOM = "custom"  # Custom validation rules


class ValidationResult(Enum):
    """Validation result status."""
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ValidationReport:
    """Validation report for configuration."""
    level: ValidationLevel
    result: ValidationResult
    message: str
    details: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None


class ConfigValidator:
    """Configuration validator for the mystery event research system."""
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        self.validation_level = validation_level
        self.reports: List[ValidationReport] = []
    
    def validate_config_file(self, config_path: str) -> List[ValidationReport]:
        """Validate configuration file."""
        self.reports = []
        
        # Check if file exists
        if not Path(config_path).exists():
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.FAILED,
                message=f"Configuration file not found: {config_path}"
            ))
            return self.reports
        
        try:
            config_data = ConfigLoader.load_yaml(config_path)
        except yaml.YAMLError as e:
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.FAILED,
                message=f"Invalid YAML syntax: {e}"
            ))
            return self.reports
        except Exception as e:
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.FAILED,
                message=f"Error reading configuration file: {e}"
            ))
            return self.reports
        
        # Validate configuration structure
        self._validate_structure(config_data)
        
        if self.validation_level in [ValidationLevel.STANDARD, ValidationLevel.STRICT]:
            self._validate_api_keys(config_data)
            self._validate_database_connections(config_data)
            self._validate_ai_models(config_data)
        
        if self.validation_level == ValidationLevel.STRICT:
            self._validate_search_engines(config_data)
            self._validate_crawlers(config_data)
            self._validate_workflow(config_data)
            self._validate_performance(config_data)
        
        return self.reports
    
    def validate_system_config(self, config: SystemConfig) -> List[ValidationReport]:
        """Validate system configuration object."""
        self.reports = []
        
        if not config.validate():
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.FAILED,
                message="System configuration validation failed"
            ))
        
        return self.reports
    
    def validate_agents_config(self, config: Dict[str, AgentConfig]) -> List[ValidationReport]:
        """Validate agents configuration object."""
        self.reports = []
        
        for agent_name, agent_config in config.items():
            if not agent_config.validate():
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.FAILED,
                    message=f"Agent configuration validation failed for {agent_name}"
                ))
        
        return self.reports
    
    def validate_tools_config(self, config: ToolConfig) -> List[ValidationReport]:
        """Validate tools configuration object."""
        self.reports = []
        
        if not config.validate():
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.FAILED,
                message="Tools configuration validation failed"
            ))
        
        return self.reports
    
    def validate_llm_config(self, config: LLMConfig) -> List[ValidationReport]:
        """Validate LLM configuration object."""
        self.reports = []
        
        if not config.validate():
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.FAILED,
                message="LLM configuration validation failed"
            ))
        
        return self.reports
    
    def _validate_structure(self, config_data: Dict[str, Any]):
        """Validate basic configuration structure."""
        required_sections = ['system', 'agents', 'tools', 'llm']
        
        for section in required_sections:
            if section not in config_data:
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message=f"Missing configuration section: {section}",
                    suggestions=[f"Add {section} section to configuration"]
                ))
    
    def _validate_api_keys(self, config_data: Dict[str, Any]):
        """Validate API keys configuration."""
        # Check system config API keys
        system_config = config_data.get('system', {})
        api_keys = system_config.get('api_keys', {})
        
        required_keys = ['CNKI_API_KEY', 'WANFANG_API_KEY', 'WEB_OF_SCIENCE_API_KEY']
        for key in required_keys:
            if not api_keys.get(key):
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message=f"Missing API key: {key}",
                    suggestions=[f"Set {key} in environment variables or configuration"]
                ))
        
        # Check agents API configs
        agents_config = config_data.get('agents', {})
        for agent_name, agent in agents_config.items():
            api_config = agent.get('api_config', {})
            api_key = api_config.get('api_key', '')
            if api_key and len(api_key) < 10:
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message=f"API key for agent {agent_name} seems too short",
                    suggestions=[f"Check API key length for agent {agent_name}"]
                ))
        
        # Check tools API configs
        tools_config = config_data.get('tools', {})
        api_configs = tools_config.get('api_configs', {})
        
        for name, config in api_configs.items():
            api_key = config.get('api_key', '')
            if api_key and len(api_key) < 10:
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message=f"API key for {name} seems too short",
                    suggestions=["Verify the API key is correct"]
                ))
    
    def _validate_database_connections(self, config_data: Dict[str, Any]):
        """Validate database connection configurations."""
        system_config = config_data.get('system', {})
        db_config = system_config.get('database', {})
        
        # Validate Neo4j configuration
        neo4j_config = db_config.get('neo4j', {})
        if neo4j_config:
            required_fields = ['uri', 'username', 'password']
            for field in required_fields:
                if not neo4j_config.get(field):
                    self.reports.append(ValidationReport(
                        level=self.validation_level,
                        result=ValidationResult.WARNING,
                        message=f"Missing Neo4j {field}",
                        suggestions=[f"Configure Neo4j {field}"]
                    ))
        
        # Validate Elasticsearch configuration
        es_config = db_config.get('elasticsearch', {})
        if es_config:
            if not es_config.get('hosts'):
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message="Missing Elasticsearch hosts",
                    suggestions=["Configure Elasticsearch hosts"]
                ))
    
    def _validate_ai_models(self, config_data: Dict[str, Any]):
        """Validate AI model configurations."""
        llm_config = config_data.get('llm', {})
        
        # Check if default provider is configured
        default_provider = llm_config.get('default_provider')
        if not default_provider:
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.WARNING,
                message="No default LLM provider configured",
                suggestions=["Set a default LLM provider (openai, anthropic, etc.)"]
            ))
        
        # Validate provider configurations
        providers_config = llm_config.get('providers', {})
        for provider_name, provider_config in providers_config.items():
            if provider_config and not provider_config.get('api_key'):
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message=f"Missing API key for {provider_name}",
                    suggestions=[f"Configure {provider_name.upper()}_API_KEY"]
                ))
    
    def _validate_search_engines(self, config_data: Dict[str, Any]):
        """Validate search engine configurations."""
        tools_config = config_data.get('tools', {})
        search_engine = tools_config.get('search_engine')
        
        if not search_engine:
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.WARNING,
                message="No search engine configured",
                suggestions=["Configure a search engine (tavily, google, etc.)"]
            ))
        
        # Validate search tools
        tools = tools_config.get('tools', {})
        search_tools = [name for name, tool in tools.items() 
                       if tool.get('type') == 'search']
        
        if not search_tools:
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.WARNING,
                message="No search tools configured",
                suggestions=["Configure at least one search tool"]
            ))
    
    def _validate_crawlers(self, config_data: Dict[str, Any]):
        """Validate crawler configurations."""
        tools_config = config_data.get('tools', {})
        tools = tools_config.get('tools', {})
        
        # Check for web scraper tool
        scraper_tools = [name for name, tool in tools.items() 
                        if 'scraper' in name.lower() or 'crawler' in name.lower()]
        
        if not scraper_tools:
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.WARNING,
                message="No web scraper tools configured",
                suggestions=["Configure web scraper tools for data collection"]
            ))
        
        # Validate scraper parameters
        for tool_name, tool_config in tools.items():
            if 'scraper' in tool_name.lower():
                params = tool_config.get('parameters', {})
                timeout = params.get('timeout', 30)
                if timeout > 60:
                    self.reports.append(ValidationReport(
                        level=self.validation_level,
                        result=ValidationResult.WARNING,
                        message=f"High timeout for {tool_name}: {timeout}s",
                        suggestions=["Consider reducing timeout to avoid long waits"]
                    ))
    
    def _validate_workflow(self, config_data: Dict[str, Any]):
        """Validate workflow configurations."""
        agents_config = config_data.get('agents', {})
        
        if not agents_config:
            self.reports.append(ValidationReport(
                level=self.validation_level,
                result=ValidationResult.WARNING,
                message="No agents configured",
                suggestions=["Configure at least one agent for workflow execution"]
            ))
        
        # Check agent-tool dependencies
        tools_config = config_data.get('tools', {})
        tools = tools_config.get('tools', {})
        for agent_name, agent_config in agents_config.items():
            agent_tools = agent_config.get('tools', [])
            for tool_name in agent_tools:
                if tool_name not in tools:
                    self.reports.append(ValidationReport(
                        level=self.validation_level,
                        result=ValidationResult.FAILED,
                        message=f"Agent {agent_name} references undefined tool: {tool_name}",
                        suggestions=[f"Define tool {tool_name} or remove from agent configuration"]
                    ))
    
    def _validate_performance(self, config_data: Dict[str, Any]):
        """Validate performance configurations."""
        system_config = config_data.get('system', {})
        performance = system_config.get('performance', {})
        
        if performance:
            # Check memory settings
            max_memory = performance.get('max_memory_mb')
            if max_memory and max_memory < 512:
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message=f"Low memory limit: {max_memory}MB",
                    suggestions=["Consider increasing memory limit for better performance"]
                ))
            
            # Check cache settings
            cache_enabled = performance.get('cache_enabled', True)
            if not cache_enabled:
                self.reports.append(ValidationReport(
                    level=self.validation_level,
                    result=ValidationResult.WARNING,
                    message="Caching is disabled",
                    suggestions=["Enable caching for better performance"]
                ))
    
    def get_validation_summary(self) -> Dict[str, int]:
        """Get summary of validation results."""
        summary = {
            'total': len(self.reports),
            'passed': 0,
            'warnings': 0,
            'failed': 0,
            'skipped': 0
        }
        
        for report in self.reports:
            summary[report.result.value] += 1
        
        return summary
    
    def has_errors(self) -> bool:
        """Check if there are any failed validations."""
        return any(report.result == ValidationResult.FAILED for report in self.reports)
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return any(report.result == ValidationResult.WARNING for report in self.reports)


def validate_all_configs(config_dir: Optional[str] = None) -> List[ValidationReport]:
    """Validate all configuration files in the config directory."""
    if config_dir is None:
        config_dir = Path(__file__).parent
    else:
        config_dir = Path(config_dir)
    
    validator = ConfigValidator()
    all_reports = []
    
    # Validate main configuration files
    config_files = [
        config_dir / "default.yaml"
    ]
    
    for config_file in config_files:
        if config_file.exists():
            reports = validator.validate_config_file(str(config_file))
            all_reports.extend(reports)
    
    return all_reports


def print_validation_results(reports: List[ValidationReport]):
    """Print validation results in a formatted way."""
    if not reports:
        print("✅ All configurations are valid!")
        return
    
    # Group by result type
    failed = [r for r in reports if r.result == ValidationResult.FAILED]
    warnings = [r for r in reports if r.result == ValidationResult.WARNING]
    passed = [r for r in reports if r.result == ValidationResult.PASSED]
    
    # Print failed validations
    if failed:
        print("❌ Failed Validations:")
        for report in failed:
            print(f"  • {report.message}")
            if report.suggestions:
                for suggestion in report.suggestions:
                    print(f"    💡 {suggestion}")
        print()
    
    # Print warnings
    if warnings:
        print("⚠️  Warnings:")
        for report in warnings:
            print(f"  • {report.message}")
            if report.suggestions:
                for suggestion in report.suggestions:
                    print(f"    💡 {suggestion}")
        print()
    
    # Print summary
    total = len(reports)
    print(f"📊 Summary: {len(failed)} failed, {len(warnings)} warnings, {len(passed)} passed out of {total} checks")
    
    if failed:
        print("\n🚨 Please fix the failed validations before proceeding.")
    elif warnings:
        print("\n💡 Consider addressing the warnings for optimal performance.")
    else:
        print("\n✅ All validations passed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate configuration files")
    parser.add_argument("--config-dir", help="Configuration directory path")
    parser.add_argument("--level", choices=["basic", "standard", "strict"], 
                       default="standard", help="Validation level")
    
    args = parser.parse_args()
    
    reports = validate_all_configs(args.config_dir)
    print_validation_results(reports)
    
    # Exit with error code if there are failed validations
    has_errors = any(r.result == ValidationResult.FAILED for r in reports)
    exit(1 if has_errors else 0)