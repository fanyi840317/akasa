# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from pathlib import Path

from ..base import BaseConfig, ConfigType, ConfigLoader, DatabaseConfig, CacheConfig


class MysteryEventType(str, Enum):
    """Types of mystery events that can be researched."""
    UFO = "ufo"
    CRYPTID = "cryptid"
    PARANORMAL = "paranormal"
    CONSPIRACY = "conspiracy"
    UNEXPLAINED_PHENOMENA = "unexplained_phenomena"
    ANCIENT_MYSTERIES = "ancient_mysteries"
    SUPERNATURAL = "supernatural"
    ANOMALOUS_EVENTS = "anomalous_events"


class DataSourceType(str, Enum):
    """Types of data sources for research."""
    ACADEMIC = "academic"
    NEWS = "news"
    FORUM = "forum"
    DOCUMENTARY = "documentary"
    GOVERNMENT = "government"
    WITNESS_REPORT = "witness_report"
    SOCIAL_MEDIA = "social_media"
    ARCHIVE = "archive"


@dataclass
class DataSourceConfig:
    """Configuration for a specific data source."""
    name: str
    type: DataSourceType
    base_url: str
    api_key: Optional[str] = None
    enabled: bool = True
    max_results: int = 100
    timeout: int = 30
    credibility_weight: float = 1.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataSourceConfig':
        """Create DataSourceConfig from dictionary."""
        # Handle both uppercase and lowercase type values
        type_value = data['type']
        if isinstance(type_value, str):
            # Try to find enum by name (uppercase) or value (lowercase)
            try:
                data_source_type = DataSourceType[type_value.upper()]
            except KeyError:
                data_source_type = DataSourceType(type_value.lower())
        else:
            data_source_type = DataSourceType(type_value)
            
        return cls(
            name=data['name'],
            type=data_source_type,
            base_url=data['base_url'],
            api_key=data.get('api_key'),
            enabled=data.get('enabled', True),
            max_results=data.get('max_results', 100),
            timeout=data.get('timeout', 30),
            credibility_weight=data.get('credibility_weight', 1.0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'type': self.type.value,
            'base_url': self.base_url,
            'api_key': self.api_key,
            'enabled': self.enabled,
            'max_results': self.max_results,
            'timeout': self.timeout,
            'credibility_weight': self.credibility_weight
        }
    
    def validate(self) -> bool:
        """Validate data source configuration."""
        return bool(self.name and self.base_url and 0 <= self.credibility_weight <= 1)


@dataclass
class MysteryEventConfig:
    """Configuration for mystery event research."""
    keywords: Dict[MysteryEventType, List[str]] = field(default_factory=dict)
    data_sources: Dict[str, DataSourceConfig] = field(default_factory=dict)
    credibility_threshold: float = 0.3
    max_search_results: int = 100
    time_window_days: int = 365
    location_radius_km: float = 100.0
    
    def __post_init__(self):
        # Keywords and data_sources will be loaded from configuration file
        # No need for default hardcoded values
        pass
    
    # Default configurations are now loaded from system.yaml
    # This allows for dynamic configuration without code changes
    
    def get_keywords_for_type(self, event_type: MysteryEventType) -> List[str]:
        """Get keywords for a specific mystery event type."""
        return self.keywords.get(event_type, [])
    
    def get_all_keywords(self) -> List[str]:
        """Get all keywords for all mystery event types."""
        all_keywords = []
        for keywords in self.keywords.values():
            all_keywords.extend(keywords)
        return list(set(all_keywords))  # Remove duplicates
    
    def validate(self) -> bool:
        """Validate mystery event configuration."""
        if not (0 <= self.credibility_threshold <= 1):
            return False
        
        for source in self.data_sources.values():
            if not source.validate():
                return False
        
        return True


@dataclass
class PerformanceConfig:
    """Performance and resource configuration."""
    max_memory_mb: int = 2048
    max_processing_time_minutes: int = 30
    batch_size: int = 10
    max_concurrent_requests: int = 5
    request_timeout: int = 30
    
    def validate(self) -> bool:
        """Validate performance configuration."""
        return all([
            self.max_memory_mb > 0,
            self.max_processing_time_minutes > 0,
            self.batch_size > 0,
            self.max_concurrent_requests > 0,
            self.request_timeout > 0
        ])


@dataclass
class SecurityConfig:
    """Security configuration."""
    api_rate_limit: int = 100
    max_file_size_mb: int = 10
    allowed_file_types: List[str] = field(default_factory=lambda: [".txt", ".pdf", ".docx", ".json"])
    encryption_enabled: bool = True
    audit_logging: bool = True
    
    def validate(self) -> bool:
        """Validate security configuration."""
        return all([
            self.api_rate_limit > 0,
            self.max_file_size_mb > 0,
            len(self.allowed_file_types) > 0
        ])


@dataclass
class SystemConfig(BaseConfig):
    """Unified system configuration."""
    
    config_type: ConfigType = field(default=ConfigType.SYSTEM, init=False)
    
    # Basic system info
    name: str = "神秘事件研究系统"
    version: str = "0.1.0"
    description: str = "基于AI的综合性神秘现象研究平台"
    locale: str = "zh-CN"
    timezone: str = "Asia/Shanghai"
    debug: bool = False
    verbose: bool = False
    
    # Mystery event configuration
    mystery_config: MysteryEventConfig = field(default_factory=MysteryEventConfig)
    
    # Database configurations
    neo4j_config: Optional[DatabaseConfig] = None
    elasticsearch_config: Optional[DatabaseConfig] = None
    postgresql_config: Optional[DatabaseConfig] = None
    
    # Cache configuration
    cache_config: CacheConfig = field(default_factory=CacheConfig)
    
    # Performance configuration
    performance_config: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # Security configuration
    security_config: SecurityConfig = field(default_factory=SecurityConfig)
    
    # Feature flags
    feature_research_enabled: bool = True
    feature_crawler_enabled: bool = True
    feature_analysis_enabled: bool = True
    feature_output_enabled: bool = True
    
    # Storage paths
    cache_storage_path: str = "./cache"
    temp_storage_path: str = "./temp"
    output_storage_path: str = "./output"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemConfig':
        """Create system configuration from dictionary."""
        # Extract system basic info
        system_data = data.get('system', {})
        
        # Extract mystery configuration
        mystery_data = data.get('mystery', {})
        
        # Process keywords - convert string keys to enum values
        keywords = {}
        for key, value in mystery_data.get('keywords', {}).items():
            try:
                enum_key = MysteryEventType(key.upper())
                keywords[enum_key] = value
            except ValueError:
                # Skip invalid keys
                continue
        
        # Process data sources
        data_sources = {}
        for name, config in mystery_data.get('data_sources', {}).items():
            data_sources[name] = DataSourceConfig.from_dict(config)
        
        mystery_config = MysteryEventConfig(
            keywords=keywords,
            data_sources=data_sources,
            credibility_threshold=mystery_data.get('credibility_threshold', 0.3),
            max_search_results=mystery_data.get('max_search_results', 100),
            time_window_days=mystery_data.get('time_window_days', 365),
            location_radius_km=mystery_data.get('location_radius_km', 100.0)
        )
        
        # Extract database configurations
        db_data = data.get('database', {})
        neo4j_config = None
        if 'neo4j' in db_data:
            neo4j_data = db_data['neo4j']
            neo4j_config = DatabaseConfig(
                host=neo4j_data.get('uri', 'bolt://localhost:7687').split('//')[1].split(':')[0],
                port=int(neo4j_data.get('uri', 'bolt://localhost:7687').split(':')[-1]),
                database=neo4j_data.get('database', 'neo4j'),
                timeout=neo4j_data.get('connection_timeout', 30),
                max_connections=neo4j_data.get('max_connection_pool_size', 50)
            )
        
        # Extract performance configuration
        perf_data = data.get('performance', {})
        performance_config = PerformanceConfig(
            max_memory_mb=perf_data.get('max_memory_mb', 2048),
            max_processing_time_minutes=perf_data.get('max_processing_time_minutes', 30),
            batch_size=perf_data.get('batch_size', 10),
            max_concurrent_requests=perf_data.get('max_concurrent_requests', 5),
            request_timeout=perf_data.get('request_timeout', 30)
        )
        
        # Extract security configuration
        security_data = data.get('security', {})
        security_config = SecurityConfig(
            api_rate_limit=security_data.get('api_rate_limit', 100),
            max_file_size_mb=security_data.get('max_file_size_mb', 10),
            allowed_file_types=security_data.get('allowed_file_types', [".txt", ".pdf", ".docx", ".json"]),
            encryption_enabled=security_data.get('encryption_enabled', True),
            audit_logging=security_data.get('audit_logging', True)
        )
        
        # Extract cache configuration
        cache_data = data.get('cache', {})
        cache_config = CacheConfig(
            enabled=cache_data.get('enabled', True),
            backend=cache_data.get('backend', 'memory'),
            ttl=cache_data.get('ttl', 3600),
            max_size=cache_data.get('max_size', 1000)
        )
        
        return cls(
            name=system_data.get('name', "神秘事件研究系统"),
            version=system_data.get('version', "0.1.0"),
            description=system_data.get('description', "基于AI的综合性神秘现象研究平台"),
            locale=system_data.get('locale', 'zh-CN'),
            timezone=system_data.get('timezone', 'Asia/Shanghai'),
            debug=system_data.get('debug', False),
            verbose=system_data.get('verbose', False),
            mystery_config=mystery_config,
            neo4j_config=neo4j_config,
            cache_config=cache_config,
            performance_config=performance_config,
            security_config=security_config,
            feature_research_enabled=data.get('feature_research_enabled', True),
            feature_crawler_enabled=data.get('feature_crawler_enabled', True),
            feature_analysis_enabled=data.get('feature_analysis_enabled', True),
            feature_output_enabled=data.get('feature_output_enabled', True),
            cache_storage_path=data.get('cache_storage_path', './cache'),
            temp_storage_path=data.get('temp_storage_path', './temp'),
            output_storage_path=data.get('output_storage_path', './output')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'system': {
                'name': self.name,
                'version': self.version,
                'description': self.description,
                'locale': self.locale,
                'timezone': self.timezone,
                'debug': self.debug,
                'verbose': self.verbose
            },
            'mystery': {
                'keywords': self.mystery_config.keywords,
                'data_sources': {name: {
                    'name': source.name,
                    'type': source.type.value,
                    'base_url': source.base_url,
                    'api_key': source.api_key,
                    'enabled': source.enabled,
                    'max_results': source.max_results,
                    'timeout': source.timeout,
                    'credibility_weight': source.credibility_weight
                } for name, source in self.mystery_config.data_sources.items()},
                'credibility_threshold': self.mystery_config.credibility_threshold,
                'max_search_results': self.mystery_config.max_search_results,
                'time_window_days': self.mystery_config.time_window_days,
                'location_radius_km': self.mystery_config.location_radius_km
            },
            'performance': {
                'max_memory_mb': self.performance_config.max_memory_mb,
                'max_processing_time_minutes': self.performance_config.max_processing_time_minutes,
                'batch_size': self.performance_config.batch_size,
                'max_concurrent_requests': self.performance_config.max_concurrent_requests,
                'request_timeout': self.performance_config.request_timeout
            },
            'security': {
                'api_rate_limit': self.security_config.api_rate_limit,
                'max_file_size_mb': self.security_config.max_file_size_mb,
                'allowed_file_types': self.security_config.allowed_file_types,
                'encryption_enabled': self.security_config.encryption_enabled,
                'audit_logging': self.security_config.audit_logging
            },
            'cache': {
                'enabled': self.cache_config.enabled,
                'backend': self.cache_config.backend,
                'ttl': self.cache_config.ttl,
                'max_size': self.cache_config.max_size
            },
            'feature_research_enabled': self.feature_research_enabled,
            'feature_crawler_enabled': self.feature_crawler_enabled,
            'feature_analysis_enabled': self.feature_analysis_enabled,
            'feature_output_enabled': self.feature_output_enabled,
            'cache_storage_path': self.cache_storage_path,
            'temp_storage_path': self.temp_storage_path,
            'output_storage_path': self.output_storage_path
        }
    
    def validate(self) -> bool:
        """Validate system configuration."""
        return all([
            bool(self.name and self.version),
            self.mystery_config.validate(),
            self.cache_config.validate(),
            self.performance_config.validate(),
            self.security_config.validate()
        ])
    
    def get_mystery_keywords(self, event_type: Optional[MysteryEventType] = None) -> List[str]:
        """Get mystery keywords for specific type or all types."""
        if event_type:
            return self.mystery_config.get_keywords_for_type(event_type)
        return self.mystery_config.get_all_keywords()
    
    def get_reliable_sources(self) -> List[str]:
        """Get list of reliable data sources."""
        return [
            source.name for source in self.mystery_config.data_sources.values()
            if source.enabled and source.credibility_weight >= self.mystery_config.credibility_threshold
        ]


def load_system_config(config_path: Optional[str] = None) -> SystemConfig:
    """Load system configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent / "system.yaml"
    
    data = ConfigLoader.load_yaml(config_path)
    return SystemConfig.from_dict(data)